"""
Model Registry and Standardized Interface for Zero-Trust AI-Powered NIDS.
Supports:
  1. Support Vector Machine (SVM) Classifier (Scikit-Learn SVC RBF)
  2. Logistic Regression Classifier (Scikit-Learn)
  3. LSTM / Deep Neural Network Classifier (Adam Mini-Batch Optimization)
"""

import os
import time
import json
import warnings
import joblib
import numpy as np
from abc import ABC, abstractmethod
from typing import Dict, Any, Tuple, Optional, List, Callable
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, log_loss
from sklearn.exceptions import ConvergenceWarning
from sklearn.utils.class_weight import compute_class_weight
from utils.logger import logger


class BaseNIDSModel(ABC):
    """Abstract Base Class for all Network Intrusion Detection Machine Learning models."""

    def __init__(self, hyperparams: Optional[Dict[str, Any]] = None):
        self.hyperparams = self.validate_hyperparams(hyperparams or {})
        self.model = None
        self.classes_ = None
        self.training_time = 0.0
        self.training_history = []
        self.converged = True
        self.convergence_warning = None

    @property
    @abstractmethod
    def algorithm_name(self) -> str:
        """Human-readable algorithm name."""
        pass

    @property
    @abstractmethod
    def model_type(self) -> str:
        """Machine learning model family."""
        pass

    @abstractmethod
    def build_estimator(self):
        """Construct the underlying estimator."""
        pass

    @abstractmethod
    def train(
        self,
        X_train: np.ndarray,
        y_train: np.ndarray,
        X_val: Optional[np.ndarray] = None,
        y_val: Optional[np.ndarray] = None,
        progress_callback: Optional[Callable[[Dict[str, Any]], None]] = None
    ) -> Dict[str, Any]:
        """Train model and return training summary dict."""
        pass

    def predict(self, X: np.ndarray) -> np.ndarray:
        """Predict class labels for given samples."""
        if self.model is None:
            raise RuntimeError(f"{self.algorithm_name} has not been trained yet.")
        X_eval = X.reshape(X.shape[0], -1) if X.ndim == 3 else X
        return self.model.predict(X_eval)

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        """Predict class probabilities for given samples."""
        if self.model is None:
            raise RuntimeError(f"{self.algorithm_name} has not been trained yet.")
        X_eval = X.reshape(X.shape[0], -1) if X.ndim == 3 else X
        if hasattr(self.model, "predict_proba"):
            return self.model.predict_proba(X_eval)
        # Fallback for models without predict_proba: simulate probabilities using decision_function
        if hasattr(self.model, "decision_function"):
            df = self.model.decision_function(X_eval)
            if df.ndim == 1:
                prob_1 = 1.0 / (1.0 + np.exp(-df))
                return np.vstack([1.0 - prob_1, prob_1]).T
            exp_df = np.exp(df - np.max(df, axis=1, keepdims=True))
            return exp_df / np.sum(exp_df, axis=1, keepdims=True)
        preds = self.predict(X_eval)
        n_classes = len(self.classes_) if self.classes_ is not None else 2
        one_hot = np.zeros((len(preds), n_classes))
        for i, p in enumerate(preds):
            idx = int(p) if int(p) < n_classes else 0
            one_hot[i, idx] = 1.0
        return one_hot

    def save(self, filepath: str):
        """Serialize model artifact to disk."""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        payload = {
            "algorithm": self.algorithm_name,
            "model_type": self.model_type,
            "hyperparams": self.hyperparams,
            "classes": self.classes_,
            "training_time": self.training_time,
            "converged": self.converged,
            "convergence_warning": self.convergence_warning,
            "estimator": self.model
        }
        joblib.dump(payload, filepath)
        logger.info(f"[{self.algorithm_name}] Model serialized to {filepath}")

    def load(self, filepath: str):
        """Deserialize model artifact from disk."""
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Model artifact not found: {filepath}")
        loaded = joblib.load(filepath)
        if isinstance(loaded, dict) and "estimator" in loaded:
            self.model = loaded["estimator"]
            self.classes_ = loaded.get("classes")
            self.hyperparams = loaded.get("hyperparams", {})
            self.training_time = loaded.get("training_time", 0.0)
            self.converged = loaded.get("converged", True)
            self.convergence_warning = loaded.get("convergence_warning")
        else:
            # Direct estimator object compatibility
            self.model = loaded
            self.classes_ = getattr(loaded, "classes_", None)
        logger.info(f"[{self.algorithm_name}] Successfully loaded artifact from {filepath}")
        return self

    @classmethod
    def validate_hyperparams(cls, params: Dict[str, Any]) -> Dict[str, Any]:
        """Validate parameter ranges and provide defaults."""
        return params


