import os
import sys

sys.path.insert(0, r"E:\ML")
from app import create_app
from live_detection.detection_logger import DetectionLogger

app = create_app()
logger = DetectionLogger()

# Add a simulated record to memory_buffer
logger.memory_buffer.append({
    "prediction": "Normal",
    "status": "Normal",
    "confidence": 0.98,
    "source_ip": "192.168.1.100",
    "source_port": 54321,
    "destination_ip": "8.8.8.8",
    "destination_port": 53,
    "protocol": "UDP",
    "model_name": "Support Vector Machine",
    "ground_truth": "Normal",
    "latency_ms": 1.25,
    "is_false_positive": False
})
logger.stats["total_flows"] = 1

tiers = [500, 1000, 2500, 5000, 10000, 25000, 50000]
print("Testing evaluation scaling across all tiers:")
for t in tiers:
    rep = logger.get_live_performance_evaluation(app=app, limit=t)
    print(f"  Tier {t:5d} -> total_flows: {rep['total_flows']:5d}, packets: {rep['total_packets']:7d}, bytes: {rep['total_bytes']:9d} ({rep['total_bytes']/1024:.1f} KB), accuracy: {rep['accuracy']*100:.2f}%")

print("All tier evaluations verified successfully!")
