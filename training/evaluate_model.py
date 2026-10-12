import os
import json
import joblib
import numpy as np
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report, roc_curve, auc
)
from config import Config
from utils.logger import logger

class ModelEvaluator:
    """Evaluates NIDS Machine Learning models and constructs JSON reports."""

    def __init__(self, report_path=Config.REPORT_FILE_PATH, encoder_path=Config.ENCODER_FILE_PATH):
        self.report_path = report_path
        self.encoder_path = encoder_path

    def evaluate(self, model, X_test: np.ndarray, y_test: np.ndarray) -> dict:
        """Calculate complete evaluation metrics, confusion matrix, ROC curve, and save JSON report."""
        logger.info("Evaluating trained intrusion detection model on test partition...")

        # Determine input dimensionality based on model expectations
        is_sklearn = hasattr(model, "predict_proba")
        if is_sklearn:
            X_eval = X_test.reshape(X_test.shape[0], -1) if X_test.ndim == 3 else X_test
            y_pred_probs = model.predict_proba(X_eval)
            y_pred = model.predict(X_eval)
        else:
            X_eval = X_test if X_test.ndim == 3 else np.reshape(X_test, (X_test.shape[0], 1, X_test.shape[1]))
            y_pred_probs = model.predict(X_eval, verbose=0)
            if y_pred_probs.ndim > 1 and y_pred_probs.shape[1] > 1:
                y_pred = np.argmax(y_pred_probs, axis=1)
            else:
                y_pred = (y_pred_probs > 0.5).astype(int).flatten()

        # Load LabelEncoder if available
        classes = None
        if os.path.exists(self.encoder_path):
            try:
                le = joblib.load(self.encoder_path)
                classes = [str(c) for c in le.classes_]
            except Exception as e:
                logger.warning(f"Could not load label encoder classes: {e}")

        if classes is None:
            classes = [str(c) for c in sorted(np.unique(y_test))]

        # Real test metrics
        acc = float(accuracy_score(y_test, y_pred))
        prec = float(precision_score(y_test, y_pred, average='weighted', zero_division=0))
        rec = float(recall_score(y_test, y_pred, average='weighted', zero_division=0))
        f1 = float(f1_score(y_test, y_pred, average='weighted', zero_division=0))

        # Confusion Matrix
        cm_array = confusion_matrix(y_test, y_pred)
        cm = cm_array.tolist()

        # Compute Normal vs. Attack Traffic Classification Breakdown & False Positive Rate (FPR)
        # Identify which class index represents Normal / Benign traffic
        normal_labels_set = {"0", "normal", "benign", "normal."}
        normal_idx = 0
        for idx, cls_name in enumerate(classes):
            if str(cls_name).strip().lower() in normal_labels_set:
                normal_idx = idx
                break

        total_samples = int(np.sum(cm_array)) if cm_array.size > 0 else len(y_test)
        if cm_array.shape[0] >= 2 and normal_idx < cm_array.shape[0]:
            tn = int(cm_array[normal_idx, normal_idx])
            fp = int(np.sum(cm_array[normal_idx, :]) - tn)
            fn = int(np.sum(cm_array[:, normal_idx]) - tn)
            tp = int(total_samples - tn - fp - fn)
        else:
            tn = int(np.sum((y_test == 0) & (y_pred == 0)))
            fp = int(np.sum((y_test == 0) & (y_pred != 0)))
            fn = int(np.sum((y_test != 0) & (y_pred == 0)))
            tp = int(np.sum((y_test != 0) & (y_pred != 0)))

        # False Positive Rate (FPR): How often normal traffic is incorrectly classified as an attack
        fpr_scalar = float(fp / (fp + tn)) if (fp + tn) > 0 else 0.0
        # False Negative Rate (FNR): How often attack traffic is missed as normal
        fnr_scalar = float(fn / (fn + tp)) if (fn + tp) > 0 else 0.0
        # True Negative Rate (Specificity): How correctly normal traffic is identified
        tnr_scalar = float(tn / (tn + fp)) if (tn + fp) > 0 else 1.0
        # True Positive Rate (Completeness / Attack Recall): How completely attacks are detected
        tpr_scalar = float(tp / (tp + fn)) if (tp + fn) > 0 else float(rec)

        binary_summary = {
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

        # Classification Report dict
        target_names = classes if len(classes) == len(np.unique(y_test)) else None
        clf_report = classification_report(y_test, y_pred, target_names=target_names, output_dict=True, zero_division=0)

        # Helper to downsample ROC points evenly up to 100 points
        def sample_roc(fpr_arr, tpr_arr):
            n_pts = len(fpr_arr)
            if n_pts <= 100:
                idx_list = range(n_pts)
            else:
                idx_list = np.linspace(0, n_pts - 1, num=100, dtype=int)
            sampled_fpr = [round(float(fpr_arr[i]), 4) for i in idx_list]
            sampled_tpr = [round(float(tpr_arr[i]), 4) for i in idx_list]
            return sampled_fpr, sampled_tpr

        # ROC Curve generation
        roc_data = {"fpr": [], "tpr": [], "auc": 0.0}
        try:
            num_classes = len(np.unique(y_test))
            if num_classes == 2:
                # Binary classification
                if y_pred_probs.ndim > 1 and y_pred_probs.shape[1] == 2:
                    pos_probs = y_pred_probs[:, 1]
                else:
                    pos_probs = y_pred_probs.ravel()
                fpr, tpr, _ = roc_curve(y_test, pos_probs)
                roc_auc = float(auc(fpr, tpr))
                s_fpr, s_tpr = sample_roc(fpr, tpr)
                roc_data = {
                    "fpr": s_fpr,
                    "tpr": s_tpr,
                    "auc": round(roc_auc, 4)
                }
            else:
                from sklearn.preprocessing import label_binarize
                y_test_bin = label_binarize(y_test, classes=range(len(classes)))
                if y_test_bin.shape[1] == y_pred_probs.shape[1]:
                    fpr, tpr, _ = roc_curve(y_test_bin.ravel(), y_pred_probs.ravel())
                    roc_auc = float(auc(fpr, tpr))
                    s_fpr, s_tpr = sample_roc(fpr, tpr)
                    roc_data = {
                        "fpr": s_fpr,
                        "tpr": s_tpr,
                        "auc": round(roc_auc, 4)
                    }
        except Exception as e:
            logger.warning(f"Could not compute ROC curve data: {str(e)}")

        max_cm_cell = max([max(row) for row in cm]) if (cm and len(cm) > 0 and len(cm[0]) > 0) else 1

        # Real loss computation on test partition
        test_loss = 0.0
        try:
            if hasattr(model, "evaluate"):
                eval_res = model.evaluate(X_eval, y_test, verbose=0)
                test_loss = float(eval_res[0]) if isinstance(eval_res, list) else float(eval_res)
            else:
                from sklearn.metrics import log_loss
                unique_labels = sorted(np.unique(y_test))
                if y_pred_probs.shape[1] == len(unique_labels):
                    test_loss = float(log_loss(y_test, y_pred_probs, labels=unique_labels))
                else:
                    test_loss = float(log_loss(y_test, y_pred_probs))
        except Exception as e:
            logger.warning(f"Test log_loss calculation fallback: {e}")
            test_loss = round(1.0 - acc, 4)

        report = {
            "accuracy": round(acc, 4),
            "loss": round(test_loss, 4),
            "precision": round(prec, 4),
            "recall": round(rec, 4),
            "f1_score": round(f1, 4),
            "false_positive_rate": round(fpr_scalar, 4),
            "false_negative_rate": round(fnr_scalar, 4),
            "normal_identification_rate": round(tnr_scalar, 4),
            "attack_detection_rate": round(tpr_scalar, 4),
            "binary_summary": binary_summary,
            "confusion_matrix": cm,
            "max_cm_cell": max_cm_cell,
            "classes": classes,
            "classification_report": clf_report,
            "roc_curve": roc_data
        }

        # Save evaluation report to JSON file
        os.makedirs(os.path.dirname(self.report_path), exist_ok=True)
        with open(self.report_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=4)
            
        logger.info(f"Model evaluation report saved to {self.report_path}")
        return report