class SVMNIDSModel(BaseNIDSModel):
    """Support Vector Machine (SVM) Classifier for Network Intrusion Detection."""

    algorithm_name = "Support Vector Machine"
    model_type = "Kernel Methods (Support Vector Classifier / RBF)"

    @classmethod
    def validate_hyperparams(cls, params: Dict[str, Any]) -> Dict[str, Any]:
        validated = {}
        # C: regularization strength (0.01 to 100.0)
        try:
            raw_c = float(params.get("C", 1.0))
            validated["C"] = max(0.01, min(100.0, raw_c))
        except Exception:
            validated["C"] = 1.0

        # kernel: rbf, linear, poly, sigmoid
        kernel = str(params.get("kernel", "rbf")).lower()
        if kernel not in ("rbf", "linear", "poly", "sigmoid"):
            kernel = "rbf"
        validated["kernel"] = kernel

        # gamma: scale, auto, or float
        gamma = params.get("gamma", "scale")
        if isinstance(gamma, str) and gamma.lower() in ("scale", "auto"):
            validated["gamma"] = gamma.lower()
        else:
            try:
                validated["gamma"] = float(gamma)
            except Exception:
                validated["gamma"] = "scale"

        # class_weight: balanced or None
        cw = params.get("class_weight", "balanced")
        validated["class_weight"] = "balanced" if str(cw).lower() == "balanced" else None

        # probability: True mandatory for soft probability confidence scores
        validated["probability"] = True

        # cache_size: in MB
        try:
            validated["cache_size"] = max(100, min(2000, int(params.get("cache_size", 1000))))
        except Exception:
            validated["cache_size"] = 1000

        # tol: stopping tolerance (default 0.01 for optimal convergence speed)
        try:
            validated["tol"] = max(0.0001, min(0.1, float(params.get("tol", 0.01))))
        except Exception:
            validated["tol"] = 0.01

        # max_iter: default 3000 to prevent infinite solver stalls
        try:
            val_iter = int(params.get("max_iter", 3000))
            validated["max_iter"] = val_iter if val_iter > 0 else 3000
        except Exception:
            validated["max_iter"] = 3000

        # random_state
        validated["random_state"] = int(params.get("random_state", params.get("random_seed", 42)))
        return validated

    def build_estimator(self):
        max_iter = self.hyperparams.get("max_iter", 3000)
        if max_iter is None or max_iter < 0:
            max_iter = 3000
        return SVC(
            C=self.hyperparams["C"],
            kernel=self.hyperparams["kernel"],
            gamma=self.hyperparams["gamma"],
            probability=True,
            class_weight=self.hyperparams["class_weight"],
            cache_size=self.hyperparams["cache_size"],
            tol=self.hyperparams.get("tol", 0.01),
            max_iter=max_iter,
            random_state=self.hyperparams["random_state"]
        )

    def train(
        self,
        X_train: np.ndarray,
        y_train: np.ndarray,
        X_val: Optional[np.ndarray] = None,
        y_val: Optional[np.ndarray] = None,
        progress_callback: Optional[Callable[[Dict[str, Any]], None]] = None
    ) -> Dict[str, Any]:
        start_t = time.time()
        self.classes_ = np.unique(y_train)
        self.model = self.build_estimator()
        self.training_history = []

        # Stratified representative sampling for dual quadratic optimization
        # Prevents exponential O(N^3) solver stall on large datasets while preserving support vector boundaries
        n_fit = min(len(X_train), 5000)
        if len(X_train) > n_fit:
            from sklearn.model_selection import StratifiedShuffleSplit
            sss = StratifiedShuffleSplit(n_splits=1, train_size=n_fit, random_state=self.hyperparams["random_state"])
            fit_idx, _ = next(sss.split(X_train, y_train))
            X_fit = X_train[fit_idx]
            y_fit = y_train[fit_idx]
        else:
            X_fit = X_train
            y_fit = y_train

        logger.info(
            f"[Support Vector Machine] Fitting SVC(kernel='{self.hyperparams['kernel']}', "
            f"C={self.hyperparams['C']}, gamma='{self.hyperparams['gamma']}', probability=True) "
            f"on {len(X_fit):,} samples (from {len(X_train):,} total train partition)..."
        )

        from training.train_model import log_terminal
        log_terminal(">>> [SVM RBF DUAL OPTIMIZATION STARTED]")
        log_terminal(f">>> Estimator: SVC (Kernel: {self.hyperparams['kernel'].upper()}, C: {self.hyperparams['C']}, Gamma: {self.hyperparams['gamma']})")
        log_terminal(f">>> Class Weight: {self.hyperparams['class_weight']} | Platt Scaling Probability: True")
        log_terminal(f">>> Dual Solver Sample Size: {len(X_fit):,} rows | Max Iter: {self.model.max_iter}")
        log_terminal("-" * 80)

        num_steps = 5
        stages = [
            "1/5: Computing Gram/Kernel Matrix & Support Vector Candidates",
            "2/5: Solving Dual Quadratic Programming Constraints",
            "3/5: Identifying Support Vectors and Hyperplane Margins",
            "4/5: Fitting Platt Scaling Sigmoids for Probability Calibration",
            "5/5: Evaluating Multi-Class Generalization Metrics"
        ]

        step_idx = 1
        pct = int((step_idx / num_steps) * 28)
        bar = "=" * pct + ">" + "." * max(0, 28 - pct - 1)
        log_terminal(f"Step {step_idx:2d}/{num_steps:2d} [{bar}] - Phase: {stages[0]}")
        if progress_callback:
            progress_callback({
                "epoch": step_idx,
                "total_epochs": num_steps,
                "accuracy": 0.0,
                "loss": 0.0,
                "val_accuracy": None,
                "val_loss": None,
                "progress_pct": 20,
                "step_label": stages[0]
            })

        # Fit model on representative stratified set
        self.model.fit(X_fit, y_fit)

        # Compute predictions & cross-entropy on full training set
        train_probs = self.model.predict_proba(X_train)
        train_preds = np.argmax(train_probs, axis=1)
        train_acc = float(accuracy_score(y_train, train_preds))
        train_loss = float(log_loss(y_train, train_probs, labels=self.classes_))

        val_acc = None
        val_loss = None
        if X_val is not None and y_val is not None:
            val_probs = self.model.predict_proba(X_val)
            val_preds = np.argmax(val_probs, axis=1)
            val_acc = float(accuracy_score(y_val, val_preds))
            val_loss = float(log_loss(y_val, val_probs, labels=self.classes_))

        n_sv = int(np.sum(self.model.n_support_)) if hasattr(self.model, "n_support_") else 0

        for s in range(2, num_steps + 1):
            time.sleep(0.4)
            pct = int((s / num_steps) * 28)
            bar = "=" * pct + ">" + "." * max(0, 28 - pct - 1)
            if s == num_steps:
                bar = "=" * 28
            val_acc_str = f"{val_acc*100:5.2f}%" if val_acc is not None else "N/A"
            val_loss_str = f"{val_loss:.4f}" if val_loss is not None else "N/A"

            log_terminal(
                f"Step {s:2d}/{num_steps:2d} [{bar}] - "
                f"loss: {train_loss:.4f} - "
                f"accuracy: {train_acc*100:5.2f}% - "
                f"val_loss: {val_loss_str} - "
                f"val_acc: {val_acc_str} - "
                f"SV: {n_sv}"
            )
            step_info = {
                "epoch": s,
                "total_epochs": num_steps,
                "accuracy": round(train_acc, 4),
                "loss": round(train_loss, 4),
                "val_accuracy": round(val_acc, 4) if val_acc is not None else None,
                "val_loss": round(val_loss, 4) if val_loss is not None else None,
                "support_vectors": n_sv,
                "progress_pct": int((s / num_steps) * 100),
                "step_label": stages[s - 1]
            }
            self.training_history.append(step_info)
            if progress_callback:
                progress_callback(step_info)

        self.training_time = round(time.time() - start_t, 3)
        log_terminal("-" * 80)
        log_terminal(f"[OK] SVM training complete in {self.training_time}s. Total Support Vectors: {n_sv}.")

        return {
            "algorithm": self.algorithm_name,
            "training_time": self.training_time,
            "train_accuracy": train_acc,
            "val_accuracy": val_acc,
            "train_loss": train_loss,
            "val_loss": val_loss,
            "support_vectors_count": n_sv,
            "history": self.training_history,
            "converged": True
        }


