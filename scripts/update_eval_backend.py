# Update backend routes and detection_logger for limit=None handling

# 1. Update api/live_detection_routes.py
routes_path = r"E:\ML\api\live_detection_routes.py"
with open(routes_path, "r", encoding="utf-8") as f:
    r_content = f.read()

r_norm = r_content.replace("\r\n", "\n")
target_r = """@live_detection_bp.route("/api/live-detection/evaluation", methods=["GET"])
@jwt_required
@require_role(["Admin", "Analyst"])
def get_live_evaluation_api():
    \"\"\"Compute and return comprehensive Performance Evaluation report based on live network traffic.\"\"\"
    limit = int(request.args.get("limit", 500))
    app = current_app._get_current_object()
    eval_report = _capture_manager.logger.get_live_performance_evaluation(app=app, limit=limit)
    return jsonify(eval_report), 200"""

repl_r = """@live_detection_bp.route("/api/live-detection/evaluation", methods=["GET"])
@jwt_required
@require_role(["Admin", "Analyst"])
def get_live_evaluation_api():
    \"\"\"Compute and return comprehensive Performance Evaluation report based on live network traffic.\"\"\"
    limit_arg = request.args.get("limit")
    limit = int(limit_arg) if limit_arg and limit_arg.isdigit() else None
    app = current_app._get_current_object()
    eval_report = _capture_manager.logger.get_live_performance_evaluation(app=app, limit=limit)
    return jsonify(eval_report), 200"""

if target_r in r_norm:
    r_norm = r_norm.replace(target_r, repl_r)
    with open(routes_path, "w", encoding="utf-8") as f:
        f.write(r_norm)
    print("SUCCESS: live_detection_routes.py updated.")
else:
    print("WARNING: target not found in live_detection_routes.py")

# 2. Update live_detection/detection_logger.py
logger_path = r"E:\ML\live_detection\detection_logger.py"
with open(logger_path, "r", encoding="utf-8") as f:
    l_content = f.read()

l_norm = l_content.replace("\r\n", "\n")
target_l = """    def get_live_performance_evaluation(self, app=None, limit=500) -> Dict[str, Any]:
        \"\"\"Compute empirical intrusion detection performance evaluation based on actual live traffic records.\"\"\"
        max_inspection = max(10, int(limit))"""

repl_l = """    def get_live_performance_evaluation(self, app=None, limit=None) -> Dict[str, Any]:
        \"\"\"Compute empirical intrusion detection performance evaluation based on actual live traffic records.\"\"\"
        max_inspection = max(10, int(limit)) if limit else 50000"""

if target_l in l_norm:
    l_norm = l_norm.replace(target_l, repl_l)
    with open(logger_path, "w", encoding="utf-8") as f:
        f.write(l_norm)
    print("SUCCESS: detection_logger.py updated.")
else:
    print("WARNING: target not found in detection_logger.py")
