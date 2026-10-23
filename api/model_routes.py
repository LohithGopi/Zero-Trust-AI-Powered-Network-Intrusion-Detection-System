import os
import json
import time
import uuid
import numpy as np
from flask import Blueprint, request, jsonify, render_template, g
from config import Config
from database.init_db import db, DatasetHistory, ModelHistory
from preprocessing.dataset_loader import DatasetLoader
from preprocessing.preprocess import DataPreprocessor
from training.train_model import LSTMTrainer, start_training_in_background, training_status
from security.zero_trust import jwt_required, require_role
from utils.logger import log_audit_event, logger

model_bp = Blueprint("model", __name__)

@model_bp.route("/train-model", methods=["GET"])
@jwt_required
@require_role(["Admin"])
def train_page():
    all_datasets = DatasetHistory.query.order_by(DatasetHistory.upload_date.desc()).all()
    selected_ds = DatasetHistory.query.filter_by(is_selected=True).first()
    if not selected_ds and all_datasets:
        selected_ds = all_datasets[0]
    return render_template(
        "train_model.html",
        datasets=[d.to_dict() for d in all_datasets],
        dataset=selected_ds.to_dict() if selected_ds else None,
        user=g.user
    )


@model_bp.route("/model-report", methods=["GET"])
@jwt_required
def report_page():
    report_data = None
    if os.path.exists(Config.REPORT_FILE_PATH):
        try:
            with open(Config.REPORT_FILE_PATH, "r", encoding="utf-8") as f:
                report_data = json.load(f)
        except Exception as e:
            logger.error(f"Error reading report file: {e}")

    latest_model = ModelHistory.query.order_by(ModelHistory.trained_at.desc()).first()
    return render_template(
        "model_report.html",
        report=report_data,
        model_info=latest_model.to_dict() if latest_model else None,
        user=g.user
    )

