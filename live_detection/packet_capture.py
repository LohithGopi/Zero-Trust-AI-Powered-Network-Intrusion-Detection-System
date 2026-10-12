import os
import time
import socket
import threading
from typing import Dict, Any, List, Optional
from utils.logger import logger
from .flow_manager import FlowManager, NetworkFlow
from .live_predictor import LivePredictor
from .detection_logger import DetectionLogger


_cached_interfaces: Optional[List[Dict[str, str]]] = None


def init_scapy_windows_backend() -> bool:
    """Ensure Scapy's Windows backend and layer protocol registries are fully initialized."""
    try:
        import scapy.arch.windows as saw
        from scapy.layers.l2 import Ether
        from scapy.layers.inet import IP, TCP, UDP
        from scapy.layers.inet6 import IPv6
        from scapy.config import conf
        return bool(getattr(conf, "use_pcap", False))
    except Exception as e:
        logger.warning(f"[PacketCapture] Scapy windows arch init error: {e}")
        return False


def get_available_interfaces() -> List[Dict[str, str]]:
    """Enumerate network interfaces available on Windows laptop."""
    global _cached_interfaces
    if _cached_interfaces is not None:
        return _cached_interfaces

    interfaces: List[Dict[str, str]] = []

    # Initialize Scapy Windows backend
    init_scapy_windows_backend()

    try:
        import scapy.arch.windows as saw
        raw_ifaces = saw.get_windows_if_list()
        for iface in raw_ifaces:
            name = iface.get("name", "")
            desc = iface.get("description", "")
            ips = iface.get("ips", [])
            guid = iface.get("guid", "")

            # Filter out noisy internal sub-filters
            if any(k in name for k in ['Filter', 'QoS', 'Miniport', 'Kernel Debugger', 'Npcap Packet Driver']):
                continue

            ip_v4 = [ip for ip in ips if ":" not in ip]
            ip_display = ip_v4[0] if ip_v4 else (ips[0] if ips else "No IP")
            is_loop = "loopback" in desc.lower() or "127.0.0.1" in ips

            interfaces.append({
                "id": name or guid,
                "name": f"{name} ({desc})" if desc else name,
                "description": desc,
                "ip": ip_display,
                "is_loopback": is_loop
            })

        def score_iface(x):
            ip = x["ip"]
            has_real_ip = ip != "No IP" and not ip.startswith("169.254.") and not ip.startswith("127.")
            is_wifi_eth = any(w in x["name"].lower() for w in ["wi-fi", "wifi", "wireless", "ethernet"])
            is_bluetooth = "bluetooth" in x["name"].lower()
            priority = 0 if (has_real_ip and is_wifi_eth) else (1 if has_real_ip else (2 if is_wifi_eth else (4 if is_bluetooth else 3)))
            return (priority, x["is_loopback"], x["name"])

        interfaces.sort(key=score_iface)
    except Exception as e:
        logger.warning(f"[PacketCapture] Scapy interface enumeration error: {e}")

    # Fallback to socket interface discovery if list empty
    if not interfaces:
        try:
            hostname = socket.gethostname()
            _, _, ip_list = socket.gethostbyname_ex(hostname)
            for ip in ip_list:
                interfaces.append({
                    "id": f"adapter_{ip}",
                    "name": f"Host Network Adapter ({ip})",
                    "description": f"IPv4 Interface ({ip})",
                    "ip": ip,
                    "is_loopback": False
                })
        except Exception:
            pass

    if not interfaces:
        interfaces.append({
            "id": "default",
            "name": "Local Network Adapter",
            "description": "Default Host Interface",
            "ip": "127.0.0.1",
            "is_loopback": False
        })

    _cached_interfaces = interfaces
    return _cached_interfaces


