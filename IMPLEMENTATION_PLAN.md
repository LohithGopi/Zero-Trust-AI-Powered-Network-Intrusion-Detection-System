# Implementation Plan: Multi-Model Machine Learning Architecture for Zero-Trust NIDS

## 1. Architectural Overview
This plan extends the existing Zero-Trust AI-Powered Network Intrusion Detection System (NIDS) to support multiple trainable machine learning algorithms (**Random Forest**, **Logistic Regression**, and **LSTM / Deep Neural Network**), selectable live detection, and comprehensive offline and live-session model comparisons.

```
+-----------------------------------------------------------------------------------+
|                                  Flask Backend                                    |
|                                                                                   |
|  +--------------------+   +-----------------------+   +------------------------+  |
|  |  Dataset Pipeline  |-->|  Shared Preprocessor  |-->|   Model Registry       |  |
|  |  (NSL, UNSW, CIC)  |   |  (No Data Leakage)    |   |  - Random Forest       |  |
|  +--------------------+   +-----------------------+   |  - Logistic Regression |  |
|                                                       |  - LSTM / Neural Net   |  |
|                                                       +------------------------+  |
|                                                                    |              |
|                     +----------------------------------------------+              |
|                     |                               |                             |
|                     v                               v                             |
|          +---------------------+        +-------------------------+               |
|          | Live Packet Sniffer |        |   Comparison Service    |               |
|          | (Selectable Models, |        | - Mode A: Benchmark     |               |
|          | Realtime/Simulated) |        | - Mode B: Live Replay   |               |
|          +---------------------+        +-------------------------+               |
+-----------------------------------------------------------------------------------+
                                      | (REST APIs)
                                      v
+-----------------------------------------------------------------------------------+
|                                React Frontend                                     |
|  - Model Training (Dataset, Model & Hyperparam Selection, Non-blocking Progress)  |
|  - Live Detection (Trained Model Selector, Realtime / Simulated, Risk Telemetry)  |
|  - Model Comparison (Mode A Held-out Benchmark & Mode B Live Agreement Matrix)    |
|  - Performance Evaluation (Detailed Report, Confusion Matrix, ROC Curves)         |
+-----------------------------------------------------------------------------------+
```

---

## 2. Key Modules to Implement & Enhance

### A. Backend ML Architecture (`training/`)
1. **`training/model_registry.py`**:
   - `BaseNIDSModel`: Abstract base class with `train()`, `predict()`, `predict_proba()`, `save()`, `load()`, `validate_params()`.
   - `RandomForestNIDSModel`: Scikit-learn Random Forest classifier with `n_estimators`, `max_depth`, `min_samples_split`, `min_samples_leaf`, `class_weight`, `random_state`.
   - `LogisticRegressionNIDSModel`: Scikit-learn Logistic Regression classifier with `C`, `penalty`, `solver`, `max_iter`, `class_weight`, `random_state`, convergence monitoring.
   - `LSTMNIDSModel`: Preserves existing deep neural / recurrent architecture with epoch-by-epoch Adam optimization and TensorFlow/Keras fallback.
   - `ModelRegistry`: Factory for model instantiation, default hyperparameters, parameter schemas, and loading saved artifacts.
2. **`training/comparison_service.py`**:
   - **Mode A (Offline Benchmark)**: Evaluates multiple selected trained models against the exact same held-out test dataset partition. Calculates Accuracy, Precision, Recall, F1, FPR, FNR, Confusion Matrix, ROC-AUC, training time, and inference latency.
   - **Mode B (Live-Session Comparison)**: Takes captured flow records from a live detection session and evaluates candidate models retrospectively. Reports inter-model agreement %, alert counts, and inference latency. If ground-truth labels are absent, accurately marks accuracy/recall as N/A without fabrication.
3. **`training/train_model.py`**:
   - Update training pipeline to accept `model_type` (`random_forest`, `logistic_regression`, `lstm`).
   - Fit and save shared preprocessor (`scaler.pkl`, `encoder.pkl`, `feature_encoders.pkl`) alongside model artifact (`model.joblib`).
   - Persist run in `ModelHistory` without deleting prior runs, enabling versioning and history inspection.