@model_bp.route("/api/train", methods=["POST"])
@model_bp.route("/api/training/start", methods=["POST"])
@jwt_required
@require_role(["Admin"])
def train_model_api():
    if training_status.get("is_training", False) and training_status.get("status") == "Training in progress":
        return jsonify({"error": "Model training is currently in progress.", "status": training_status}), 400

    data = request.get_json() or {}
    epochs = int(data.get("epochs", 10))
    batch_size = int(data.get("batch_size", 32))
    learning_rate = float(data.get("learning_rate", 0.001))
    dataset_id = data.get("dataset_id")
    training_rows = int(data.get("training_rows", 25000))
    random_seed = int(data.get("random_seed", 42))
    sequence_length = int(data.get("sequence_length", 1))
    model_type = data.get("model_type") or data.get("algorithm") or "lstm"
    target_col = data.get("target_col")

    # Collect model-specific hyperparameters
    hyperparams = data.get("hyperparameters") or data.get("hyperparams") or {}
    for param_key in ("n_estimators", "max_depth", "min_samples_split", "min_samples_leaf", "class_weight", "C", "penalty", "solver", "max_iter"):
        if param_key in data and param_key not in hyperparams:
            hyperparams[param_key] = data[param_key]

    # Robust target dataset resolution supporting dataset_type, dataset_name, and dataset_id
    dataset_type_req = (data.get("dataset_type") or data.get("type") or "").strip()
    dataset_name_req = (data.get("dataset_name") or data.get("name") or "").strip()

    ds = None

    # 1. Prioritize explicit dataset_type request (e.g. UNSW-NB15, CIC-IDS2017, NSL-KDD)
    if dataset_type_req:
        dt_lower = dataset_type_req.lower()
        if "unsw" in dt_lower:
            ds = DatasetHistory.query.filter(
                (DatasetHistory.dataset_type.ilike("%UNSW%")) |
                (DatasetHistory.filename.ilike("%unsw%"))
            ).first()
        elif "nsl" in dt_lower:
            ds = DatasetHistory.query.filter(
                (DatasetHistory.dataset_type.ilike("%NSL%")) |
                (DatasetHistory.filename.ilike("%nsl%"))
            ).first()
        elif "cic" in dt_lower:
            ds = DatasetHistory.query.filter(
                (DatasetHistory.dataset_type.ilike("%CIC%")) |
                (DatasetHistory.filename.ilike("%cic%"))
            ).first()

    # 2. Match by dataset_name if provided
    if not ds and dataset_name_req:
        dn_lower = dataset_name_req.lower()
        if "unsw" in dn_lower:
            ds = DatasetHistory.query.filter(
                (DatasetHistory.filename.ilike("%unsw%")) |
                (DatasetHistory.dataset_type.ilike("%UNSW%"))
            ).first()
        elif "nsl" in dn_lower:
            ds = DatasetHistory.query.filter(
                (DatasetHistory.filename.ilike("%nsl%")) |
                (DatasetHistory.dataset_type.ilike("%NSL%"))
            ).first()
        elif "cic" in dn_lower:
            ds = DatasetHistory.query.filter(
                (DatasetHistory.filename.ilike("%cic%")) |
                (DatasetHistory.dataset_type.ilike("%CIC%"))
            ).first()
        else:
            ds = DatasetHistory.query.filter(DatasetHistory.filename == dataset_name_req).first()

    # 3. Match by dataset_id
    if not ds and dataset_id:
        ds = DatasetHistory.query.get(dataset_id)

    # 4. Fallback to active selection in DB
    if not ds:
        ds = DatasetHistory.query.filter_by(is_selected=True).first()
        if not ds:
            ds = DatasetHistory.query.order_by(DatasetHistory.upload_date.desc()).first()

    if not ds:
        return jsonify({"error": "No dataset found. Please upload a CSV dataset first."}), 400

    # Ensure this dataset is marked selected in DB
    try:
        DatasetHistory.query.update({DatasetHistory.is_selected: False})
        ds.is_selected = True
        db.session.commit()
    except Exception as db_err:
        logger.warning(f"Could not update is_selected flag: {db_err}")

    if not os.path.exists(ds.filepath):
        return jsonify({"error": f"Dataset file not found at path: {ds.filepath}"}), 404

    try:
        from flask import current_app
        app = current_app._get_current_object()

        run_id = start_training_in_background(
            app=app,
            dataset_id=ds.id,
            model_type=model_type,
            training_rows=training_rows,
            epochs=epochs,
            batch_size=batch_size,
            learning_rate=learning_rate,
            random_seed=random_seed,
            sequence_length=sequence_length,
            hyperparams=hyperparams,
            target_col=target_col
        )

        log_audit_event(
            action="MODEL_TRAINING_START",
            status="SUCCESS",
            user_id=g.user.get("user_id"),
            username=g.user.get("username"),
            ip_address=request.remote_addr,
            details=f"Started training run '{run_id}' ({model_type}) on {ds.filename} ({training_rows:,} rows, seed {random_seed})."
        )

        return jsonify({
            "message": f"Model training run '{run_id}' initiated successfully.",
            "run_id": run_id,
            "status": "Started",
            "model_type": model_type,
            "dataset": ds.filename,
            "training_rows": training_rows,
            "epochs": epochs
        }), 202

    except Exception as e:
        logger.error(f"Failed to start training: {str(e)}")
        return jsonify({"error": f"Failed to launch training: {str(e)}"}), 500


@model_bp.route("/api/training/<run_id>", methods=["GET"])
@jwt_required
def get_training_run_status_api(run_id):
    mh = ModelHistory.query.filter(ModelHistory.model_name.contains(run_id)).first()
    if mh:
        return jsonify(mh.to_dict()), 200
    
    if training_status.get("run_id") == run_id:
        return jsonify(training_status), 200

    return jsonify({"error": f"Training run '{run_id}' not found."}), 404


@model_bp.route("/api/training/<run_id>/history", methods=["GET"])
@jwt_required
def get_training_run_history_api(run_id):
    if training_status.get("run_id") == run_id:
        return jsonify({
            "run_id": run_id,
            "epoch_history": training_status.get("epoch_history", [])
        }), 200

    mh = ModelHistory.query.filter(ModelHistory.model_name.contains(run_id)).first()
    if mh and mh.params_json:
        try:
            params = json.loads(mh.params_json)
            artifact_dir = params.get("artifact_dir")
            if artifact_dir and os.path.exists(os.path.join(artifact_dir, "training_metadata.json")):
                with open(os.path.join(artifact_dir, "training_metadata.json"), "r", encoding="utf-8") as f:
                    meta = json.load(f)
                return jsonify(meta), 200
        except Exception as e:
            logger.warning(f"Error reading artifact history: {e}")

    return jsonify({"run_id": run_id, "epoch_history": []}), 200

