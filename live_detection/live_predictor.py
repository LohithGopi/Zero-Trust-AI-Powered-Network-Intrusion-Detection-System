import os
import joblib
import numpy as np
from typing import Dict, Any, Tuple, Optional
from config import Config
from utils.logger import logger
from .flow_manager import NetworkFlow
from .feature_extractor import FlowFeatureExtractor


class LivePredictor:
    """Zero Trust inference engine for real-time network flow classification."""

    NORMAL_LABELS = {"0", "normal", "benign", "normal."}

    def __init__(self, model_path: Optional[str] = None, scaler_path: Optional[str] = None, encoder_path: Optional[str] = None):
        if not model_path:
            raise FileNotFoundError("No detection model trained. Please train a model based on your dataset first.")

        self.model_path = model_path
        self.scaler_path = scaler_path or os.path.join(Config.MODEL_DIR, "scaler.pkl")
        self.encoder_path = encoder_path or os.path.join(Config.MODEL_DIR, "label_encoder.pkl")
        
        self.model = None
        self.scaler = None
        self.encoder = None
        self.feature_encoders = None
        self.dataset_type = "CIC-IDS2017"
        self.expected_features = 22
        self.extractor = FlowFeatureExtractor()
        
        self._load_artifacts()

    def _load_artifacts(self):
        """Load trained model, scaler, and label encoder from disk."""
        if not self.model_path or not os.path.exists(self.model_path):
            raise FileNotFoundError(f"Model file not found at: {self.model_path}. Please train a model first.")
        if not self.scaler_path or not os.path.exists(self.scaler_path):
            raise FileNotFoundError(f"Scaler file not found at: {self.scaler_path}. Please train a model first.")

        # 1. Load Scaler
        self.scaler = joblib.load(self.scaler_path)
        self.expected_features = getattr(self.scaler, "n_features_in_", 22)

        # Infer dataset type from feature count or path
        norm_path = self.model_path.lower().replace("\\", "/")
        if "unsw" in norm_path or self.expected_features == 15:
            self.dataset_type = "UNSW-NB15"
            self.expected_features = 15
        elif "nsl" in norm_path or self.expected_features in (19, 41):
            self.dataset_type = "NSL-KDD"
            self.expected_features = 19
        else:
            self.dataset_type = "CIC-IDS2017"
            self.expected_features = 22

        # 2. Load Model (.joblib or .keras)
        if self.model_path.endswith(".keras") or self.model_path.endswith(".h5"):
            import tensorflow as tf
            self.model = tf.keras.models.load_model(self.model_path)
        else:
            self.model = joblib.load(self.model_path)

        # 3. Load Encoder if available
        if self.encoder_path and os.path.exists(self.encoder_path):
            self.encoder = joblib.load(self.encoder_path)

        # 4. Load Feature Encoders if available
        artifact_dir = os.path.dirname(self.model_path)
        fe_path = os.path.join(artifact_dir, "feature_encoders.pkl")
        if os.path.exists(fe_path):
            try:
                self.feature_encoders = joblib.load(fe_path)
            except Exception:
                self.feature_encoders = None

        logger.info(f"[LivePredictor] Initialized {self.dataset_type} model with {self.expected_features} features.")

    def validate_compatibility(self) -> Tuple[bool, str]:
        """Validate whether the loaded model and scaler are compatible with live feature extraction."""
        if self.expected_features not in (15, 19, 22):
            return False, f"Incompatible model dimension: Model expects {self.expected_features} features, but live capture supports 15 (UNSW), 19 (NSL), or 22 (CIC)."
        return True, f"Compatible: {self.dataset_type} with {self.expected_features} features."

    def predict_flow(self, flow: NetworkFlow) -> Dict[str, Any]:
        """Classify a network flow into Normal or Attack category with statistical confidence."""
        # 1. Feature extraction
        X_raw = self.extractor.extract(flow, self.dataset_type, self.feature_encoders)
        if X_raw.shape[1] != self.expected_features:
            raise ValueError(f"Feature vector dimension mismatch: got {X_raw.shape[1]}, expected {self.expected_features}")

        # 2. Scaling
        X_scaled = self.scaler.transform(X_raw)

        # 3. Inference
        if hasattr(self.model, "predict_proba"):
            probs = self.model.predict_proba(X_scaled)[0]
            pred_idx = int(np.argmax(probs))
            confidence = float(probs[pred_idx])
        elif hasattr(self.model, "predict"):
            raw_pred = self.model.predict(X_scaled)
            if hasattr(raw_pred, "ndim") and raw_pred.ndim > 1 and raw_pred.shape[1] > 1:
                probs = raw_pred[0]
                pred_idx = int(np.argmax(probs))
                confidence = float(probs[pred_idx])
            else:
                pred_idx = int(round(float(raw_pred[0])))
                confidence = 0.85
        else:
            raise RuntimeError("Model does not implement standard predict interface.")

        # 4. Decode label
        pred_label = self._decode_label(pred_idx)
        is_attack = str(pred_label).strip().lower() not in self.NORMAL_LABELS

        # 5. Risk score assignment
        if not is_attack or confidence < 0.60:
            risk_level = "LOW"
        elif confidence >= 0.85:
            risk_level = "HIGH"
        else:
            risk_level = "MEDIUM"

        if not is_attack:
            display_name = "Normal"
        elif str(pred_label).strip() == "1":
            display_name = "Intrusion Attack"
        else:
            display_name = str(pred_label)

        return {
            "prediction": display_name,
            "confidence": round(confidence, 4),
            "risk_level": risk_level,
            "is_attack": is_attack,
            "dataset_type": self.dataset_type,
            "flow_summary": {
                "src": f"{flow.src_ip}:{flow.src_port}",
                "dst": f"{flow.dst_ip}:{flow.dst_port}",
                "protocol": flow.protocol,
                "duration": round(flow.duration, 3),
                "packets": flow.total_packets,
                "bytes": flow.total_bytes
            }
        }

    def _decode_label(self, idx: int) -> str:
        if self.encoder is not None and hasattr(self.encoder, "classes_"):
            classes = self.encoder.classes_
            if 0 <= idx < len(classes):
                return str(classes[idx])
        elif hasattr(self.model, "classes_"):
            classes = self.model.classes_
            if 0 <= idx < len(classes):
                return str(classes[idx])
        return str(idx)