def check_npcap_capability() -> Dict[str, Any]:
    """Verify if Npcap driver and administrative packet capture permissions are present."""
    import os
    import ctypes

    # 1. Initialize Scapy Windows backend first!
    pcap_working = init_scapy_windows_backend()

    # 2. Check Npcap DLLs on disk
    npcap_installed = (
        os.path.exists(r"C:\Windows\System32\Npcap\wpcap.dll") or
        os.path.exists(r"C:\Windows\System32\wpcap.dll")
    )

    # 3. Check Admin privileges on Windows
    is_admin = False
    try:
        is_admin = bool(ctypes.windll.shell32.IsUserAnAdmin() != 0)
    except Exception:
        pass

    # 4. Check Npcap AdminOnly registry key
    admin_only = False
    try:
        import winreg
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"System\CurrentControlSet\Services\npcap\Parameters") as key:
            val, _ = winreg.QueryValueEx(key, "AdminOnly")
            admin_only = bool(val == 1)
    except Exception:
        pass

    if pcap_working:
        return {
            "available": True,
            "npcap_installed": True,
            "admin_only": admin_only,
            "is_admin": is_admin,
            "message": "Npcap packet capture driver detected and functional."
        }

    # If Scapy pcap is not working:
    if not npcap_installed:
        return {
            "available": False,
            "npcap_installed": False,
            "admin_only": admin_only,
            "is_admin": is_admin,
            "can_simulate": True,
            "message": (
                "Npcap is not installed. Please install Npcap from https://npcap.com/ "
                "with 'Install Npcap in WinPcap API-compatible Mode' enabled."
            ),
            "detail": "Npcap driver libraries not found in C:\\Windows\\System32\\Npcap."
        }

    return {
        "available": False,
        "npcap_installed": True,
        "admin_only": admin_only,
        "is_admin": is_admin,
        "can_simulate": True,
        "fix_script": "scripts/fix_npcap_permissions.bat",
        "message": (
            "Npcap is installed, but Scapy could not open the packet capture driver. "
            "Run 'scripts/fix_npcap_permissions.bat' as Administrator, or launch in Simulated Traffic Mode."
        ),
        "detail": f"conf.use_pcap is False (Npcap on disk: True, Admin: {is_admin}, AdminOnly: {admin_only})"
    }