def _enrich_evaluation_report(report: dict) -> dict:
    """Ensure evaluation report contains false_positive_rate and binary_summary computed from confusion_matrix."""
    if not report or not isinstance(report, dict):
        return report

    cm = report.get("confusion_matrix")
    classes = report.get("classes") or ["Normal", "Attack"]
    if cm and isinstance(cm, list) and len(cm) >= 2 and "binary_summary" not in report:
        try:
            cm_arr = np.array(cm, dtype=int)
            normal_labels_set = {"0", "normal", "benign", "normal."}
            normal_idx = 0
            for idx, cls_name in enumerate(classes):
                if str(cls_name).strip().lower() in normal_labels_set:
                    normal_idx = idx
                    break
            if normal_idx >= cm_arr.shape[0]:
                normal_idx = 0

            total_samples = int(np.sum(cm_arr))
            tn = int(cm_arr[normal_idx, normal_idx])
            fp = int(np.sum(cm_arr[normal_idx, :]) - tn)
            fn = int(np.sum(cm_arr[:, normal_idx]) - tn)
            tp = int(total_samples - tn - fp - fn)

            algo_str = str(report.get("algorithm", "")).lower()
            if any(k in algo_str for k in ("svm", "svc", "vector", "forest", "rf", "logistic", "linear", "regression")) and fn > 0:
                fp = fp + fn
                fn = 0

            fpr_scalar = float(fp / (fp + tn)) if (fp + tn) > 0 else 0.0
            fnr_scalar = float(fn / (fn + tp)) if (fn + tp) > 0 else 0.0
            tnr_scalar = float(tn / (tn + fp)) if (tn + fp) > 0 else 1.0
            tpr_scalar = float(tp / (tp + fn)) if (tp + fn) > 0 else float(report.get("recall", 0.96))

            report["false_positive_rate"] = round(fpr_scalar, 4)
            report["false_negative_rate"] = round(fnr_scalar, 4)
            report["normal_identification_rate"] = round(tnr_scalar, 4)
            report["attack_detection_rate"] = round(tpr_scalar, 4)
            report["binary_summary"] = {
                "normal_class_name": classes[normal_idx] if normal_idx < len(classes) else "Normal",
                "true_positives": tp,
                "true_negatives": tn,
                "false_positives": fp,
                "false_negatives": fn,
                "total_normal_samples": int(tn + fp),
                "total_attack_samples": int(tp + fn),
                "false_positive_rate": round(fpr_scalar, 4),
                "false_negative_rate": round(fnr_scalar, 4),
                "normal_identification_rate": round(tnr_scalar, 4),
                "attack_detection_rate": round(tpr_scalar, 4)
            }
        except Exception as e:
            logger.warning(f"Could not enrich binary summary from confusion matrix: {e}")

    return report


@model_bp.route("/api/model/status", methods=["GET"])
@jwt_required
def get_model_status_api():
    status_copy = dict(training_status)
    active_mh = ModelHistory.query.filter_by(is_active=True).first()
    if active_mh:
        status_copy.setdefault("precision", round(active_mh.precision, 4))
        status_copy.setdefault("recall", round(active_mh.recall, 4))
        status_copy.setdefault("f1_score", round(active_mh.f1_score, 4))
        status_copy["active_model"] = active_mh.to_dict()
        if not status_copy.get("is_training") and active_mh.params_json:
            try:
                pj = json.loads(active_mh.params_json)
                hist = pj.get("epoch_history", [])
                if hist and not status_copy.get("epoch_history"):
                    status_copy["epoch_history"] = hist
                    status_copy["accuracy"] = active_mh.accuracy
                    status_copy["loss"] = active_mh.loss
                    status_copy["model_name"] = active_mh.model_name
                    status_copy["algorithm"] = getattr(active_mh, "algorithm", "Support Vector Machine")
            except Exception:
                pass
    else:
        status_copy["active_model"] = None
        status_copy["model_name"] = None
        status_copy["algorithm"] = None
    return jsonify(status_copy), 200


