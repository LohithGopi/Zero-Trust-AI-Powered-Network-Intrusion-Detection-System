import sys
sys.path.append(r"E:\ML")
from app import create_app
from api.live_detection_routes import _capture_manager
import json

app = create_app()
with app.app_context():
    eval_report = _capture_manager.logger.get_live_performance_evaluation(app=app)
    print("Keys in eval_report:")
    for k in sorted(eval_report.keys()):
        val = eval_report[k]
        if isinstance(val, (int, float, str, bool)):
            print(f"  {k}: {val}")
        elif isinstance(val, list):
            print(f"  {k}: list of length {len(val)}")
        elif isinstance(val, dict):
            print(f"  {k}: dict with keys {list(val.keys())}")
