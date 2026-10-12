import io
import csv
import time
from collections import deque
from datetime import datetime
from typing import Dict, Any, List, Optional
from database.init_db import db, LiveDetection
from utils.logger import logger


class DetectionLogger:
    """Manages persistent database storage, rolling in-memory cache, and CSV export."""

    def __init__(self, memory_buffer_size: int = 300):
        self.memory_buffer = deque(maxlen=memory_buffer_size)
        self.alerts_buffer = deque(maxlen=100)
        self.stats = {
            "total_flows": 0,
            "normal_flows": 0,
            "attack_flows": 0,
            "high_risk": 0,
            "medium_risk": 0,
            "low_risk": 0,
            "total_packets": 0,
            "total_bytes": 0,
            "raw_packets": 0,
            "raw_bytes": 0,
            "start_time": time.time(),
        }

    def record_packet(self, pkt_len: int = 0):
        """Update live streaming packet and byte counters in real time as packets arrive."""
        self.stats["raw_packets"] = self.stats.get("raw_packets", 0) + 1
        self.stats["raw_bytes"] = self.stats.get("raw_bytes", 0) + pkt_len

    def record_detection(
        self,
        app,
        flow,
        pred_result: Dict[str, Any],
        interface: str = "Unknown"
    ) -> Dict[str, Any]:
        """Record flow prediction to in-memory buffers and SQLite database."""
        now_dt = datetime.utcnow()
        prediction = pred_result["prediction"]
        confidence = pred_result["confidence"]
        risk_level = pred_result["risk_level"]
        is_attack = pred_result.get("is_attack", False)

        record_dict = {
            "timestamp": now_dt.strftime("%Y-%m-%d %H:%M:%S"),
            "source_ip": flow.src_ip,
            "destination_ip": flow.dst_ip,
            "source_port": flow.src_port,
            "destination_port": flow.dst_port,
            "protocol": flow.protocol,
            "flow_duration": round(flow.duration, 3),
            "packet_count": flow.total_packets,
            "bytes": flow.total_bytes,
            "prediction": prediction,
            "confidence": confidence,
            "risk_level": risk_level,
            "interface": interface,
            "status": "Alert" if is_attack else "Normal"
        }

        # Update stats
        self.stats["total_flows"] += 1
        self.stats["total_packets"] += flow.total_packets
        self.stats["total_bytes"] += flow.total_bytes
        if is_attack:
            self.stats["attack_flows"] += 1
        else:
            self.stats["normal_flows"] += 1

        if risk_level == "HIGH":
            self.stats["high_risk"] += 1
        elif risk_level == "MEDIUM":
            self.stats["medium_risk"] += 1
        else:
            self.stats["low_risk"] += 1

        # Memory buffers
        self.memory_buffer.appendleft(record_dict)
        if is_attack or risk_level in ("HIGH", "MEDIUM"):
            self.alerts_buffer.appendleft(record_dict)

        # Database persistence
        if app:
            try:
                with app.app_context():
                    db_entry = LiveDetection(
                        timestamp=now_dt,
                        source_ip=flow.src_ip,
                        destination_ip=flow.dst_ip,
                        source_port=flow.src_port,
                        destination_port=flow.dst_port,
                        protocol=flow.protocol,
                        flow_duration=round(flow.duration, 3),
                        packet_count=flow.total_packets,
                        bytes=flow.total_bytes,
                        prediction=prediction,
                        confidence=confidence,
                        risk_level=risk_level,
                        interface=interface,
                        status=record_dict["status"]
                    )
                    db.session.add(db_entry)
                    db.session.commit()
                    record_dict["id"] = db_entry.id
            except Exception as e:
                logger.error(f"[DetectionLogger] DB insert error: {e}")

        return record_dict

    def get_live_stats(self) -> Dict[str, Any]:
        """Return real-time throughput and detection summary."""
        elapsed = max(1.0, time.time() - self.stats["start_time"])
        total_pkts = max(self.stats["total_packets"], self.stats.get("raw_packets", 0))
        total_bytes = max(self.stats["total_bytes"], self.stats.get("raw_bytes", 0))
        return {
            **self.stats,
            "total_packets": total_pkts,
            "total_bytes": total_bytes,
            "elapsed_seconds": round(elapsed, 1),
            "flows_per_sec": round(self.stats["total_flows"] / elapsed, 2),
            "packets_per_sec": round(total_pkts / elapsed, 2),
            "kb_per_sec": round((total_bytes / 1024.0) / elapsed, 2)
        }

    def get_recent_detections(self, limit: int = 50) -> List[Dict[str, Any]]:
        return list(self.memory_buffer)[:limit]

    def get_recent_alerts(self, limit: int = 20) -> List[Dict[str, Any]]:
        return list(self.alerts_buffer)[:limit]

    def reset_stats(self):
        self.stats = {
            "total_flows": 0,
            "normal_flows": 0,
            "attack_flows": 0,
            "high_risk": 0,
            "medium_risk": 0,
            "low_risk": 0,
            "total_packets": 0,
            "total_bytes": 0,
            "start_time": time.time(),
        }

    def export_csv(self, app, limit: int = 1000) -> str:
        """Export detection history from SQLite to CSV formatted string."""
        output = io.StringIO()
        fieldnames = [
            "id", "timestamp", "source_ip", "destination_ip", "source_port",
            "destination_port", "protocol", "flow_duration", "packet_count",
            "bytes", "prediction", "confidence", "risk_level", "interface", "status"
        ]
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()

        if app:
            try:
                with app.app_context():
                    rows = LiveDetection.query.order_by(LiveDetection.id.desc()).limit(limit).all()
                    for r in rows:
                        writer.writerow(r.to_dict())
            except Exception as e:
                logger.error(f"[DetectionLogger] CSV export query error: {e}")
        else:
            for r in self.memory_buffer:
                writer.writerow(r)

        return output.getvalue()