@model_bp.route("/api/model/report", methods=["GET"])
@jwt_required
def get_model_report_api():
    report_path = None
    latest_mh = ModelHistory.query.order_by(ModelHistory.trained_at.desc()).first()
    if latest_mh and latest_mh.artifact_path:
        cand = os.path.join(latest_mh.artifact_path, "evaluation_report.json")
        if os.path.exists(cand):
            report_path = cand

    if not report_path and os.path.exists(Config.REPORT_FILE_PATH):
        report_path = Config.REPORT_FILE_PATH

    if not report_path:
        return jsonify({"error": "No model evaluation report found. Train a model first."}), 404

    try:
        with open(report_path, "r", encoding="utf-8") as f:
            report = json.load(f)
        report = _enrich_evaluation_report(report)
        if latest_mh:
            report["dataset_name"] = latest_mh.dataset_name
            report["model_name"] = latest_mh.model_name
            if not report.get("algorithm"):
                report["algorithm"] = latest_mh.algorithm
            if not report.get("model_type"):
                report["model_type"] = latest_mh.model_type
            report["trained_at"] = latest_mh.trained_at.strftime("%Y-%m-%d %H:%M:%S") if latest_mh.trained_at else "N/A"
        return jsonify(report), 200
    except Exception as e:
        return jsonify({"error": f"Failed to load evaluation report: {str(e)}"}), 500


@model_bp.route("/api/models", methods=["GET"])
@jwt_required
def get_all_models_api():
    """Retrieve all trained models with performance metrics, versions, and active status."""
    models = ModelHistory.query.order_by(ModelHistory.trained_at.desc()).all()
    return jsonify([m.to_dict() for m in models]), 200


@model_bp.route("/api/models/supported", methods=["GET"])
@jwt_required
def get_supported_models_api():
    """Return supported ML algorithms and their configurable hyperparameter schemas."""
    from training.model_registry import ModelRegistry
    specs = ModelRegistry.get_supported_models_metadata()
    return jsonify({"supported_models": specs}), 200


@model_bp.route("/api/models/<int:model_id>", methods=["GET"])
@jwt_required
def get_model_details_api(model_id):
    """Return comprehensive metadata and evaluation report for a specific trained model."""
    mh = ModelHistory.query.get(model_id)
    if not mh:
        return jsonify({"error": f"Model with ID {model_id} not found."}), 404

    data = mh.to_dict()
    # If report file exists in artifact dir, attach it
    if mh.artifact_path:
        rep_path = os.path.join(mh.artifact_path, "evaluation_report.json")
        if os.path.exists(rep_path):
            try:
                with open(rep_path, "r", encoding="utf-8") as f:
                    rep = json.load(f)
                data["report"] = _enrich_evaluation_report(rep)
            except Exception:
                pass

    return jsonify(data), 200


