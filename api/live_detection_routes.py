import os
import glob
from flask import Blueprint, request, jsonify, Response, current_app, g
from config import Config
from security.zero_trust import jwt_required, require_role
from database.init_db import db, ModelHistory
from live_detection.packet_capture import (
    PacketCaptureManager,
    get_available_interfaces,
    check_npcap_capability
)
from utils.logger import log_audit_event, logger

live_detection_bp = Blueprint("live_detection", __name__)

# Singleton manager instance for maintaining capture lifecycle
_capture_manager = PacketCaptureManager()


@live_detection_bp.route("/api/live-detection/interfaces", methods=["GET"])
@jwt_required
@require_role(["Admin", "Analyst"])
def get_interfaces_api():
    """Enumerate network adapters and report packet capture capability."""
    interfaces = get_available_interfaces()
    npcap_status = check_npcap_capability()
    return jsonify({
        "interfaces": interfaces,
        "npcap": npcap_status
    }), 200


@live_detection_bp.route("/api/live-detection/models", methods=["GET"])
@jwt_required
@require_role(["Admin", "Analyst"])
def get_compatible_models_api():
    """Return all trained models compatible with live flow classification."""
    import json
    available_models = []

    # Retrieve all trained models registered in ModelHistory
    all_mh = ModelHistory.query.order_by(ModelHistory.trained_at.desc()).all()

    for m in all_mh:
        artifact_dir = m.artifact_path or ""
        if artifact_dir and os.path.isdir(artifact_dir):
            model_file = os.path.join(artifact_dir, "model.joblib")
            if not os.path.exists(model_file):
                continue
            scaler_file = os.path.join(artifact_dir, "scaler.pkl")
            encoder_file = os.path.join(artifact_dir, "encoder.pkl")
            if not os.path.exists(encoder_file):
                encoder_file = os.path.join(artifact_dir, "label_encoder.pkl")

            dataset_name = m.dataset_name or ""
            dataset_type = "CIC-IDS2017"
            features = 22

            meta_file = os.path.join(artifact_dir, "training_metadata.json")
            algo_name = m.algorithm or "Neural Network"
            if os.path.exists(meta_file):
                try:
                    with open(meta_file, "r", encoding="utf-8") as f:
                        meta = json.load(f)
                        dataset_type = meta.get("dataset_type", dataset_type)
                        algo_name = meta.get("algorithm", algo_name)
                except Exception:
                    pass

            if "unsw" in dataset_name.lower() or "unsw" in dataset_type.lower():
                dataset_type = "UNSW-NB15"
                features = 15
            elif "nsl" in dataset_name.lower() or "nsl" in dataset_type.lower():
                dataset_type = "NSL-KDD"
                features = 19
            else:
                dataset_type = "CIC-IDS2017"
                features = 22

            if os.path.exists(scaler_file):
                try:
                    import joblib
                    sc = joblib.load(scaler_file)
                    features = getattr(sc, "n_features_in_", features)
                except Exception:
                    pass

            is_compat = features in (15, 19, 22)
            if os.path.exists(model_file) and os.path.exists(scaler_file):
                available_models.append({
                    "id": f"history_{m.id}",
                    "raw_id": m.id,
                    "name": f"{algo_name} ({dataset_type}) — Acc: {round(m.accuracy * 100, 1)}%",
                    "algorithm": algo_name,
                    "model_version": m.model_version or f"v{m.id}",
                    "dataset_name": dataset_name,
                    "dataset_type": dataset_type,
                    "features": features,
                    "accuracy": round(m.accuracy * 100, 2),
                    "f1_score": round(m.f1_score * 100, 2),
                    "compatible": is_compat,
                    "trained_at": m.trained_at.strftime("%Y-%m-%d %H:%M:%S") if m.trained_at else "N/A",
                    "model_path": os.path.abspath(model_file),
                    "scaler_path": os.path.abspath(scaler_file),
                    "encoder_path": os.path.abspath(encoder_file) if os.path.exists(encoder_file) else None,
                    "is_active": bool(m.is_active),
                    "is_default": bool(m.is_active)
                })

    # Return active_model ONLY if an explicitly active model exists; do NOT default to available_models[0] before training
    active_model = next((m for m in available_models if m.get("is_active")), None)

    return jsonify({
        "models": available_models,
        "active_model": active_model,
        "has_trained_model": len(available_models) > 0,
        "message": f"{len(available_models)} compatible trained model(s) available for selection." if available_models else "No model trained yet. Please train a model based on your dataset first."
    }), 200


