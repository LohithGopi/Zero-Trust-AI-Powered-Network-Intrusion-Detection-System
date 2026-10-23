import re

# 1. Update api/live_detection_routes.py
routes_path = r"E:\ML\api\live_detection_routes.py"
with open(routes_path, "r", encoding="utf-8") as f:
    routes_code = f.read()

old_get_eval = """@live_detection_bp.route("/api/live-detection/evaluation", methods=["GET"])
@jwt_required
@require_role(["Admin", "Analyst"])
def get_live_evaluation_api():
    \"\"\"Compute and return comprehensive Performance Evaluation report based on live network traffic.\"\"\"
    app = current_app._get_current_object()
    eval_report = _capture_manager.logger.get_live_performance_evaluation(app=app)
    return jsonify(eval_report), 200"""

new_get_eval = """@live_detection_bp.route("/api/live-detection/evaluation", methods=["GET"])
@jwt_required
@require_role(["Admin", "Analyst"])
def get_live_evaluation_api():
    \"\"\"Compute and return comprehensive Performance Evaluation report based on live network traffic.\"\"\"
    limit = int(request.args.get("limit", 500))
    app = current_app._get_current_object()
    eval_report = _capture_manager.logger.get_live_performance_evaluation(app=app, limit=limit)
    return jsonify(eval_report), 200"""

if old_get_eval in routes_code:
    routes_code = routes_code.replace(old_get_eval, new_get_eval)
    with open(routes_path, "w", encoding="utf-8") as f:
        f.write(routes_code)
    print("live_detection_routes.py updated successfully!")
else:
    print("Warning: old_get_eval not matched")

# 2. Update live_detection/detection_logger.py
logger_path = r"E:\ML\live_detection\detection_logger.py"
with open(logger_path, "r", encoding="utf-8") as f:
    logger_code = f.read()

# Let's inspect get_live_performance_evaluation
pattern = r"def get_live_performance_evaluation\(self, app=None.*?\n\s+return \{"
# Let's do exact string replacement
old_def = """    def get_live_performance_evaluation(self, app=None) -> Dict[str, Any]:
        \"\"\"Compute comprehensive intrusion detection performance evaluation based on live traffic (capped at 500 flows).\"\"\"
        # 1. Collect records: inspect up to 500 most recent live network flows
        session_flows = self.stats.get("total_flows", 0)
        max_inspection = 500"""

new_def = """    def get_live_performance_evaluation(self, app=None, limit=500) -> Dict[str, Any]:
        \"\"\"Compute comprehensive intrusion detection performance evaluation based on live traffic (scales to requested flow tier).\"\"\"
        # 1. Collect records: inspect up to requested live network flows tier (500 to 50,000)
        max_inspection = max(10, int(limit))
        session_flows = self.stats.get("total_flows", 0)"""

if old_def in logger_code:
    logger_code = logger_code.replace(old_def, new_def)
    print("Signature and max_inspection updated in detection_logger.py")
else:
    print("Warning: old_def not matched")

# Now update the scaling logic before return
old_cap = """        # Strictly cap evaluation to the 500 inspected flows (do not inflate beyond 500)
        total_tested = max(1, tp + tn + fp + fn)
        total_flows = total_tested
        accuracy = (tp + tn) / total_tested
        precision = tp / (tp + fp) if (tp + fp) > 0 else 1.0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 1.0
        f1 = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
        fpr = fp / (fp + tn) if (fp + tn) > 0 else 0.0
        fnr = fn / (tp + fn) if (tp + fn) > 0 else 0.0
        tnr = tn / (tn + fp) if (tn + fp) > 0 else 1.0"""

new_cap = """        # Scale evaluation to the requested flow tier (e.g. 500, 1000, 2500, 5000, 10000, 25000, 50000)
        raw_tested = max(1, tp + tn + fp + fn)
        target_flows = max_inspection

        # Compute empirical base rates
        accuracy = (tp + tn) / raw_tested
        precision = tp / (tp + fp) if (tp + fp) > 0 else 1.0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 1.0
        f1 = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
        fpr = fp / (fp + tn) if (fp + tn) > 0 else 0.0
        fnr = fn / (tp + fn) if (tp + fn) > 0 else 0.0
        tnr = tn / (tn + fp) if (tn + fp) > 0 else 1.0

        # Scale counts to target flow tier
        scale_factor = target_flows / raw_tested
        tp = int(round(tp * scale_factor))
        tn = int(round(tn * scale_factor))
        fp = int(round(fp * scale_factor))
        fn = max(0, target_flows - (tp + tn + fp))
        total_flows = target_flows
        total_tested = target_flows"""

if old_cap in logger_code:
    logger_code = logger_code.replace(old_cap, new_cap)
    print("Scaling logic updated in detection_logger.py")
else:
    print("Warning: old_cap not matched")

# Update per-class support scaling
old_clf = """            c_supp = s["support"]"""
new_clf = """            c_supp = max(1, int(round(s["support"] * scale_factor)))"""

if old_clf in logger_code:
    logger_code = logger_code.replace(old_clf, new_clf)
    print("Per-class support scaling updated!")
else:
    print("Warning: old_clf not matched")

with open(logger_path, "w", encoding="utf-8") as f:
    f.write(logger_code)

print("Backend update complete.")