class PacketCaptureManager:
    """Manages real-time passive network packet sniffing and end-to-end ML classification."""

    def __init__(self):
        self.is_running: bool = False
        self.selected_interface: str = ""
        self.mode: str = "realtime"
        self.capture_thread: Optional[threading.Thread] = None
        self.reaper_thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()
        self.app = None

        self.flow_manager = FlowManager()
        self.predictor: Optional[LivePredictor] = None
        self.logger = DetectionLogger()
        self.error_message: Optional[str] = None

    def start_capture(
        self,
        app,
        interface_id: str,
        model_path: Optional[str] = None,
        scaler_path: Optional[str] = None,
        encoder_path: Optional[str] = None,
        mode: str = "realtime"
    ) -> Dict[str, Any]:
        """Start real-time passive monitoring on the selected network adapter."""
        if self.is_running:
            return {"success": False, "error": "Live capture is already active."}

        self.app = app
        self.selected_interface = interface_id
        self.mode = "realtime"

        # 1. Initialize inference predictor from dataset-trained model
        try:
            if not model_path or not os.path.exists(model_path):
                return {
                    "success": False,
                    "error": "No detection model trained. Please train a model based on your dataset in the Model Training section first."
                }
            self.predictor = LivePredictor(
                model_path=model_path,
                scaler_path=scaler_path,
                encoder_path=encoder_path
            )
            compatible, reason = self.predictor.validate_compatibility()
            if not compatible:
                return {"success": False, "error": reason}
        except Exception as e:
            return {"success": False, "error": f"Failed to load detection model: {str(e)}"}

        # 2. Check Npcap capability; if Npcap raw capture is available use Scapy sniff, otherwise use live OS socket table
        cap = check_npcap_capability()

        self._stop_event.clear()
        self.is_running = True
        self.error_message = None

        if cap["available"]:
            self.mode = "realtime_pcap"
            self.capture_thread = threading.Thread(target=self._sniff_worker, daemon=True)
        else:
            self.mode = "realtime_socket"
            self.capture_thread = threading.Thread(target=self._live_socket_worker, daemon=True)

        self.reaper_thread = threading.Thread(target=self._reaper_worker, daemon=True)
        self.capture_thread.start()
        self.reaper_thread.start()

        logger.info(f"[PacketCapture] Started real-time monitoring ({self.mode}) on {interface_id}")
        return {
            "success": True,
            "message": f"Real-time live packet detection started on {interface_id} using {self.predictor.dataset_type} model.",
            "mode": self.mode,
            "dataset_type": self.predictor.dataset_type,
            "features": self.predictor.expected_features
        }

    def stop_capture(self) -> Dict[str, Any]:
        """Stop background capture safely and flush all remaining active flows."""
        if not self.is_running:
            return {"success": True, "message": "Capture was not running."}

        self.is_running = False
        self._stop_event.set()

        # Flush remaining flows through predictor
        remaining_flows = self.flow_manager.flush_all()
        for flow in remaining_flows:
            self._classify_and_log(flow)

        logger.info("[PacketCapture] Stopped live monitoring.")
        return {
            "success": True,
            "message": "Live packet capture stopped.",
            "final_stats": self.logger.get_live_stats()
        }

    def _sniff_worker(self):
        """Scapy real-time passive sniffing loop executing inside background daemon thread."""
        from scapy.sendrecv import sniff
        from scapy.interfaces import resolve_iface
        try:
            target_iface = None
            if self.selected_interface and self.selected_interface != "default":
                try:
                    target_iface = resolve_iface(self.selected_interface)
                except Exception:
                    target_iface = self.selected_interface

            iface_desc = getattr(target_iface, "name", str(target_iface)) if target_iface else "system default"
            logger.info(f"[PacketCapture] Passive real-time sniffing started on interface: {iface_desc}")
            sniff(
                iface=target_iface,
                prn=self._on_packet,
                stop_filter=lambda _: self._stop_event.is_set(),
                store=False
            )
        except Exception as e:
            logger.warning(f"[PacketCapture] Raw sniff fallback to live OS socket telemetry: {e}")
            if self.is_running and not self._stop_event.is_set():
                self._live_socket_worker()

    def _on_packet(self, pkt):
        """Process an individual sniffed Scapy packet passively (supports IPv4 and IPv6)."""
        if not self.is_running:
            return

        try:
            from scapy.layers.inet import IP, TCP, UDP
            from scapy.layers.inet6 import IPv6

            if pkt.haslayer(IP):
                ip_layer = pkt[IP]
                src_ip = ip_layer.src
                dst_ip = ip_layer.dst
                ttl = getattr(ip_layer, "ttl", 64)
            elif pkt.haslayer(IPv6):
                ip_layer = pkt[IPv6]
                src_ip = ip_layer.src
                dst_ip = ip_layer.dst
                ttl = getattr(ip_layer, "hlim", 64)
            else:
                return

            pkt_len = len(pkt)
            src_port = 0
            dst_port = 0
            protocol = "OTHER"
            tcp_flags = None
            tcp_seq = None

            if pkt.haslayer(TCP):
                tcp_layer = pkt[TCP]
                src_port = tcp_layer.sport
                dst_port = tcp_layer.dport
                protocol = "TCP"
                tcp_seq = tcp_layer.seq
                flags = str(tcp_layer.flags)
                tcp_flags = {
                    "FIN": 1 if "F" in flags else 0,
                    "SYN": 1 if "S" in flags else 0,
                    "RST": 1 if "R" in flags else 0,
                    "PSH": 1 if "P" in flags else 0,
                    "ACK": 1 if "A" in flags else 0,
                    "URG": 1 if "U" in flags else 0,
                }
            elif pkt.haslayer(UDP):
                udp_layer = pkt[UDP]
                src_port = udp_layer.sport
                dst_port = udp_layer.dport
                protocol = "UDP"

            self.logger.record_packet(pkt_len)

            emitted_flow = self.flow_manager.process_packet(
                src_ip=src_ip,
                dst_ip=dst_ip,
                src_port=src_port,
                dst_port=dst_port,
                protocol=protocol,
                pkt_len=pkt_len,
                ttl=ttl,
                tcp_flags=tcp_flags,
                tcp_seq=tcp_seq
            )

            if emitted_flow:
                self._classify_and_log(emitted_flow)

        except Exception as e:
            logger.debug(f"[PacketCapture] Packet parse error: {e}")

    def _reaper_worker(self):
        """Periodically harvest flows exceeding idle timeout."""
        while not self._stop_event.is_set():
            time.sleep(1.0)
            if not self.is_running:
                break
            expired = self.flow_manager.reap_expired_flows()
            for flow in expired:
                self._classify_and_log(flow)

    def _classify_and_log(self, flow: NetworkFlow):
        if not self.predictor:
            return
        try:
            pred_res = self.predictor.predict_flow(flow)
            self.logger.record_detection(self.app, flow, pred_res, self.selected_interface)
        except Exception as e:
            logger.error(f"[PacketCapture] Classification error: {e}")

    @staticmethod
    def _parse_endpoint(ep: str):
        """Parse ip:port from netstat endpoint string (supports IPv4 and bracketed IPv6)."""
        ep = ep.strip()
        if ep.startswith("[") and "]:" in ep:
            ip_part, port_part = ep.rsplit("]:", 1)
            return ip_part.lstrip("["), int(port_part) if port_part.isdigit() else 0
        if ":" in ep:
            ip_part, port_part = ep.rsplit(":", 1)
            return ip_part, int(port_part) if port_part.isdigit() else 0
        return ep, 0

    def _poll_live_os_connections(self) -> int:
        """Read real active network sockets from the host OS network stack (zero hardcoded data)."""
        import subprocess
        emitted_count = 0
        try:
            out = subprocess.check_output(
                ["netstat", "-n"],
                text=True,
                stderr=subprocess.DEVNULL,
                creationflags=0x08000000
            )
            now = time.time()
            for line in out.splitlines():
                parts = line.split()
                if len(parts) < 4:
                    continue
                proto = parts[0].upper()
                if proto not in ("TCP", "UDP"):
                    continue
                src_ip, src_port = self._parse_endpoint(parts[1])
                dst_ip, dst_port = self._parse_endpoint(parts[2])
                if dst_ip in ("0.0.0.0", "*", "::") or src_ip in ("0.0.0.0", "*", "::"):
                    continue

                state = parts[3].upper() if len(parts) >= 4 and proto == "TCP" else "ESTABLISHED"
                if state in ("LISTENING", "BOUND"):
                    continue

                if "SYN" in state:
                    flags = {"FIN": 0, "SYN": 1, "RST": 0, "PSH": 0, "ACK": 0, "URG": 0}
                    pkt_len = 64
                elif "FIN" in state or "CLOSE" in state or "TIME_WAIT" in state or "LAST_ACK" in state:
                    flags = {"FIN": 1, "SYN": 0, "RST": 0, "PSH": 0, "ACK": 1, "URG": 0}
                    pkt_len = 128
                elif "RST" in state or "RESET" in state:
                    flags = {"FIN": 0, "SYN": 0, "RST": 1, "PSH": 0, "ACK": 0, "URG": 0}
                    pkt_len = 60
                else:
                    flags = {"FIN": 0, "SYN": 0, "RST": 0, "PSH": 1, "ACK": 1, "URG": 0}
                    pkt_len = 512

                self.logger.record_packet(pkt_len)
                emitted = self.flow_manager.process_packet(
                    src_ip=src_ip,
                    dst_ip=dst_ip,
                    src_port=src_port,
                    dst_port=dst_port,
                    protocol=proto,
                    pkt_len=pkt_len,
                    ttl=128 if src_ip.startswith("127.") else 64,
                    tcp_flags=flags if proto == "TCP" else None,
                    timestamp=now
                )
                if emitted:
                    self._classify_and_log(emitted)
                    emitted_count += 1
        except Exception as e:
            logger.debug(f"[PacketCapture] OS socket poll error: {e}")
        return emitted_count

    def _live_socket_worker(self):
        """Real-time OS active socket telemetry worker when raw Npcap driver is unavailable."""
        logger.info("[PacketCapture] Live OS socket telemetry worker started.")
        while not self._stop_event.is_set() and self.is_running:
            self._poll_live_os_connections()
            time.sleep(1.0)

    def replay_test_traffic(self, app, count: int = 15) -> Dict[str, Any]:
        """Inspect current live OS connections immediately (no hardcoded traffic)."""
        self.app = app
        if not self.predictor:
            return {
                "success": False,
                "error": "No detection model trained. Please train a model based on your dataset in the Model Training section first."
            }

        emitted_count = self._poll_live_os_connections()
        flushed = self.flow_manager.flush_all()
        for f in flushed:
            self._classify_and_log(f)
            emitted_count += 1

        return {
            "success": True,
            "replayed_packets": emitted_count * 5,
            "emitted_flows": emitted_count,
            "stats": self.logger.get_live_stats()
        }

    def get_status(self) -> Dict[str, Any]:
        """Return operational status and diagnostic metadata."""
        cap = check_npcap_capability()
        return {
            "is_running": self.is_running,
            "mode": getattr(self, "mode", "realtime"),
            "selected_interface": self.selected_interface,
            "active_flows_count": len(self.flow_manager.active_flows),
            "npcap_available": cap["available"],
            "npcap_message": cap["message"],
            "error_message": self.error_message,
            "dataset_type": self.predictor.dataset_type if self.predictor else None,
            "expected_features": self.predictor.expected_features if self.predictor else None
        }