@live_detection_bp.route("/api/live-detection/models", methods=["DELETE"])
@live_detection_bp.route("/api/live-detection/models/remove", methods=["POST", "DELETE"])
@jwt_required
@require_role(["Admin", "Analyst"])
def remove_detection_model_api():
    """Remove the active detection model (or all trained models) and reset active model state to null."""
    import shutil
    from config import Config
    from training.train_model import training_status

    data = request.get_json(silent=True) or {}
    model_id = data.get("model_id") or request.args.get("model_id") or "all"

    # Stop active live capture if running
    if _capture_manager.is_running:
        _capture_manager.stop_capture()
    _capture_manager.predictor = None

    removed_name = "All trained models"
    try:
        target_int_id = None
        if isinstance(model_id, int):
            target_int_id = model_id
        elif isinstance(model_id, str):
            clean_str = model_id.replace("history_", "").strip()
            if clean_str.isdigit():
                target_int_id = int(clean_str)

        if target_int_id is not None:
            mh = ModelHistory.query.get(target_int_id)
            if mh:
                removed_name = mh.model_name or f"Model #{target_int_id}"
                artifact_dir = mh.artifact_path
                db.session.delete(mh)
                db.session.commit()
                if artifact_dir and os.path.isdir(artifact_dir) and "test_run" not in artifact_dir:
                    shutil.rmtree(artifact_dir, ignore_errors=True)
            else:
                removed_name = f"Model #{target_int_id}"

            # If other models remain, ensure an active model is set
            remaining = ModelHistory.query.order_by(ModelHistory.trained_at.desc()).all()
            if remaining and not any(m.is_active for m in remaining):
                remaining[0].is_active = True
                db.session.commit()
        elif str(model_id).lower() == "all":
            # Remove all trained models
            all_mh = ModelHistory.query.all()
            for mh in all_mh:
                if mh.artifact_path and os.path.isdir(mh.artifact_path) and "test_run" not in mh.artifact_path:
                    shutil.rmtree(mh.artifact_path, ignore_errors=True)
            ModelHistory.query.delete()
            db.session.commit()

        # If no models remain in ModelHistory, clean global model artifacts & reset training status
        remaining_count = ModelHistory.query.count()
        if remaining_count == 0:
            for fname in ("model.joblib", "scaler.pkl", "label_encoder.pkl", "encoder.pkl"):
                fpath = os.path.join(Config.MODEL_DIR, fname)
                if os.path.exists(fpath):
                    try:
                        os.remove(fpath)
                    except Exception:
                        pass

            training_status["run_id"] = None
            training_status["dataset_name"] = None
            training_status["is_training"] = False
            training_status["current_epoch"] = 0
            training_status["accuracy"] = 0.0
            training_status["loss"] = 0.0
            training_status["val_accuracy"] = 0.0
            training_status["val_loss"] = 0.0
            training_status["epoch_history"] = []
            training_status["status"] = "Ready"
            training_status["message"] = "Active detection model removed. No model trained."

        log_audit_event(
            action="MODEL_REMOVED",
            status="SUCCESS",
            user_id=g.user.get("user_id") if g.user else None,
            username=g.user.get("username") if g.user else "admin",
            ip_address=request.remote_addr,
            details=f"Removed detection model: {removed_name}"
        )

        # Return updated model list
        resp, _ = get_compatible_models_api()
        resp_data = resp.get_json()
        resp_data["success"] = True
        resp_data["removed"] = removed_name
        resp_data["message"] = (
            f"Removed '{removed_name}'. Active detection model is now null (no model trained)."
            if not resp_data.get("active_model")
            else f"Removed '{removed_name}'."
        )
        return jsonify(resp_data), 200

    except Exception as e:
        logger.error(f"Error removing detection model: {e}")
        return jsonify({"success": False, "error": f"Failed to remove model: {str(e)}"}), 500



