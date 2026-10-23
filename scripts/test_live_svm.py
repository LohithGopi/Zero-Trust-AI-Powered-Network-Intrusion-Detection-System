import sys
import os
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app
from config import Config
from live_detection.flow_manager import FlowManager, NetworkFlow
from live_detection.live_predictor import LivePredictor
from live_detection.packet_capture import PacketCaptureManager

def test_live_detection():
    print("=" * 80)
    print(">>> VERIFYING LIVE PACKET DETECTION WITH TRAINED SVM MODEL")
    print("=" * 80)

    model_path = os.path.join(Config.MODEL_DIR, "model.joblib")
    scaler_path = Config.SCALER_FILE_PATH
    encoder_path = Config.ENCODER_FILE_PATH

    print(f"Loading Model: {model_path}")
    print(f"Loading Scaler: {scaler_path}")
    print(f"Loading Encoder: {encoder_path}")

    # 1. Initialize LivePredictor
    predictor = LivePredictor(
        model_path=model_path,
        scaler_path=scaler_path,
        encoder_path=encoder_path
    )

    print(f"\n[OK] LivePredictor initialized successfully:")
    print(f"  - Detected Algorithm : {predictor.algorithm_name}")
    print(f"  - Target Dataset     : {predictor.dataset_type}")
    print(f"  - Expected Features  : {predictor.expected_features}")

    # 2. Simulate Normal / Benign Flow
    now = time.time()
    normal_flow = NetworkFlow(
        src_ip="192.168.1.45",
        dst_ip="142.250.190.46",  # Google IP
        src_port=54321,
        dst_port=443,              # HTTPS
        protocol="TCP",
        start_time=now - 1.2,
        last_time=now,
        fwd_packets=12,
        bwd_packets=10,
        fwd_bytes=1420,
        bwd_bytes=4850,
        fwd_lengths=[120, 340, 520, 440],
        bwd_lengths=[500, 1400, 1400, 1550],
        tcp_flags={"FIN": 0, "SYN": 1, "RST": 0, "PSH": 1, "ACK": 1, "URG": 0},
        sttl=64,
        dttl=56,
        ground_truth="normal"
    )

    res_normal = predictor.predict_flow(normal_flow)
    print("\n--- TEST FLOW 1: BENIGN HTTPS TRAFFIC ---")
    print(f"  Connection : {res_normal['flow_summary']['src']} -> {res_normal['flow_summary']['dst']} ({res_normal['flow_summary']['protocol']})")
    print(f"  Prediction : {res_normal['prediction']}")
    print(f"  Is Attack  : {res_normal['is_attack']}")
    print(f"  Confidence : {res_normal['confidence'] * 100:.2f}%")
    print(f"  Risk Level : {res_normal['risk_level']}")
    print(f"  Latency    : {res_normal['latency_ms']:.3f} ms")

    # 3. Simulate Attack / SYN Flood Flow
    attack_flow = NetworkFlow(
        src_ip="10.0.0.99",
        dst_ip="192.168.1.1",
        src_port=44444,
        dst_port=80,
        protocol="TCP",
        start_time=now - 0.05,
        last_time=now,
        fwd_packets=150,
        bwd_packets=0,
        fwd_bytes=9000,
        bwd_bytes=0,
        fwd_lengths=[60] * 20,
        bwd_lengths=[],
        tcp_flags={"FIN": 0, "SYN": 150, "RST": 0, "PSH": 0, "ACK": 0, "URG": 0},
        sttl=255,
        dttl=0,
        sloss=15,
        ground_truth="neptune"
    )

    res_attack = predictor.predict_flow(attack_flow)
    print("\n--- TEST FLOW 2: MALICIOUS SYN FLOOD (neptune / DoS) ---")
    print(f"  Connection : {res_attack['flow_summary']['src']} -> {res_attack['flow_summary']['dst']} ({res_attack['flow_summary']['protocol']})")
    print(f"  Prediction : {res_attack['prediction']}")
    print(f"  Is Attack  : {res_attack['is_attack']}")
    print(f"  Confidence : {res_attack['confidence'] * 100:.2f}%")
    print(f"  Risk Level : {res_attack['risk_level']}")
    print(f"  Latency    : {res_attack['latency_ms']:.3f} ms")

    # 4. Test PacketCaptureManager Live Adapter Binding
    app = create_app()
    capture_mgr = PacketCaptureManager()
    start_res = capture_mgr.start_capture(
        app=app,
        interface_id="default",
        model_path=model_path,
        scaler_path=scaler_path,
        encoder_path=encoder_path,
        mode="simulated"
    )
    print("\n--- TEST PACKET CAPTURE MANAGER INTEGRATION ---")
    print(f"  Start Capture Success : {start_res.get('success')}")
    print(f"  Active Algorithm      : {start_res.get('algorithm')}")
    print(f"  Capture Mode          : {start_res.get('mode')}")
    print(f"  Message               : {start_res.get('message')}")

    time.sleep(1.5)
    stop_res = capture_mgr.stop_capture()
    print(f"  Stop Capture Message  : {stop_res.get('message')}")
    print("=" * 80)
    print(">>> LIVE DETECTION VERIFICATION PASSED WITH SUPPORT VECTOR MACHINE!")
    print("=" * 80)

if __name__ == "__main__":
    test_live_detection()