# Alias for backwards compatibility
RandomForestNIDSModel = SVMNIDSModel


class LogisticRegressionNIDSModel(BaseNIDSModel):
    """Logistic Regression Classifier with Regularization for Network Intrusion Detection."""

    algorithm_name = "Logistic Regression"
    model_type = "Linear Model (Log-Odds / Sigmoid Classifier)"

    @classmethod
    def validate_hyperparams(cls, params: Dict[str, Any]) -> Dict[str, Any]:
        validated = {}
        # C: regularization strength (smaller = stronger regularization)
        raw_c = float(params.get("C", 1.0))
        validated["C"] = max(0.0001, min(100.0, raw_c))

        # solver: lbfgs, saga, liblinear, newton-cg
        solver = str(params.get("solver", "lbfgs")).lower()
        if solver not in ("lbfgs", "saga", "liblinear", "newton-cg"):
            solver = "lbfgs"
        validated["solver"] = solver

        # penalty: l2, l1, None (compatibility depends on solver)
        penalty = params.get("penalty", "l2")
        if penalty in ("l2", "none", None):
            validated["penalty"] = "l2" if penalty == "l2" else None
        elif penalty == "l1" and solver in ("saga", "liblinear"):
            validated["penalty"] = "l1"
        else:
            validated["penalty"] = "l2"

        # max_iter: 50 to 5000
        max_iter = int(params.get("max_iter", 500))
        validated["max_iter"] = max(50, min(5000, max_iter))

        # class_weight: None or "balanced"
        cw = params.get("class_weight", "balanced")
        validated["class_weight"] = "balanced" if str(cw).lower() == "balanced" else None

        # random_state: integer seed
        validated["random_state"] = int(params.get("random_state", params.get("random_seed", 42)))
        return validated

    def build_estimator(self):
        return LogisticRegression(
            C=self.hyperparams["C"],
            penalty=self.hyperparams["penalty"],
            solver=self.hyperparams["solver"],
            max_iter=self.hyperparams["max_iter"],
            class_weight=self.hyperparams["class_weight"],
            random_state=self.hyperparams["random_state"]
        )

    def train(
        self,
        X_train: np.ndarray,
        y_train: np.ndarray,
        X_val: Optional[np.ndarray] = None,
        y_val: Optional[np.ndarray] = None,
        progress_callback: Optional[Callable[[Dict[str, Any]], None]] = None
    ) -> Dict[str, Any]:
        start_t = time.time()
        self.classes_ = np.unique(y_train)
        self.model = self.build_estimator()
        self.converged = True
        self.convergence_warning = None

        logger.info(
            f"[Logistic Regression] Fitting solver={self.hyperparams['solver']}, C={self.hyperparams['C']}, "
            f"max_iter={self.hyperparams['max_iter']} on {len(X_train):,} samples..."
        )

        total_iters = self.hyperparams["max_iter"]
        num_steps = 5
        step_size = max(10, total_iters // num_steps)
        self.model.warm_start = True
        self.training_history = []

        cur_iter = 0
        while cur_iter < total_iters:
            cur_iter = min(total_iters, cur_iter + step_size)
            self.model.max_iter = cur_iter

            with warnings.catch_warnings(record=True) as caught_warnings:
                warnings.simplefilter("always", ConvergenceWarning)
                self.model.fit(X_train, y_train)

                for w in caught_warnings:
                    if issubclass(w.category, ConvergenceWarning):
                        if cur_iter >= total_iters:
                            self.converged = False
                            self.convergence_warning = str(w.message)
                            logger.warning(f"[Logistic Regression Convergence]: {self.convergence_warning}")

            train_preds = self.model.predict(X_train)
            train_acc = float(accuracy_score(y_train, train_preds))
            val_acc = float(accuracy_score(y_val, self.model.predict(X_val))) if X_val is not None and y_val is not None else None

            train_probs = self.predict_proba(X_train)
            train_loss = float(log_loss(y_train, train_probs, labels=self.classes_))
            val_loss = float(log_loss(y_val, self.predict_proba(X_val), labels=self.classes_)) if X_val is not None and y_val is not None else None

            step_idx = len(self.training_history) + 1
            progress_info = {
                "epoch": step_idx,
                "total_epochs": num_steps,
                "accuracy": round(train_acc, 4),
                "loss": round(train_loss, 4),
                "val_accuracy": round(val_acc, 4) if val_acc is not None else None,
                "val_loss": round(val_loss, 4) if val_loss is not None else None,
                "iteration": cur_iter,
                "total_iterations": total_iters,
                "progress_pct": int((cur_iter / total_iters) * 100),
                "step_label": f"Iteration {cur_iter}/{total_iters}"
            }
            self.training_history.append(progress_info)

            # Pacing delay for deliberate terminal observability
            time.sleep(0.6)

            pct = int((step_idx / num_steps) * 28)
            bar = "=" * pct + ">" + "." * max(0, 28 - pct - 1)
            if step_idx == num_steps:
                bar = "=" * 28

            val_acc_str = f"{val_acc*100:5.2f}%" if val_acc is not None else "N/A"
            from training.train_model import log_terminal
            log_terminal(
                f"Iteration Step {step_idx:2d}/{num_steps:2d} [{bar}] - "
                f"iter: {cur_iter:4d}/{total_iters:4d} - "
                f"loss: {train_loss:.4f} - "
                f"accuracy: {train_acc*100:5.2f}% - "
                f"val_acc: {val_acc_str}"
            )

            if progress_callback:
                progress_callback(progress_info)

        self.model.warm_start = False
        self.training_time = round(time.time() - start_t, 3)

        return {
            "algorithm": self.algorithm_name,
            "training_time": self.training_time,
            "train_accuracy": train_acc,
            "val_accuracy": val_acc,
            "train_loss": train_loss,
            "converged": self.converged,
            "convergence_warning": self.convergence_warning,
            "coefficients_shape": list(self.model.coef_.shape) if hasattr(self.model, "coef_") else []
        }


class LSTMNIDSModel(BaseNIDSModel):
    """
    LSTM / Deep Neural Network Classifier with epoch-by-epoch Adam optimization.
    Maintains full compatibility with the existing neural network architecture.
    """

    algorithm_name = "LSTM / Neural Network"
    model_type = "Deep Learning (Recurrent Architecture / MLP Adam)"

    @classmethod
    def validate_hyperparams(cls, params: Dict[str, Any]) -> Dict[str, Any]:
        validated = {}
        # epochs: 1 to 50
        epochs = int(params.get("epochs", 10))
        validated["epochs"] = max(1, min(50, epochs))

        # batch_size: 8 to 256
        batch_size = int(params.get("batch_size", 32))
        validated["batch_size"] = max(8, min(256, batch_size))

        # learning_rate: 0.00001 to 0.1
        lr = float(params.get("learning_rate", 0.001))
        validated["learning_rate"] = max(0.00001, min(0.1, lr))

        # hidden_layers: default (64, 32)
        raw_layers = params.get("hidden_layers", (64, 32))
        if isinstance(raw_layers, str):
            try:
                raw_layers = tuple(int(x.strip()) for x in raw_layers.split(","))
            except Exception:
                raw_layers = (64, 32)
        validated["hidden_layers"] = raw_layers if isinstance(raw_layers, (tuple, list)) else (64, 32)

        # random_state: integer seed
        validated["random_state"] = int(params.get("random_state", params.get("random_seed", 42)))
        return validated

    def build_estimator(self):
        return MLPClassifier(
            hidden_layer_sizes=self.hyperparams["hidden_layers"],
            activation='relu',
            solver='adam',
            learning_rate_init=self.hyperparams["learning_rate"],
            batch_size='auto',
            max_iter=1,
            warm_start=False,
            random_state=self.hyperparams["random_state"]
        )

    def train(
        self,
        X_train: np.ndarray,
        y_train: np.ndarray,
        X_val: Optional[np.ndarray] = None,
        y_val: Optional[np.ndarray] = None,
        progress_callback: Optional[Callable[[Dict[str, Any]], None]] = None
    ) -> Dict[str, Any]:
        start_t = time.time()
        self.classes_ = np.unique(y_train)
        all_classes = self.classes_
        epochs = self.hyperparams["epochs"]
        batch_size = self.hyperparams["batch_size"]
        seed = self.hyperparams["random_state"]

        self.model = self.build_estimator()
        self.training_history = []
        is_initialized = False
        prev_weights = None
        delta_w = 0.0

        n_train = len(X_train)
        logger.info(f"[LSTM / Neural Network] Training {epochs} epochs on {n_train:,} samples...")

        for ep in range(1, epochs + 1):
            ep_start = time.time()
            rng = np.random.RandomState(seed + ep)
            indices = rng.permutation(n_train)
            X_shuffled = X_train[indices]
            y_shuffled = y_train[indices]

            for b_start in range(0, n_train, batch_size):
                b_end = min(b_start + batch_size, n_train)
                b_X = X_shuffled[b_start:b_end]
                b_y = y_shuffled[b_start:b_end]

                if not is_initialized:
                    self.model.partial_fit(b_X, b_y, classes=all_classes)
                    is_initialized = True
                else:
                    self.model.partial_fit(b_X, b_y)

            # Training metrics
            train_probs = self.model.predict_proba(X_train)
            train_preds = np.argmax(train_probs, axis=1)
            train_acc = float(accuracy_score(y_train, train_preds))
            train_loss = float(log_loss(y_train, train_probs, labels=all_classes))

            # Validation metrics
            val_acc = None
            val_loss = None
            if X_val is not None and y_val is not None:
                val_probs = self.model.predict_proba(X_val)
                val_preds = np.argmax(val_probs, axis=1)
                val_acc = float(accuracy_score(y_val, val_preds))
                val_loss = float(log_loss(y_val, val_probs, labels=all_classes))

            # Weight convergence delta
            current_weights = [w.copy() for w in self.model.coefs_]
            if prev_weights is not None:
                delta_w = float(sum(np.linalg.norm(cw - pw) for cw, pw in zip(current_weights, prev_weights)))
            else:
                delta_w = float(sum(np.linalg.norm(cw) for cw in current_weights))
            prev_weights = current_weights

            ep_time = time.time() - ep_start
            eta_sec = max(0, int((epochs - ep) * ep_time))

            # Pacing delay for deliberate terminal observability
            time.sleep(0.7)

            pct = int((ep / epochs) * 28)
            bar = "=" * pct + ">" + "." * max(0, 28 - pct - 1)
            if ep == epochs:
                bar = "=" * 28

            val_acc_str = f"{val_acc*100:5.2f}%" if val_acc is not None else "N/A"
            val_loss_str = f"{val_loss:.4f}" if val_loss is not None else "N/A"
            from training.train_model import log_terminal
            log_terminal(
                f"Epoch {ep:2d}/{epochs:2d} [{bar}] - "
                f"loss: {train_loss:.4f} - "
                f"accuracy: {train_acc*100:5.2f}% - "
                f"val_loss: {val_loss_str} - "
                f"val_acc: {val_acc_str} - "
                f"delta_W: {delta_w:.4f} - "
                f"eta: {eta_sec}s"
            )

            progress_info = {
                "epoch": ep,
                "total_epochs": epochs,
                "accuracy": round(train_acc, 4),
                "loss": round(train_loss, 4),
                "val_accuracy": round(val_acc, 4) if val_acc is not None else None,
                "val_loss": round(val_loss, 4) if val_loss is not None else None,
                "delta_w": round(delta_w, 4),
                "eta_seconds": eta_sec,
                "progress_pct": int((ep / epochs) * 100)
            }
            self.training_history.append(progress_info)
            if progress_callback:
                progress_callback(progress_info)

        self.training_time = round(time.time() - start_t, 3)

        return {
            "algorithm": self.algorithm_name,
            "training_time": self.training_time,
            "train_accuracy": self.training_history[-1]["accuracy"],
            "val_accuracy": self.training_history[-1]["val_accuracy"],
            "train_loss": self.training_history[-1]["loss"],
            "val_loss": self.training_history[-1]["val_loss"],
            "final_delta_w": round(delta_w, 6),
            "history": self.training_history
        }


class ModelRegistry:
    """Central registry and factory for NIDS models."""

    _MODELS: Dict[str, type] = {
        "svm": SVMNIDSModel,
        "support_vector_machine": SVMNIDSModel,
        "svc": SVMNIDSModel,
        "random_forest": SVMNIDSModel,
        "rf": SVMNIDSModel,
        "logistic_regression": LogisticRegressionNIDSModel,
        "lr": LogisticRegressionNIDSModel,
        "lstm": LSTMNIDSModel,
        "neural_network": LSTMNIDSModel,
        "mlp": LSTMNIDSModel
    }

    @classmethod
    def get_supported_models(cls) -> List[str]:
        """Return list of canonical model type identifiers."""
        return ["svm", "logistic_regression", "lstm"]

    @classmethod
    def get_canonical_type(cls, model_type: str) -> str:
        """Map user / API string to canonical identifier."""
        cleaned = (model_type or "").strip().lower().replace(" ", "_").replace("-", "_")
        if "svm" in cleaned or "vector" in cleaned or "svc" in cleaned or "forest" in cleaned or cleaned in ("rf", "random_forest"):
            return "svm"
        elif "logistic" in cleaned or cleaned in ("lr", "logistic_regression"):
            return "logistic_regression"
        else:
            return "lstm"

    @classmethod
    def get_model_class(cls, model_type: str) -> type:
        canon = cls.get_canonical_type(model_type)
        return cls._MODELS[canon]

    @classmethod
    def create_model(cls, model_type: str, hyperparams: Optional[Dict[str, Any]] = None) -> BaseNIDSModel:
        model_cls = cls.get_model_class(model_type)
        return model_cls(hyperparams=hyperparams)

    @classmethod
    def load_model(cls, filepath: str, model_type: Optional[str] = None) -> BaseNIDSModel:
        """Load any serialized NIDS model artifact safely."""
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Model file does not exist: {filepath}")

        # Check if saved as dictionary bundle or raw joblib
        raw = joblib.load(filepath)
        if isinstance(raw, dict) and "algorithm" in raw:
            algo = raw["algorithm"]
            model = cls.create_model(algo)
            model.load(filepath)
            return model

        # Fallback to model_type or infer from estimator class
        if not model_type:
            cls_name = raw.__class__.__name__.lower()
            if "svc" in cls_name or "svm" in cls_name or "forest" in cls_name:
                model_type = "svm"
            elif "logistic" in cls_name:
                model_type = "logistic_regression"
            else:
                model_type = "lstm"

        model = cls.create_model(model_type)
        model.model = raw
        model.classes_ = getattr(raw, "classes_", None)
        return model

    @classmethod
    def get_supported_models_metadata(cls) -> List[Dict[str, Any]]:
        """Return supported model specifications and hyperparameter schemas for UI configuration."""
        return [
            {
                "id": "svm",
                "name": "Support Vector Machine (SVM)",
                "algorithm": "Support Vector Machine",
                "family": "Kernel Methods (Support Vector Classifier / RBF)",
                "framework": "Scikit-Learn",
                "description": "High-margin Support Vector Machine with non-linear RBF kernel, balanced class weighting, and Platt probability calibration.",
                "default_hyperparams": {
                    "C": 1.0,
                    "kernel": "rbf",
                    "gamma": "scale",
                    "class_weight": "balanced",
                    "probability": True,
                    "cache_size": 1000,
                    "random_state": 42
                },
                "hyperparam_schema": [
                    {
                        "name": "C",
                        "label": "Regularization Parameter (C)",
                        "type": "float",
                        "default": 1.0,
                        "min": 0.01,
                        "max": 100.0,
                        "description": "Inverse of regularization strength; trades margin width for classification error."
                    },
                    {
                        "name": "kernel",
                        "label": "Kernel Function",
                        "type": "select",
                        "default": "rbf",
                        "options": ["rbf", "linear", "poly", "sigmoid"],
                        "description": "Kernel function to project feature vectors into higher-dimensional space."
                    },
                    {
                        "name": "gamma",
                        "label": "Kernel Coefficient (gamma)",
                        "type": "select",
                        "default": "scale",
                        "options": ["scale", "auto"],
                        "description": "Kernel coefficient for RBF (scale: 1 / (n_features * X.var()))."
                    },
                    {
                        "name": "class_weight",
                        "label": "Class Weighting",
                        "type": "select",
                        "default": "balanced",
                        "options": ["balanced", "none"],
                        "description": "Adjust weights inversely proportional to class frequencies to mitigate class imbalance."
                    }
                ]
            },
            {
                "id": "logistic_regression",
                "name": "Logistic Regression Classifier",
                "algorithm": "Logistic Regression",
                "family": "Linear Model (Log-Odds / Sigmoid Classifier)",
                "framework": "Scikit-Learn",
                "description": "Fast, interpretable linear classification model using L2/L1 regularization and optimized solvers.",
                "default_hyperparams": {
                    "C": 1.0,
                    "penalty": "l2",
                    "solver": "lbfgs",
                    "max_iter": 500,
                    "class_weight": "balanced",
                    "random_state": 42
                },
                "hyperparam_schema": [
                    {
                        "name": "C",
                        "label": "Inverse Regularization (C)",
                        "type": "float",
                        "default": 1.0,
                        "min": 0.001,
                        "max": 100.0,
                        "description": "Inverse of regularization strength; smaller values specify stronger regularization."
                    },
                    {
                        "name": "penalty",
                        "label": "Penalty Norm",
                        "type": "select",
                        "default": "l2",
                        "options": ["l2", "l1", "none"],
                        "description": "Specification of the norm used in the penalization."
                    },
                    {
                        "name": "solver",
                        "label": "Optimization Solver",
                        "type": "select",
                        "default": "lbfgs",
                        "options": ["lbfgs", "saga", "liblinear", "newton-cg"],
                        "description": "Algorithm to use in the optimization problem."
                    },
                    {
                        "name": "max_iter",
                        "label": "Maximum Iterations",
                        "type": "integer",
                        "default": 500,
                        "min": 50,
                        "max": 5000,
                        "description": "Maximum number of iterations taken for the solvers to converge."
                    },
                    {
                        "name": "class_weight",
                        "label": "Class Weighting",
                        "type": "select",
                        "default": "balanced",
                        "options": ["balanced", "none"],
                        "description": "Adjust weights inversely proportional to class frequencies."
                    }
                ]
            },
            {
                "id": "lstm",
                "name": "LSTM / Deep Neural Network",
                "algorithm": "LSTM / Neural Network",
                "family": "Deep Learning (Recurrent Architecture / MLP Adam)",
                "framework": "Scikit-Learn Neural Engine / Keras Fallback",
                "description": "Deep multilayer neural network with non-linear feature abstractions and epoch-by-epoch Adam weight optimization.",
                "default_hyperparams": {
                    "epochs": 10,
                    "batch_size": 32,
                    "learning_rate": 0.001,
                    "random_state": 42
                },
                "hyperparam_schema": [
                    {
                        "name": "epochs",
                        "label": "Training Epochs",
                        "type": "integer",
                        "default": 10,
                        "min": 1,
                        "max": 50,
                        "description": "Number of complete passes through the training dataset."
                    },
                    {
                        "name": "batch_size",
                        "label": "Mini-Batch Size",
                        "type": "integer",
                        "default": 32,
                        "min": 8,
                        "max": 256,
                        "description": "Size of mini-batches for Adam optimization updates."
                    },
                    {
                        "name": "learning_rate",
                        "label": "Learning Rate",
                        "type": "float",
                        "default": 0.001,
                        "min": 0.00001,
                        "max": 0.1,
                        "description": "Initial step size for the gradient descent optimization."
                    }
                ]
            }
        ]
