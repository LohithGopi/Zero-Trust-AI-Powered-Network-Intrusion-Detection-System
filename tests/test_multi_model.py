import os
import sys
import json
import shutil
import tempfile
import unittest
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app
from database.init_db import db, ModelHistory, DatasetHistory, LiveDetection
from security.jwt_auth import generate_token
from training.model_registry import (
    ModelRegistry,
    RandomForestNIDSModel,
    LogisticRegressionNIDSModel,
    LSTMNIDSModel
)
from training.comparison_service import ModelComparisonService


class TestMultiModelSystem(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp_dir = tempfile.mkdtemp(prefix="nids_test_models_")
        cls.test_db_path = os.path.join(cls.temp_dir, "test.db")
        cls.app = create_app({
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": f"sqlite:///{cls.test_db_path}"
        })
        cls.client = cls.app.test_client()

        cls.admin_token = generate_token(user_id=1, username="admin", role="Admin")
        cls.analyst_token = generate_token(user_id=2, username="analyst", role="Analyst")
        cls.user_token = generate_token(user_id=3, username="user", role="User")

        # Synthetic dataset for unit testing
        np.random.seed(42)
        n_samples = 300
        n_features = 10
        cls.X_synthetic = np.random.randn(n_samples, n_features)
        # Binary target: 0 (Normal), 1 (Attack)
        cls.y_synthetic = (cls.X_synthetic[:, 0] + cls.X_synthetic[:, 1] > 0).astype(int)

        cls.X_train = cls.X_synthetic[:200]
        cls.y_train = cls.y_synthetic[:200]
        cls.X_test = cls.X_synthetic[200:]
        cls.y_test = cls.y_synthetic[200:]

        with cls.app.app_context():
            db.create_all()

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(cls.temp_dir):
            shutil.rmtree(cls.temp_dir, ignore_errors=True)

    def test_01_model_registry_supported_types(self):
        """Verify registry provides supported types and schemas."""
        supported = ModelRegistry.get_supported_models()
        self.assertIn("random_forest", supported)
        self.assertIn("logistic_regression", supported)
        self.assertIn("lstm", supported)

        metadata = ModelRegistry.get_supported_models_metadata()
        self.assertEqual(len(metadata), 3)
        for meta in metadata:
            self.assertIn("id", meta)
            self.assertIn("name", meta)
            self.assertIn("hyperparam_schema", meta)
            self.assertIn("default_hyperparams", meta)

    def test_02_random_forest_lifecycle(self):
        """Test Random Forest training, evaluation, saving, and loading."""
        rf = RandomForestNIDSModel({"n_estimators": 10, "max_depth": 5, "random_state": 42})
        self.assertEqual(rf.algorithm_name, "Random Forest")

        progress_calls = []
        def on_progress(p):
            progress_calls.append(p)

        summary = rf.train(self.X_train, self.y_train, self.X_test, self.y_test, progress_callback=on_progress)
        self.assertGreater(len(progress_calls), 0)
        self.assertIn("train_accuracy", summary)
        self.assertIn("val_accuracy", summary)

        preds = rf.predict(self.X_test)
        self.assertEqual(len(preds), len(self.y_test))
        probs = rf.predict_proba(self.X_test)
        self.assertEqual(probs.shape, (len(self.y_test), 2))
        np.testing.assert_allclose(probs.sum(axis=1), np.ones(len(self.y_test)), atol=1e-5)

        save_path = os.path.join(self.temp_dir, "rf_standalone.pkl")
        rf.save(save_path)
        self.assertTrue(os.path.exists(save_path))

        loaded_rf = ModelRegistry.load_model(save_path)
        self.assertEqual(loaded_rf.algorithm_name, "Random Forest")
        loaded_preds = loaded_rf.predict(self.X_test)
        np.testing.assert_array_equal(preds, loaded_preds)

    def test_03_logistic_regression_lifecycle(self):
        """Test Logistic Regression training, evaluation, saving, and loading."""
        lr = LogisticRegressionNIDSModel({"C": 1.0, "max_iter": 200, "random_state": 42})
        self.assertEqual(lr.algorithm_name, "Logistic Regression")

        summary = lr.train(self.X_train, self.y_train, self.X_test, self.y_test)
        self.assertIn("train_accuracy", summary)
        self.assertTrue(summary.get("converged", False))

        preds = lr.predict(self.X_test)
        self.assertEqual(len(preds), len(self.y_test))
        probs = lr.predict_proba(self.X_test)
        self.assertEqual(probs.shape, (len(self.y_test), 2))

        save_path = os.path.join(self.temp_dir, "lr_standalone.pkl")
        lr.save(save_path)
        self.assertTrue(os.path.exists(save_path))

        loaded_lr = ModelRegistry.load_model(save_path)
        self.assertEqual(loaded_lr.algorithm_name, "Logistic Regression")
        loaded_preds = loaded_lr.predict(self.X_test)
        np.testing.assert_array_equal(preds, loaded_preds)

    def test_04_lstm_lifecycle(self):
        """Test LSTM / Neural Network training, evaluation, saving, and loading."""
        lstm = LSTMNIDSModel({"epochs": 5, "batch_size": 16, "learning_rate": 0.01, "random_state": 42})
        self.assertEqual(lstm.algorithm_name, "LSTM / Neural Network")

        progress_calls = []
        def on_progress(p):
            progress_calls.append(p)

        summary = lstm.train(self.X_train, self.y_train, self.X_test, self.y_test, progress_callback=on_progress)
        self.assertGreater(len(progress_calls), 0)
        self.assertIn("history", summary)
        self.assertIn("train_accuracy", summary)

        preds = lstm.predict(self.X_test)
        self.assertEqual(len(preds), len(self.y_test))
        probs = lstm.predict_proba(self.X_test)
        self.assertEqual(probs.shape, (len(self.y_test), 2))

        save_path = os.path.join(self.temp_dir, "lstm_standalone.pkl")
        lstm.save(save_path)
        self.assertTrue(os.path.exists(save_path))

        loaded_lstm = ModelRegistry.load_model(save_path)
        self.assertEqual(loaded_lstm.algorithm_name, "LSTM / Neural Network")
        loaded_preds = loaded_lstm.predict(self.X_test)
        np.testing.assert_array_equal(preds, loaded_preds)

    def test_05_mode_a_offline_benchmark_comparison(self):
        """Test Mode A offline benchmark comparison logic."""
        import joblib

        rf_dir = os.path.join(self.temp_dir, "rf_dir")
        lr_dir = os.path.join(self.temp_dir, "lr_dir")
        os.makedirs(rf_dir, exist_ok=True)
        os.makedirs(lr_dir, exist_ok=True)

        rf = RandomForestNIDSModel({"n_estimators": 10, "random_state": 42})
        rf.train(self.X_train, self.y_train)
        rf.save(os.path.join(rf_dir, "model.joblib"))

        lr = LogisticRegressionNIDSModel({"C": 1.0, "random_state": 42})
        lr.train(self.X_train, self.y_train)
        lr.save(os.path.join(lr_dir, "model.joblib"))

        scaler = StandardScaler()
        scaler.fit(self.X_train)
        joblib.dump(scaler, os.path.join(rf_dir, "scaler.pkl"))
        joblib.dump(scaler, os.path.join(lr_dir, "scaler.pkl"))

        # Save synthetic test dataset as CSV
        feature_cols = [f"f{i}" for i in range(10)]
        df_bench = pd.DataFrame(self.X_synthetic, columns=feature_cols)
        df_bench["label"] = self.y_synthetic
        test_csv_path = os.path.join(self.temp_dir, "bench_dataset.csv")
        df_bench.to_csv(test_csv_path, index=False)

        with self.app.app_context():
            ds = DatasetHistory(
                filename="bench_dataset.csv",
                dataset_type="CIC-IDS2017",
                filepath=test_csv_path,
                row_count=len(df_bench),
                col_count=len(df_bench.columns),
                target_col="label",
                is_selected=True
            )
            db.session.add(ds)
            db.session.commit()

            m1 = ModelHistory(
                model_name="RF Benchmark Model",
                dataset_name="bench_dataset.csv",
                accuracy=0.9,
                algorithm="random_forest",
                artifact_path=rf_dir,
                feature_names_json=json.dumps(feature_cols),
                is_active=True
            )
            m2 = ModelHistory(
                model_name="LR Benchmark Model",
                dataset_name="bench_dataset.csv",
                accuracy=0.85,
                algorithm="logistic_regression",
                artifact_path=lr_dir,
                feature_names_json=json.dumps(feature_cols),
                is_active=False
            )
            db.session.add(m1)
            db.session.add(m2)
            db.session.commit()
            m1_id, m2_id = m1.id, m2.id

            res = ModelComparisonService.compare_offline_benchmark(
                model_ids=[m1_id, m2_id],
                dataset_id=ds.id,
                test_samples_limit=50
            )

        self.assertIn("models", res)
        self.assertEqual(len(res["models"]), 2)
        for m_eval in res["models"]:
            self.assertIn("accuracy", m_eval)
            self.assertIn("precision", m_eval)
            self.assertIn("recall", m_eval)
            self.assertIn("f1_score", m_eval)
            self.assertIn("confusion_matrix", m_eval)
            self.assertIn("prediction_latency_ms", m_eval)
            self.assertIn("throughput_samples_sec", m_eval)

    def test_06_mode_b_live_session_comparison(self):
        """Test Mode B live session comparison on logged flows."""
        with self.app.app_context():
            models = ModelHistory.query.all()
            self.assertGreaterEqual(len(models), 2)
            m_ids = [m.id for m in models[:2]]

            for i in range(10):
                flow_feat = [float(self.X_test[i, j]) for j in range(10)]
                det = LiveDetection(
                    source_ip="192.168.1.100",
                    destination_ip="10.0.0.1",
                    source_port=50000 + i,
                    destination_port=80,
                    protocol="TCP",
                    risk_level="Low" if self.y_test[i] == 0 else "High",
                    prediction="Normal" if self.y_test[i] == 0 else "Attack",
                    confidence=0.95,
                    flow_features_json=json.dumps(flow_feat),
                    model_name="RF Benchmark Model"
                )
                db.session.add(det)
            db.session.commit()

            res = ModelComparisonService.compare_live_session(
                model_ids=m_ids,
                limit=10
            )

            self.assertIn("models", res)
            self.assertIn("agreement_matrix", res)
            self.assertIn("consensus_summary", res)
            self.assertEqual(res["total_flows"], 10)

    def test_07_model_api_endpoints(self):
        """Test model management REST API endpoints."""
        headers = {"Authorization": f"Bearer {self.admin_token}"}

        # 1. Supported models
        r1 = self.client.get("/api/models/supported", headers=headers)
        self.assertEqual(r1.status_code, 200)
        data1 = r1.get_json()
        self.assertIn("supported_models", data1)

        # 2. List all models
        r2 = self.client.get("/api/models", headers=headers)
        self.assertEqual(r2.status_code, 200)
        data2 = r2.get_json()
        self.assertIsInstance(data2, list)
        self.assertGreater(len(data2), 0)

        # 3. RBAC role-restriction check: User role should be denied Admin actions
        r_forbidden = self.client.delete("/api/models/99999", headers={"Authorization": f"Bearer {self.user_token}"})
        self.assertEqual(r_forbidden.status_code, 403)

        # 4. Analyst access check
        analyst_headers = {"Authorization": f"Bearer {self.analyst_token}"}
        r3 = self.client.get("/api/models", headers=analyst_headers)
        self.assertEqual(r3.status_code, 200)


if __name__ == "__main__":
    unittest.main()
