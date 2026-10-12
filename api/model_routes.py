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
            training_rows=training_rows,
            epochs=epochs,
            batch_size=batch_size,
            learning_rate=learning_rate,
            random_seed=random_seed,
            sequence_length=sequence_length
        )

        log_audit_event(
            action="MODEL_TRAINING_START",
            status="SUCCESS",
            user_id=g.user.get("user_id"),
            username=g.user.get("username"),
            ip_address=request.remote_addr,
            details=f"Started training run '{run_id}' on {ds.filename} ({training_rows:,} rows, seed {random_seed}, {epochs} epochs)."
        )

        return jsonify({
            "message": f"Model training run '{run_id}' initiated successfully.",
            "run_id": run_id,
            "status": "Started",
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
    latest_mh = ModelHistory.query.order_by(ModelHistory.trained_at.desc()).first()
    if latest_mh:
        status_copy.setdefault("precision", round(latest_mh.precision, 4))
        status_copy.setdefault("recall", round(latest_mh.recall, 4))
        status_copy.setdefault("f1_score", round(latest_mh.f1_score, 4))
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
            report["trained_at"] = latest_mh.trained_at.strftime("%Y-%m-%d %H:%M:%S") if latest_mh.trained_at else "N/A"
        return jsonify(report), 200
    except Exception as e:
        return jsonify({"error": f"Failed to load evaluation report: {str(e)}"}), 500