@live_detection_bp.route("/api/live-detection/start", methods=["POST"])
@jwt_required
@require_role(["Admin", "Analyst"])
def start_capture_api():
    """Start passive live traffic monitoring on the chosen network interface."""
    data = request.get_json() or {}
    interface_id = data.get("interface_id", "default")
    model_path = data.get("model_path")
    scaler_path = data.get("scaler_path")
    encoder_path = data.get("encoder_path")
    mode = data.get("mode", "hardware")

    model_id = data.get("model_id")
    if model_id:
        raw_id = None
        if isinstance(model_id, int):
            raw_id = model_id
        elif isinstance(model_id, str):
            clean = model_id.replace("history_", "").strip()
            if clean.isdigit():
                raw_id = int(clean)
        if raw_id:
            mh = ModelHistory.query.get(raw_id)
            if mh and mh.artifact_path:
                cand_m = os.path.join(mh.artifact_path, "model.joblib")
                cand_s = os.path.join(mh.artifact_path, "scaler.pkl")
                cand_e = os.path.join(mh.artifact_path, "encoder.pkl")
                if not os.path.exists(cand_e):
                    cand_e = os.path.join(mh.artifact_path, "label_encoder.pkl")
                if os.path.exists(cand_m) and os.path.exists(cand_s):
                    model_path = os.path.abspath(cand_m)
                    scaler_path = os.path.abspath(cand_s)
                    encoder_path = os.path.abspath(cand_e) if os.path.exists(cand_e) else None

    # If no model_path specified, look up explicitly active model
    if not model_path:
        active_mh = ModelHistory.query.filter_by(is_active=True).first()
        if not active_mh:
            return jsonify({
                "success": False,
                "error": "No active detection model trained or activated. Please navigate to Model Training and train or activate a model first."
            }), 400
        latest_mh = active_mh
        if latest_mh and latest_mh.artifact_path:
            cand_m = os.path.join(latest_mh.artifact_path, "model.joblib")
            cand_s = os.path.join(latest_mh.artifact_path, "scaler.pkl")
            cand_e = os.path.join(latest_mh.artifact_path, "encoder.pkl")
            if not os.path.exists(cand_e):
                cand_e = os.path.join(latest_mh.artifact_path, "label_encoder.pkl")
            if os.path.exists(cand_m) and os.path.exists(cand_s):
                model_path = os.path.abspath(cand_m)
                scaler_path = os.path.abspath(cand_s)
                encoder_path = os.path.abspath(cand_e) if os.path.exists(cand_e) else None

    if not model_path or not os.path.exists(model_path):
        return jsonify({
            "success": False,
            "error": "No detection model trained. Please train a model based on your dataset first in the Model Training section."
        }), 400

    app = current_app._get_current_object()
    result = _capture_manager.start_capture(
        app=app,
        interface_id=interface_id,
        model_path=model_path,
        scaler_path=scaler_path,
        encoder_path=encoder_path,
        mode=mode,
        flow_boundary=data.get("flow_boundary") or data.get("packet_boundary"),
        packet_boundary=data.get("flow_boundary") or data.get("packet_boundary")
    )

    if not result.get("success"):
        return jsonify(result), 400

    log_audit_event(
        action="LIVE_CAPTURE_START",
        status="SUCCESS",
        user_id=g.user.get("user_id"),
        username=g.user.get("username"),
        ip_address=request.remote_addr,
        details=f"Live capture initiated on interface {interface_id} using {result.get('dataset_type')}"
    )

    return jsonify(result), 200


@live_detection_bp.route("/api/live-detection/stop", methods=["POST"])
@jwt_required
@require_role(["Admin", "Analyst"])
def stop_capture_api():
    """Stop active live packet capture and generate session performance evaluation."""
    try:
        result = _capture_manager.stop_capture()
    except Exception as e:
        logger.error(f"Error stopping capture manager: {e}")
        result = {"success": True, "message": f"Capture stopped: {str(e)}"}

    try:
        app = current_app._get_current_object()
        eval_report = _capture_manager.logger.get_live_performance_evaluation(app=app)
    except Exception as e:
        logger.error(f"Error generating session evaluation: {e}")
        eval_report = {"has_data": False, "total_flows": 0, "error": str(e)}

    result["evaluation"] = eval_report

    try:
        log_audit_event(
            action="LIVE_CAPTURE_STOP",
            status="SUCCESS",
            user_id=g.user.get("user_id") if hasattr(g, 'user') and g.user else None,
            username=g.user.get("username") if hasattr(g, 'user') and g.user else "analyst",
            ip_address=request.remote_addr,
            details=f"Live capture stopped. Session evaluation computed for {eval_report.get('total_flows', 0)} flows."
        )
    except Exception as e:
        logger.warning(f"Error logging capture stop audit: {e}")

    return jsonify(result), 200


@live_detection_bp.route("/api/live-detection/evaluation", methods=["GET"])
@jwt_required
@require_role(["Admin", "Analyst"])
def get_live_evaluation_api():
    """Compute and return comprehensive Performance Evaluation report based on live network traffic."""
    limit_arg = request.args.get("limit")
    limit = int(limit_arg) if limit_arg and limit_arg.isdigit() else None
    app = current_app._get_current_object()
    eval_report = _capture_manager.logger.get_live_performance_evaluation(app=app, limit=limit)
    return jsonify(eval_report), 200


@live_detection_bp.route("/api/live-detection/status", methods=["GET"])
@jwt_required
@require_role(["Admin", "Analyst"])
def get_status_api():
    """Poll current packet capture engine status."""
    status = _capture_manager.get_status()
    stats = _capture_manager.logger.get_live_stats()
    return jsonify({
        "status": status,
        "stats": stats
    }), 200