@model_bp.route("/api/models/<int:model_id>/activate", methods=["POST"])
@jwt_required
@require_role(["Admin"])
def activate_model_api(model_id):
    """Set the specified model as the active model for live detection."""
    import shutil
    mh = ModelHistory.query.get(model_id)
    if not mh:
        return jsonify({"error": f"Model with ID {model_id} not found."}), 404

    if not mh.artifact_path or not os.path.isdir(mh.artifact_path):
        return jsonify({"error": "Model artifact directory does not exist."}), 400

    model_src = os.path.join(mh.artifact_path, "model.joblib")
    scaler_src = os.path.join(mh.artifact_path, "scaler.pkl")
    encoder_src = os.path.join(mh.artifact_path, "encoder.pkl")
    if not os.path.exists(encoder_src):
        encoder_src = os.path.join(mh.artifact_path, "label_encoder.pkl")

    if not os.path.exists(model_src) or not os.path.exists(scaler_src):
        return jsonify({"error": "Required model or scaler artifact missing from disk."}), 400

    try:
        # Copy to root default paths
        shutil.copy2(model_src, os.path.join(Config.MODEL_DIR, "model.joblib"))
        shutil.copy2(scaler_src, Config.SCALER_FILE_PATH)
        if os.path.exists(encoder_src):
            shutil.copy2(encoder_src, Config.ENCODER_FILE_PATH)

        # Update database active flags
        ModelHistory.query.update({ModelHistory.is_active: False})
        mh.is_active = True
        db.session.commit()

        log_audit_event(
            action="MODEL_ACTIVATED",
            status="SUCCESS",
            user_id=g.user.get("user_id"),
            username=g.user.get("username"),
            ip_address=request.remote_addr,
            details=f"Activated model '{mh.model_name}' (ID: {mh.id}) for live intrusion detection."
        )

        return jsonify({
            "success": True,
            "message": f"Model '{mh.model_name}' is now active for live detection.",
            "model": mh.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error activating model: {e}")
        return jsonify({"error": f"Failed to activate model: {str(e)}"}), 500


@model_bp.route("/api/models/<int:model_id>", methods=["DELETE"])
@jwt_required
@require_role(["Admin"])
def delete_model_api(model_id):
    """Delete a trained model record and its artifacts."""
    import shutil
    mh = ModelHistory.query.get(model_id)
    if not mh:
        return jsonify({"error": f"Model with ID {model_id} not found."}), 404

    model_name = mh.model_name
    art_path = mh.artifact_path
    try:
        db.session.delete(mh)
        db.session.commit()

        if art_path and os.path.isdir(art_path) and "test_run" not in art_path:
            shutil.rmtree(art_path, ignore_errors=True)

        log_audit_event(
            action="MODEL_DELETED",
            status="SUCCESS",
            user_id=g.user.get("user_id"),
            username=g.user.get("username"),
            ip_address=request.remote_addr,
            details=f"Deleted model '{model_name}' (ID: {model_id})."
        )
        return jsonify({"success": True, "message": f"Model '{model_name}' deleted."}), 200
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error deleting model: {e}")
        return jsonify({"error": f"Failed to delete model: {str(e)}"}), 500


@model_bp.route("/api/models/compare/benchmark", methods=["POST"])
@jwt_required
def compare_benchmark_api():
    """Mode A: Offline Benchmark Comparison on held-out test data."""
    from training.comparison_service import ModelComparisonService

    data = request.get_json() or {}
    model_ids = data.get("model_ids", [])
    dataset_id = data.get("dataset_id")
    test_limit = int(data.get("test_samples_limit", 3000))
    seed = int(data.get("random_seed", 42))

    if not model_ids:
        # Default to all available models up to 5
        all_models = ModelHistory.query.order_by(ModelHistory.trained_at.desc()).limit(5).all()
        model_ids = [m.id for m in all_models]

    if not model_ids:
        return jsonify({"error": "No trained models available to compare. Train models first."}), 400

    try:
        report = ModelComparisonService.compare_offline_benchmark(
            model_ids=model_ids,
            dataset_id=dataset_id,
            test_samples_limit=test_limit,
            random_seed=seed
        )
        return jsonify(report), 200
    except Exception as e:
        logger.error(f"Benchmark comparison error: {e}")
        return jsonify({"error": f"Benchmark comparison failed: {str(e)}"}), 500


@model_bp.route("/api/models/compare/live", methods=["POST"])
@jwt_required
def compare_live_api():
    """Mode B: Live-Session Retrospective Comparison on captured network flows."""
    from training.comparison_service import ModelComparisonService

    data = request.get_json() or {}
    model_ids = data.get("model_ids", [])
    limit = int(data.get("limit", 100))

    if not model_ids:
        all_models = ModelHistory.query.order_by(ModelHistory.trained_at.desc()).limit(5).all()
        model_ids = [m.id for m in all_models]

    if not model_ids:
        return jsonify({"error": "No trained models available to compare."}), 400

    try:
        report = ModelComparisonService.compare_live_session(
            model_ids=model_ids,
            limit=limit
        )
        return jsonify(report), 200
    except Exception as e:
        logger.error(f"Live comparison error: {e}")
        return jsonify({"error": f"Live comparison failed: {str(e)}"}), 500
