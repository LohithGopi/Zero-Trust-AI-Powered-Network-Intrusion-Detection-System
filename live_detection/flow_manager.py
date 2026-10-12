import time
from collections import OrderedDict
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Tuple


@dataclass
class NetworkFlow:
    src_ip: str
    dst_ip: str
    src_port: int
    dst_port: int
    protocol: str
    start_time: float
    last_time: float
    fwd_packets: int = 0
    bwd_packets: int = 0
    fwd_bytes: int = 0
    bwd_bytes: int = 0
    fwd_lengths: List[int] = field(default_factory=list)
    bwd_lengths: List[int] = field(default_factory=list)
    packet_times: List[float] = field(default_factory=list)
    tcp_flags: Dict[str, int] = field(default_factory=lambda: {
        "FIN": 0, "SYN": 0, "RST": 0, "PSH": 0, "ACK": 0, "URG": 0
    })
    sttl: int = 64
    dttl: int = 0
    state: str = "INT"
    service: str = "-"
    sloss: int = 0
    dloss: int = 0
    fwd_seqs: set = field(default_factory=set)
    bwd_seqs: set = field(default_factory=set)
    last_emitted_packets: int = 0

    @property
    def duration(self) -> float:
        return max(0.0001, self.last_time - self.start_time)

    @property
    def total_packets(self) -> int:
        return self.fwd_packets + self.bwd_packets

    @property
    def total_bytes(self) -> int:
        return self.fwd_bytes + self.bwd_bytes

    def is_forward(self, src_ip: str, src_port: int) -> bool:
        return self.src_ip == src_ip and self.src_port == src_port


class FlowManager:
    """Aggregates raw packets into bidirectional network conversation flows."""

    def __init__(self, idle_timeout: float = 2.0, live_packet_threshold: int = 5, max_flows: int = 5000):
        self.idle_timeout = idle_timeout
        self.live_packet_threshold = live_packet_threshold
        self.max_flows = max_flows
        self.active_flows: OrderedDict[str, NetworkFlow] = OrderedDict()

    @staticmethod
    def get_canonical_key(src_ip: str, dst_ip: str, src_port: int, dst_port: int, protocol: str) -> str:
        endpoint_a = (src_ip, src_port)
        endpoint_b = (dst_ip, dst_port)
        if endpoint_a > endpoint_b:
            endpoint_a, endpoint_b = endpoint_b, endpoint_a
        return f"{endpoint_a[0]}:{endpoint_a[1]}<->{endpoint_b[0]}:{endpoint_b[1]}@{protocol}"

    def process_packet(
        self,
        src_ip: str,
        dst_ip: str,
        src_port: int,
        dst_port: int,
        protocol: str,
        pkt_len: int,
        ttl: int = 64,
        tcp_flags: Optional[Dict[str, int]] = None,
        tcp_seq: Optional[int] = None,
        timestamp: Optional[float] = None
    ) -> Optional[NetworkFlow]:
        """
        Ingest an individual packet into its corresponding bidirectional flow.
        Returns the flow if it reached an emission boundary (FIN/RST or batch threshold).
        """
        now = timestamp or time.time()
        flow_key = self.get_canonical_key(src_ip, dst_ip, src_port, dst_port, protocol)

        flow = self.active_flows.get(flow_key)
        if flow is None:
            # Capacity check: evict oldest flow if limit exceeded
            if len(self.active_flows) >= self.max_flows:
                self.active_flows.popitem(last=False)

            flow = NetworkFlow(
                src_ip=src_ip,
                dst_ip=dst_ip,
                src_port=src_port,
                dst_port=dst_port,
                protocol=protocol,
                start_time=now,
                last_time=now,
                sttl=ttl,
                service=self._identify_service(src_port, dst_port)
            )
            self.active_flows[flow_key] = flow
        else:
            self.active_flows.move_to_end(flow_key)
            flow.last_time = now

        flow.packet_times.append(now)
        is_fwd = flow.is_forward(src_ip, src_port)

        if is_fwd:
            flow.fwd_packets += 1
            flow.fwd_bytes += pkt_len
            flow.fwd_lengths.append(pkt_len)
            flow.sttl = ttl
            if tcp_seq is not None:
                if tcp_seq in flow.fwd_seqs:
                    flow.sloss += 1
                else:
                    flow.fwd_seqs.add(tcp_seq)
        else:
            flow.bwd_packets += 1
            flow.bwd_bytes += pkt_len
            flow.bwd_lengths.append(pkt_len)
            if flow.dttl == 0:
                flow.dttl = ttl
            if tcp_seq is not None:
                if tcp_seq in flow.bwd_seqs:
                    flow.dloss += 1
                else:
                    flow.bwd_seqs.add(tcp_seq)

        # Update TCP flags & connection state
        should_emit = False
        if tcp_flags:
            for flag, val in tcp_flags.items():
                if val:
                    flow.tcp_flags[flag] = flow.tcp_flags.get(flag, 0) + 1

            if tcp_flags.get("ACK"):
                flow.state = "CON"
                if flow.dttl == 0:
                    flow.dttl = flow.sttl
            elif tcp_flags.get("SYN") and not tcp_flags.get("ACK"):
                flow.state = "REQ"

            if tcp_flags.get("FIN") or tcp_flags.get("RST"):
                flow.state = "FIN" if tcp_flags.get("FIN") else "RST"
                should_emit = True
        elif protocol == "UDP":
            flow.state = "CON"
            if flow.dttl == 0:
                flow.dttl = flow.sttl

        # Emit if packet batch threshold reached
        unemitted_pkts = flow.total_packets - flow.last_emitted_packets
        if unemitted_pkts >= self.live_packet_threshold:
            should_emit = True

        if should_emit:
            flow.last_emitted_packets = flow.total_packets
            # Pop flow so next packet batch starts a clean measurement window
            # (prevents normal long-lived HTTPS connections from accumulating giant duration/flag values)
            self.active_flows.pop(flow_key, None)
            return flow

        return None

    def reap_expired_flows(self, now: Optional[float] = None) -> List[NetworkFlow]:
        """Collect and remove flows that exceeded idle inactivity timeout."""
        current_time = now or time.time()
        expired: List[NetworkFlow] = []
        keys_to_remove = []

        for key, flow in self.active_flows.items():
            if (current_time - flow.last_time) >= self.idle_timeout:
                if flow.total_packets > flow.last_emitted_packets:
                    flow.last_emitted_packets = flow.total_packets
                    expired.append(flow)
                keys_to_remove.append(key)

        for k in keys_to_remove:
            self.active_flows.pop(k, None)

        return expired

    def flush_all(self) -> List[NetworkFlow]:
        """Flush all remaining in-flight flows when stopping capture."""
        remaining = [f for f in self.active_flows.values() if f.total_packets > f.last_emitted_packets]
        self.active_flows.clear()
        return remaining

    @staticmethod
    def _identify_service(src_port: int, dst_port: int) -> str:
        ports = {
            80: "http", 443: "http", 8080: "http", 8443: "http", 5000: "http",
            53: "dns", 5353: "dns", 20: "ftp-data", 21: "ftp-data", 22: "ssh",
            25: "smtp", 587: "smtp", 110: "http", 143: "http"
        }
        return ports.get(dst_port) or ports.get(src_port) or "http"

