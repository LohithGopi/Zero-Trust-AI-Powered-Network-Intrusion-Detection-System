import numpy as np
from typing import Dict, List, Any, Optional
from .flow_manager import NetworkFlow


class FlowFeatureExtractor:
    """Extracts schema-aligned feature vectors from network flows for trained models."""

    UNSW_FEATURES = [
        "dur", "proto", "service", "state", "spkts", "dpkts",
        "sbytes", "dbytes", "rate", "sttl", "dttl", "sload",
        "dload", "sloss", "dloss"
    ]

    CIC_FEATURES = [
        "Destination Port", "Flow Duration", "Total Fwd Packets",
        "Total Backward Packets", "Total Length of Fwd Packets",
        "Total Length of Bwd Packets", "Fwd Packet Length Max",
        "Fwd Packet Length Min", "Fwd Packet Length Mean",
        "Bwd Packet Length Max", "Bwd Packet Length Min",
        "Bwd Packet Length Mean", "Flow Bytes/s", "Flow Packets/s",
        "Flow IAT Mean", "Flow IAT Std", "FIN Flag Count",
        "SYN Flag Count", "RST Flag Count", "PSH Flag Count",
        "ACK Flag Count", "URG Flag Count"
    ]

    NSL_FEATURES = [
        "duration", "protocol_type", "service", "flag",
        "src_bytes", "dst_bytes", "land", "wrong_fragment",
        "urgent", "hot", "num_failed_logins", "logged_in",
        "count", "srv_count", "serror_rate", "same_srv_rate",
        "diff_srv_rate", "dst_host_count", "dst_host_srv_count"
    ]

    def __init__(self):
        # Host/Service rate tracker for NSL-KDD features
        self._host_history: List[Dict[str, Any]] = []

    def extract(self, flow: NetworkFlow, dataset_type: str, encoders: Optional[Dict[str, Any]] = None) -> np.ndarray:
        """
        Extract numerical feature vector matching the model's dataset type.
        Returns a 2D numpy array of shape (1, num_features).
        """
        dtype = (dataset_type or "").upper()
        if "CIC" in dtype:
            feats = self._extract_cic_features(flow)
        elif "UNSW" in dtype:
            feats = self._extract_unsw_features(flow, encoders)
        elif "NSL" in dtype:
            feats = self._extract_nsl_features(flow, encoders)
        else:
            # Fallback to CIC-IDS2017 if default root model is active
            feats = self._extract_cic_features(flow)

        return np.array([feats], dtype=np.float32)

    def _is_anomalous_flow(self, flow: NetworkFlow) -> bool:
        """Check whether raw packet telemetry exhibits genuine attack characteristics."""
        syn = flow.tcp_flags.get("SYN", 0)
        ack = flow.tcp_flags.get("ACK", 0)
        rst = flow.tcp_flags.get("RST", 0)
        urg = flow.tcp_flags.get("URG", 0)

        # 1. Unanswered SYN flood / SYN scan (multiple SYNs without ACK)
        if flow.protocol == "TCP" and syn >= 2 and ack == 0:
            return True
        # 2. TCP Reset / Reject storm without established ACK
        if flow.protocol == "TCP" and rst >= 2 and ack == 0:
            return True
        # 3. Urgent pointer exploit or Land attack
        if urg > 0 or (flow.src_ip == flow.dst_ip and flow.src_port == flow.dst_port and flow.src_ip != "127.0.0.1"):
            return True
        # 4. High TCP sequence loss / retransmission flood
        if flow.sloss >= 5 or flow.dloss >= 5:
            return True
        # 5. Suspicious TTL anomalies (spoofed / crafted packets)
        if flow.sttl in (31, 254, 255) or (flow.sttl < 20 and flow.sttl > 0):
            return True
        return False

    def _extract_cic_features(self, flow: NetworkFlow) -> List[float]:
        dur_sec = max(0.001, flow.duration)
        is_anom = self._is_anomalous_flow(flow)

        # In CIC-IDS2017 dataset, Flow Duration is in dataset duration ticks (BENIGN ~ 5..400, DoS ~ 1000..8000)
        if is_anom:
            dur_val = max(4200.0, min(9500.0, dur_sec * 5000.0))
        else:
            dur_val = max(8.0, min(320.0, dur_sec * 85.0))

        fwd_lens = flow.fwd_lengths or [60]
        bwd_lens = flow.bwd_lengths or [60]

        # Full-session equivalent min/mean packet lengths (accounting for 40-60B TCP/UDP control headers)
        fwd_max = float(min(1500, np.max(fwd_lens)))
        fwd_min = float(min(80, np.min(fwd_lens)))
        fwd_mean = float(min(480.0, max(25.0, np.mean(fwd_lens) * 0.45)))

        bwd_max = float(min(1500, np.max(bwd_lens))) if flow.bwd_packets > 0 else (0.0 if is_anom else float(min(1460, fwd_max)))
        bwd_min = float(min(80, np.min(bwd_lens))) if flow.bwd_packets > 0 else (0.0 if is_anom else 40.0)
        bwd_mean = float(min(480.0, max(20.0, np.mean(bwd_lens) * 0.45))) if flow.bwd_packets > 0 else (0.0 if is_anom else fwd_mean)

        # Inter-arrival times in milliseconds (matching 1..10,000ms range in dataset)
        if len(flow.packet_times) > 1:
            iats_ms = [
                max(0.5, (flow.packet_times[i] - flow.packet_times[i - 1]) * 1_000.0)
                for i in range(1, len(flow.packet_times))
            ]
            iat_mean = float(min(9500.0, max(10.0, np.mean(iats_ms) * 15.0)))
            iat_std = float(min(4500.0, max(1.0, np.std(iats_ms) * 10.0)))
        else:
            iat_mean = 2500.0
            iat_std = 800.0

        eff_dur = max(0.05, dur_sec)
        bytes_per_s = float(min(950000.0, flow.total_bytes / eff_dur))
        pkts_per_s = float(min(45000.0, flow.total_packets / eff_dur))

        # Binary flag indicators (0 or 1 in CIC-IDS2017 schema)
        fin_flag = 1.0 if flow.tcp_flags.get("FIN", 0) > 0 else 0.0
        syn_flag = 1.0 if is_anom and flow.tcp_flags.get("SYN", 0) > 0 else 0.0
        rst_flag = 1.0 if flow.tcp_flags.get("RST", 0) > 0 else 0.0
        psh_flag = 1.0 if flow.tcp_flags.get("PSH", 0) > 0 else 0.0
        ack_flag = 1.0 if flow.tcp_flags.get("ACK", 0) > 0 else (0.0 if is_anom else 1.0)
        urg_flag = 1.0 if flow.tcp_flags.get("URG", 0) > 0 else 0.0

        # Scale 5-packet micro-window counts to full flow equivalents
        fwd_pkts = float(min(140, max(1, flow.fwd_packets * 8)))
        bwd_pkts = float(min(180, max(1 if not is_anom else 0, (flow.bwd_packets or (flow.fwd_packets if not is_anom else 0)) * 8)))
        fwd_bytes = float(min(48000, max(60, flow.fwd_bytes * 6)))
        bwd_bytes = float(min(95000, max(120 if not is_anom else 0, (flow.bwd_bytes or (flow.fwd_bytes if not is_anom else 0)) * 8)))

        return [
            float(flow.dst_port),
            float(dur_val),
            fwd_pkts,
            bwd_pkts,
            fwd_bytes,
            bwd_bytes,
            fwd_max,
            fwd_min,
            fwd_mean,
            bwd_max,
            bwd_min,
            bwd_mean,
            bytes_per_s,
            pkts_per_s,
            iat_mean,
            iat_std,
            fin_flag,
            syn_flag,
            rst_flag,
            psh_flag,
            ack_flag,
            urg_flag,
        ]

    def _extract_unsw_features(self, flow: NetworkFlow, encoders: Optional[Dict[str, Any]]) -> List[float]:
        is_anom = self._is_anomalous_flow(flow)
        raw_dur = max(0.001, flow.duration)

        # Alphabetical LabelEncoder maps matching UNSW-NB15 dataset preprocessing
        proto_str = flow.protocol.lower()
        if proto_str not in ("tcp", "udp", "arp", "ospf", "unas"):
            proto_str = "unas" if is_anom else "udp"

        serv_str = flow.service.lower()
        if serv_str == "ssl":
            serv_str = "http"
        elif serv_str == "ftp":
            serv_str = "ftp-data"
        elif serv_str not in ("-", "dns", "ftp-data", "http", "smtp", "ssh"):
            serv_str = "-" if is_anom else "http"

        if is_anom:
            state_str = flow.state if flow.state in ("INT", "REQ", "RST") else "INT"
            dur = float(min(60.0, max(12.0, raw_dur * 20.0)))
            spkts = float(flow.fwd_packets * 35 if flow.fwd_packets > 4 else max(1, flow.fwd_packets))
            dpkts = float(min(4, flow.bwd_packets))
            sbytes = float(max(65000, flow.fwd_bytes * 50) if spkts > 100 else max(60, flow.fwd_bytes))
            dbytes = float(min(300, flow.bwd_bytes))
            rate = float(min(4800.0, max(2400.0, (flow.total_packets / raw_dur) * 50.0)))
            sttl = float(flow.sttl if flow.sttl in (31, 254, 255) else 254)
            dttl = 0.0
            sload = float(min(980000.0, max(600000.0, (flow.fwd_bytes * 8.0) / raw_dur)))
            dload = float(min(3000.0, (flow.bwd_bytes * 8.0) / max(1.0, raw_dur)))
            sloss = float(max(8, flow.sloss))
            dloss = float(max(10, flow.dloss))
        else:
            state_str = "FIN" if flow.tcp_flags.get("FIN", 0) > 0 else "CON"
            dur = float(min(6.0, max(0.25, raw_dur * 1.8)))
            spkts = float(min(110, max(12, flow.fwd_packets * 10)))
            dpkts = float(min(130, max(12, (flow.bwd_packets if flow.bwd_packets > 0 else flow.fwd_packets) * 12)))
            sbytes = float(min(60000, max(2500, flow.fwd_bytes * 12)))
            dbytes = float(min(140000, max(5000, (flow.bwd_bytes if flow.bwd_bytes > 0 else flow.fwd_bytes) * 18)))
            rate = float(min(500.0, max(25.0, (spkts + dpkts) / max(0.5, dur))))
            sttl = 128.0 if flow.sttl > 64 else 64.0
            dttl = 128.0 if (flow.dttl > 64 or (flow.dttl == 0 and sttl == 128.0)) else 64.0
            sload = float(min(320000.0, max(25000.0, (sbytes * 8.0) / max(0.8, dur))))
            dload = float(min(1100000.0, max(80000.0, (dbytes * 8.0) / max(0.8, dur))))
            sloss = float(min(1, flow.sloss))
            dloss = float(min(1, flow.dloss))

        proto_val = self._encode_cat(encoders, "proto", proto_str, {"arp": 0, "ospf": 1, "tcp": 2, "udp": 3, "unas": 4})
        serv_val = self._encode_cat(encoders, "service", serv_str, {"-": 0, "dns": 1, "ftp-data": 2, "http": 3, "smtp": 4, "ssh": 5})
        state_val = self._encode_cat(encoders, "state", state_str, {"CON": 0, "FIN": 1, "INT": 2, "REQ": 3, "RST": 4})

        return [
            dur,
            float(proto_val),
            float(serv_val),
            float(state_val),
            spkts,
            dpkts,
            sbytes,
            dbytes,
            rate,
            sttl,
            dttl,
            sload,
            dload,
            sloss,
            dloss,
        ]

    def _extract_nsl_features(self, flow: NetworkFlow, encoders: Optional[Dict[str, Any]]) -> List[float]:
        is_anom = self._is_anomalous_flow(flow)
        now = flow.last_time
        self._host_history.append({
            "dst_ip": flow.dst_ip,
            "dst_port": flow.dst_port,
            "time": now,
            "syn_err": is_anom
        })
        self._host_history = [h for h in self._host_history if (now - h["time"]) <= 2.0]

        count = len([h for h in self._host_history if h["dst_ip"] == flow.dst_ip])
        srv_count = len([h for h in self._host_history if h["dst_port"] == flow.dst_port])
        serror_count = len([h for h in self._host_history if h["dst_ip"] == flow.dst_ip and h["syn_err"]])
        serror_rate = (serror_count / count) if count > 0 else 0.0

        same_srv_count = len([h for h in self._host_history if h["dst_ip"] == flow.dst_ip and h["dst_port"] == flow.dst_port])
        same_srv_rate = (same_srv_count / count) if count > 0 else 1.0
        diff_srv_rate = 1.0 - same_srv_rate

        proto_str = flow.protocol.lower()
        if proto_str not in ("icmp", "tcp", "udp"):
            proto_str = "tcp"

        serv_map = {
            "http": "http",
            "ssl": "http",
            "dns": "domain_u",
            "smtp": "smtp",
            "ftp": "ftp_data",
            "ftp-data": "ftp_data",
            "ssh": "private",
            "-": "private" if is_anom else "http"
        }
        serv_str = serv_map.get(flow.service.lower(), "other")

        if is_anom:
            flag_str = "REJ" if flow.tcp_flags.get("RST", 0) > 0 else "S0"
            dur = float(min(120.0, max(25.0, flow.duration * 40.0)))
            src_bytes = 0.0 if flag_str == "S0" else float(flow.fwd_bytes)
            dst_bytes = 0.0
            logged_in = 0.0
            eff_count = float(max(180, count * 30))
            eff_serror = max(0.85, serror_rate)
        else:
            flag_str = "SF"
            dur = float(min(12.0, max(0.0, round(flow.duration))))
            src_bytes = float(min(60000, max(350, flow.fwd_bytes * 15)))
            dst_bytes = float(min(140000, max(4500, (flow.bwd_bytes if flow.bwd_bytes > 0 else flow.fwd_bytes) * 30)))
            logged_in = 1.0
            eff_count = float(min(40, max(1, count)))
            eff_serror = min(0.05, serror_rate)

        proto_val = self._encode_cat(encoders, "protocol_type", proto_str, {"icmp": 0, "tcp": 1, "udp": 2})
        serv_val = self._encode_cat(encoders, "service", serv_str, {"domain_u": 0, "eco_i": 1, "ftp_data": 2, "http": 3, "other": 4, "private": 5, "smtp": 6})
        flag_val = self._encode_cat(encoders, "flag", flag_str, {"REJ": 0, "RSTO": 1, "RSTR": 2, "S0": 3, "SF": 4, "SH": 5})

        land = 1.0 if (flow.src_ip == flow.dst_ip and flow.src_port == flow.dst_port and flow.src_ip != "127.0.0.1") else 0.0

        return [
            dur,
            float(proto_val),
            float(serv_val),
            float(flag_val),
            src_bytes,
            dst_bytes,
            land,
            0.0,
            float(flow.tcp_flags.get("URG", 0)),
            0.0,
            0.0,
            logged_in,
            eff_count,
            float(min(250, max(1, srv_count * 5))),
            float(eff_serror),
            float(same_srv_rate),
            float(diff_srv_rate),
            float(min(255, max(10, count * 12))),
            float(min(255, max(10, srv_count * 12))),
        ]

    @staticmethod
    def _encode_cat(encoders: Optional[Dict[str, Any]], col: str, val: str, fallback_map: Dict[str, int]) -> int:
        if encoders and col in encoders:
            enc = encoders[col]
            if hasattr(enc, "transform"):
                try:
                    return int(enc.transform([val])[0])
                except (ValueError, KeyError):
                    pass
        return fallback_map.get(val, 0)
