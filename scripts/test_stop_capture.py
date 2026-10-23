import sys
import os
sys.path.append(r"E:\ML")
from app import create_app
from api.live_detection_routes import _capture_manager
from database.init_db import LiveDetection

app = create_app()
with app.app_context():
    count = LiveDetection.query.count()
    print(f"Total LiveDetection rows in database: {count}")
    try:
        res = _capture_manager.stop_capture()
        print("stop_capture result:", res)
        eval_report = _capture_manager.logger.get_live_performance_evaluation(app=app)
        print("get_live_performance_evaluation total_flows:", eval_report.get("total_flows"))
        print("has_data:", eval_report.get("has_data"))
    except Exception as e:
        import traceback
        traceback.print_exc()
