import sys
import os
import time

sys.path.insert(0, r"E:\ML")
from app import create_app
from database.init_db import ModelHistory
from live_detection.flow_manager import NetworkFlow
from live_detection.live_predictor import LivePredictor
from live_detection.packet_capture import PacketCaptureManager

flask_app = create_app()

results = {}

with flask_app.app_context():
    models_db = ModelHistory.query.order_by(ModelHistory.id.asc()).all()
    models = [(m.algorithm, m.artifact_path) for m in models_db]

for algo_name, model_dir in models:
    mgr = PacketCaptureManager()
    mgr.app = None  # in-memory evaluation for instant throughput
    m_path = os.path.join(model_dir, "model.joblib")
    s_path = os.path.join(model_dir, "scaler.pkl")
    e_path = os.path.join(model_dir, "encoder.pkl")
    if not os.path.exists(e_path):
        e_path = os.path.join(model_dir, "label_encoder.pkl")
    
    mgr.predictor = LivePredictor(
        model_path=m_path,
        scaler_path=s_path,
        encoder_path=e_path if os.path.exists(e_path) else None
    )
    
    now = time.time()
    for i in range(1, 501):
        flow = NetworkFlow(
            src_ip=f"192.168.1.{10 + (i % 200)}",
            dst_ip=f"142.250.190.{1 + (i % 50)}",
            src_port=49152 + (i % 15000),
            dst_port=443 if i % 2 == 0 else 80,
            protocol="TCP",
            start_time=now - 0.5,
            last_time=now,
            fwd_packets=5,
            bwd_packets=4,
            fwd_bytes=512,
            bwd_bytes=1024,
            ground_truth="Normal"
        )
        mgr._classify_and_log(flow)
        
    stats = mgr.logger.get_live_stats()
    results[algo_name] = stats

print("\n" + "=" * 95)
print(">>> VERIFIED LIVE DETECTION FALSE POSITIVE (FP) HIERARCHY OVER 500 FLOWS <<<")
print("=" * 95)
for name, s in results.items():
    tot = s["total_flows"]
    fp = s["false_positives"]
    fpr = s["false_positive_rate"]
    norm = s["normal_flows"]
    atk = s.get("attack_flows", 0)
    print(f"Model: {name:24s} | Total: {tot:3d} | False Positives (FP): {fp:3d} ({fpr:>6s}) | Normal: {norm:3d} | Threats: {atk}")
print("=" * 95 + "\n")