@live_detection_bp.route("/api/live-detection/traffic", methods=["GET"])
@jwt_required
@require_role(["Admin", "Analyst"])
def get_traffic_feed_api():
    """Poll recent analyzed network flows and security alerts."""
    limit = int(request.args.get("limit", 50))
    recent_detections = _capture_manager.logger.get_recent_detections(limit=limit)
    recent_alerts = _capture_manager.logger.get_recent_alerts(limit=20)
    live_stats = _capture_manager.logger.get_live_stats()

    return jsonify({
        "detections": recent_detections,
        "alerts": recent_alerts,
        "stats": live_stats,
        "is_running": _capture_manager.is_running
    }), 200


@live_detection_bp.route("/api/live-detection/replay", methods=["POST"])
@jwt_required
@require_role(["Admin", "Analyst"])
def replay_traffic_api():
    """Replay controlled test packets for pipeline functional verification."""
    data = request.get_json() or {}
    count = int(data.get("count", 10))

    app = current_app._get_current_object()
    result = _capture_manager.replay_test_traffic(app=app, count=count)

    if not result.get("success"):
        return jsonify(result), 400

    log_audit_event(
        action="LIVE_REPLAY_TEST",
        status="SUCCESS",
        user_id=g.user.get("user_id"),
        username=g.user.get("username"),
        ip_address=request.remote_addr,
        details=f"Controlled test replay executed: {count} flow batches."
    )

    return jsonify(result), 200


@live_detection_bp.route("/api/live-detection/reset", methods=["POST"])
@jwt_required
@require_role(["Admin", "Analyst"])
def reset_stats_api():
    """Reset live traffic counters and purge detection memory buffers to 0."""
    _capture_manager.logger.reset_stats()
    try:
        from database.init_db import LiveDetection
        LiveDetection.query.delete()
        db.session.commit()
    except Exception as e:
        logger.warning(f"Error purging LiveDetection DB rows on reset: {e}")
    return jsonify({"success": True, "message": "Monitored packets and flows reset to zero."}), 200


@live_detection_bp.route("/api/live-detection/ingest-csv", methods=["POST"])
@jwt_required
@require_role(["Admin", "Analyst"])
def ingest_csv_api():
    """Ingest a CSV dataset into the live detection pipeline and detect attacks."""
    import os
    from werkzeug.utils import secure_filename
    from config import Config
    from database.init_db import DatasetHistory

    count = int(request.form.get("count", 50))
    app = current_app._get_current_object()

    filepath = None
    if 'file' in request.files and request.files['file'].filename != '':
        file = request.files['file']
        if not file.filename.endswith('.csv'):
            return jsonify({"error": "Only CSV dataset files are supported."}), 400
        filename = secure_filename(file.filename)
        os.makedirs(Config.DATASET_RAW_DIR, exist_ok=True)
        filepath = os.path.join(Config.DATASET_RAW_DIR, filename)
        file.save(filepath)
    else:
        dataset_id = request.form.get("dataset_id") or (request.get_json(silent=True) or {}).get("dataset_id")
        if dataset_id:
            ds = DatasetHistory.query.get(dataset_id)
            if ds and ds.filepath and os.path.exists(ds.filepath):
                filepath = ds.filepath

    if not filepath or not os.path.exists(filepath):
        # Fallback to the latest dataset in DatasetHistory
        latest_ds = DatasetHistory.query.order_by(DatasetHistory.upload_date.desc()).first()
        if latest_ds and latest_ds.filepath and os.path.exists(latest_ds.filepath):
            filepath = latest_ds.filepath

    if not filepath or not os.path.exists(filepath):
        return jsonify({"error": "No CSV dataset found. Please upload a CSV file."}), 400

    result = _capture_manager.ingest_csv_traffic(app=app, filepath=filepath, count=count)
    if not result.get("success"):
        return jsonify(result), 400

    log_audit_event(
        action="LIVE_CSV_INGESTION",
        status="SUCCESS",
        user_id=g.user.get("user_id"),
        username=g.user.get("username"),
        ip_address=request.remote_addr,
        details=f"Live CSV detection executed: {result.get('processed', 0)} flows."
    )

    return jsonify(result), 200


@live_detection_bp.route("/api/live-detection/export", methods=["GET"])
@jwt_required
@require_role(["Admin", "Analyst"])
def export_detections_csv_api():
    """Export live detection history to downloadable CSV."""
    app = current_app._get_current_object()
    csv_data = _capture_manager.logger.export_csv(app=app, limit=2000)

    log_audit_event(
        action="LIVE_DETECTION_EXPORT",
        status="SUCCESS",
        user_id=g.user.get("user_id"),
        username=g.user.get("username"),
        ip_address=request.remote_addr,
        details="Exported live detection logs to CSV."
    )

    return Response(
        csv_data,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=live_intrusion_detections.csv"}
    )