4. **`training/evaluate_model.py`**:
   - Calculate comprehensive metrics with robust zero-division handling and positive class definition for attack detection.

### B. Preprocessing Pipeline (`preprocessing/`)
- Ensure data leakage prevention: all encoders and scalers fit ONLY on training fold.
- Maintain consistent feature schema ordering across training, benchmark evaluation, and live feature extraction.

### C. Live Detection Integration (`live_detection/`)
1. **`live_detection/live_predictor.py`**:
   - Load any compatible model artifact (`Random Forest`, `Logistic Regression`, `LSTM`).
   - Validate feature count, scaler compatibility, and label mappings.
2. **`live_detection/packet_capture.py`**:
   - Fix simulated stream mode and replay mechanism so both real-time Npcap and zero-permission simulated mode work reliably.
   - Store privacy-conscious flow feature vector alongside detections in memory/database for Mode B retrospective comparison.

### D. Database Schema & Migration (`database/init_db.py`)
- Safe schema migration for SQLite:
  - `model_history`: Add `algorithm`, `model_version`, `hyperparams_json`, `metrics_json`, `is_active`.
  - `live_detections`: Add `model_name`, `flow_features_json`, `ground_truth`.
- Preserve existing records without dropping tables or losing historical runs.

### E. API Routes (`api/`)
1. **`api/model_routes.py`**:
   - `POST /api/training/start`: Supports `model_type`, configurable hyperparameters, dataset selection, target column.
   - `GET /api/models`: Returns list of all trained models, algorithms, datasets, versions, and metrics.
   - `GET /api/models/<id>`: Returns detailed metadata and evaluation report.
   - `POST /api/models/compare/benchmark`: Mode A offline benchmark comparison.
   - `POST /api/models/compare/live`: Mode B live session comparison.
   - `POST /api/models/<id>/activate`: Set active model for detection.
2. **`api/live_detection_routes.py`**:
   - `GET /api/live-detection/models`: Returns all compatible trained models for the model selector.
   - `POST /api/live-detection/start`: Accepts `model_id` or `model_path` to use the chosen model.

### F. Frontend Dashboard (`frontend/src/`)
1. **`frontend/src/services/api.js`**:
   - Add API methods for multi-model training, model listing, benchmark comparison, and live comparison.
2. **`frontend/src/pages/dashboard/TrainingView.jsx`**:
   - Add Model Selector: Random Forest, Logistic Regression, LSTM.
   - Dynamic hyperparameter configuration cards based on selected model.
   - Target label column selector.
   - Previous training runs / model versions table.
3. **`frontend/src/pages/dashboard/LiveDetectionView.jsx`**:
   - Enhanced Model Selector: Choose between trained RF, LR, and LSTM models with compatibility badge.
   - Displays active model name, algorithm, and feature dimensions.
4. **`frontend/src/pages/dashboard/CompareView.jsx`**:
   - Transform into Model Comparison Matrix:
     - Mode A: Side-by-side benchmark comparison on held-out test data (accuracy, precision, recall, F1, FPR, latency, confusion matrices, ROC curves).
     - Mode B: Live-session agreement comparison on captured flows (agreement %, alert distribution, replayed latency).
5. **`frontend/src/pages/dashboard/ModelDetailsView.jsx`**:
   - Inspect evaluation reports of any selected trained model version.

### G. Automated Testing (`tests/`)
- Comprehensive test suite `tests/test_multi_model.py`:
  - Training Random Forest, Logistic Regression, and LSTM on synthetic & sample benchmark datasets.
  - Model serialization, reloading, and prediction consistency verification.
  - Data leakage prevention validation.
  - Model selection in live detection and compatibility checking.
  - Mode A benchmark comparison on identical test partitions.
  - Mode B live session comparison without ground truth.
  - Fix existing tests in `tests/test_live_detection.py`.
