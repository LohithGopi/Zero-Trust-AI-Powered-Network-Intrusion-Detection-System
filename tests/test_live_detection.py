import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import unittest
import numpy as np
from app import create_app
from database.init_db import db, LiveDetection
from live_detection.flow_manager import FlowManager, NetworkFlow
from live_detection.feature_extractor import FlowFeatureExtractor
from live_detection.live_predictor import LivePredictor
from live_detection.detection_logger import DetectionLogger
from live_detection.packet_capture import (
    get_available_interfaces,
    check_npcap_capability,
    PacketCaptureManager
)
from security.jwt_auth import generate_token


class TestLiveDetectionSystem(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.app.config["TESTING"] = True
        cls.client = cls.app.test_client()

        from database.init_db import ModelHistory
        with cls.app.app_context():
            db.create_all()
            cls._backup_models = []
            for m in ModelHistory.query.all():
                cls._backup_models.append({
                    "model_name": m.model_name,
                    "dataset_name": m.dataset_name,
                    "trained_at": m.trained_at,
                    "accuracy": m.accuracy,
                    "loss": m.loss,
                    "precision": m.precision,
                    "recall": m.recall,
                    "f1_score": m.f1_score,
                    "training_time": m.training_time,
                    "prediction_time": m.prediction_time,
                    "model_type": m.model_type,
                    "framework": m.framework,
                    "model_status": m.model_status,
                    "params_json": m.params_json,
                    "artifact_path": m.artifact_path,
                    "total_dataset_rows": m.total_dataset_rows,
                    "training_rows": m.training_rows,
                    "random_seed": m.random_seed
                })

        # Generate test JWT tokens
        cls.admin_token = generate_token(user_id=1, username="admin", role="Admin")
        cls.analyst_token = generate_token(user_id=2, username="analyst", role="Analyst")
        cls.user_token = generate_token(user_id=3, username="testuser", role="User")

    def test_01_interface_discovery(self):
        interfaces = get_available_interfaces()
        self.assertIsInstance(interfaces, list)
        self.assertGreater(len(interfaces), 0)
        first = interfaces[0]
        self.assertIn("id", first)
        self.assertIn("name", first)
        self.assertIn("ip", first)

    def test_02_npcap_capability_check(self):
        status = check_npcap_capability()
        self.assertIn("available", status)
        self.assertIn("message", status)
        self.assertIsInstance(status["available"], bool)

    def test_03_flow_manager_bidirectional_aggregation(self):
        fm = FlowManager(idle_timeout=2.0, live_packet_threshold=10)

        # Forward packets (client -> server)
        for i in range(5):
            emitted = fm.process_packet(
                src_ip="192.168.1.100",
                dst_ip="93.184.216.34",
                src_port=49152,
                dst_port=80,
                protocol="TCP",
                pkt_len=60,
                tcp_flags={"SYN": 1 if i == 0 else 0, "ACK": 1 if i > 0 else 0}
            )
            self.assertIsNone(emitted)

        # Reverse packets (server -> client)
        for j in range(5):
            emitted = fm.process_packet(
                src_ip="93.184.216.34",
                dst_ip="192.168.1.100",
                src_port=80,
                dst_port=49152,
                protocol="TCP",
                pkt_len=1460,
                tcp_flags={"SYN": 1 if j == 0 else 0, "ACK": 1}
            )

        # Batch threshold (10 packets) reached
        self.assertIsNotNone(emitted)
        self.assertEqual(emitted.total_packets, 10)
        self.assertEqual(emitted.fwd_packets, 5)
        self.assertEqual(emitted.bwd_packets, 5)
        self.assertEqual(emitted.fwd_bytes, 5 * 60)
        self.assertEqual(emitted.bwd_bytes, 5 * 1460)

    def test_04_feature_extraction_schemas(self):
        extractor = FlowFeatureExtractor()
        flow = NetworkFlow(
            src_ip="10.0.0.5",
            dst_ip="10.0.0.1",
            src_port=53210,
            dst_port=443,
            protocol="TCP",
            start_time=100.0,
            last_time=101.5,
            fwd_packets=8,
            bwd_packets=6,
            fwd_bytes=1200,
            bwd_bytes=4500,
            fwd_lengths=[150] * 8,
            bwd_lengths=[750] * 6,
            packet_times=[100.0, 100.2, 100.5, 101.0, 101.5]
        )

        # 1. CIC-IDS2017 (22 features)
        cic_feats = extractor.extract(flow, "CIC-IDS2017")
        self.assertEqual(cic_feats.shape, (1, 22))

        # 2. UNSW-NB15 (15 features)
        unsw_feats = extractor.extract(flow, "UNSW-NB15")
        self.assertEqual(unsw_feats.shape, (1, 15))

        # 3. NSL-KDD (19 features)
        nsl_feats = extractor.extract(flow, "NSL-KDD")
        self.assertEqual(nsl_feats.shape, (1, 19))

    def test_05_untrained_model_guard(self):
        from database.init_db import ModelHistory
        with self.app.app_context():
            ModelHistory.query.delete()
            db.session.commit()

        # 1. Verify models endpoint returns null active model when no model is trained
        res_models = self.client.get(
            "/api/live-detection/models",
            headers={"Authorization": f"Bearer {self.admin_token}"}
        )
        self.assertEqual(res_models.status_code, 200)
        data = res_models.get_json()
        self.assertIsNone(data["active_model"])
        self.assertFalse(data["has_trained_model"])
        self.assertEqual(len(data["models"]), 0)

        # 2. Verify LivePredictor raises FileNotFoundError when no model is trained
        with self.assertRaises(FileNotFoundError):
            LivePredictor()

        # 3. Verify start capture fails with error when no model is trained
        res_start = self.client.post(
            "/api/live-detection/start",
            headers={"Authorization": f"Bearer {self.admin_token}"},
            json={"interface_id": "default", "mode": "simulated"}
        )
        self.assertEqual(res_start.status_code, 400)
        self.assertIn("No detection model trained", res_start.get_json().get("error", ""))

    def test_05b_trained_model_activation_and_inference(self):
        import joblib
        from sklearn.neural_network import MLPClassifier
        from sklearn.preprocessing import StandardScaler, LabelEncoder
        from database.init_db import ModelHistory
        from datetime import datetime

        # Create a test trained model artifact directory
        test_dir = os.path.abspath(os.path.join("models", "test_run"))
        os.makedirs(test_dir, exist_ok=True)

        X_dummy = np.random.randn(20, 22).astype(np.float32)
        y_dummy = np.array([0] * 10 + [1] * 10)

        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X_dummy)
        encoder = LabelEncoder()
        encoder.classes_ = np.array(["BENIGN", "DDoS"])

        mlp = MLPClassifier(hidden_layer_sizes=(16,), max_iter=2, random_state=42)
        mlp.fit(X_scaled, y_dummy)

        joblib.dump(mlp, os.path.join(test_dir, "model.joblib"))
        joblib.dump(scaler, os.path.join(test_dir, "scaler.pkl"))
        joblib.dump(encoder, os.path.join(test_dir, "encoder.pkl"))

        # Register in ModelHistory
        with self.app.app_context():
            mh = ModelHistory(
                model_name="Neural Network NIDS (CIC-IDS2017 test)",
                dataset_name="cicids2017_raw.csv",
                trained_at=datetime.utcnow(),
                accuracy=0.95,
                loss=0.12,
                precision=0.94,
                recall=0.95,
                f1_score=0.945,
                artifact_path=test_dir,
                model_type="Deep Learning",
                model_status="Trained"
            )
            db.session.add(mh)
            db.session.commit()

        # Verify models endpoint returns this trained model
        res_models = self.client.get(
            "/api/live-detection/models",
            headers={"Authorization": f"Bearer {self.admin_token}"}
        )
        self.assertEqual(res_models.status_code, 200)
        data = res_models.get_json()
        self.assertTrue(data["has_trained_model"])
        self.assertIsNotNone(data["active_model"])
        self.assertEqual(data["active_model"]["dataset_type"], "CIC-IDS2017")
        self.assertEqual(data["active_model"]["features"], 22)

        # Predict flow using the registered trained model
        predictor = LivePredictor(
            model_path=os.path.join(test_dir, "model.joblib"),
            scaler_path=os.path.join(test_dir, "scaler.pkl"),
            encoder_path=os.path.join(test_dir, "encoder.pkl")
        )
        flow = NetworkFlow(
            src_ip="192.168.1.10",
            dst_ip="1.1.1.1",
            src_port=51200,
            dst_port=53,
            protocol="UDP",
            start_time=200.0,
            last_time=200.05,
            fwd_packets=2,
            bwd_packets=2,
            fwd_bytes=128,
            bwd_bytes=256
        )

        res = predictor.predict_flow(flow)
        self.assertIn("prediction", res)
        self.assertIn("confidence", res)
        self.assertIn("risk_level", res)
        self.assertIn(res["risk_level"], ["LOW", "MEDIUM", "HIGH"])
        self.assertGreaterEqual(res["confidence"], 0.0)
        self.assertLessEqual(res["confidence"], 1.0)

    def test_06_detection_logger_and_db(self):
        logger = DetectionLogger(memory_buffer_size=10)
        flow = NetworkFlow(
            src_ip="172.16.0.4",
            dst_ip="172.16.0.1",
            src_port=3306,
            dst_port=50000,
            protocol="TCP",
            start_time=300.0,
            last_time=301.0,
            fwd_packets=4,
            bwd_packets=3,
            fwd_bytes=500,
            bwd_bytes=800
        )
        pred_res = {
            "prediction": "Normal",
            "confidence": 0.985,
            "risk_level": "LOW",
            "is_attack": False
        }

        entry = logger.record_detection(self.app, flow, pred_res, interface="TestAdapter")
        self.assertEqual(entry["prediction"], "Normal")
        self.assertEqual(entry["risk_level"], "LOW")
        self.assertEqual(len(logger.get_recent_detections()), 1)

        # Check SQLite persistence
        with self.app.app_context():
            db_row = LiveDetection.query.filter_by(source_ip="172.16.0.4").first()
            self.assertIsNotNone(db_row)
            self.assertEqual(db_row.destination_ip, "172.16.0.1")

    def test_07_controlled_replay_mode(self):
        mgr = PacketCaptureManager()
        replay_res = mgr.replay_test_traffic(self.app, count=5)
        self.assertTrue(replay_res["success"])
        self.assertGreater(replay_res["emitted_flows"], 0)

        stats = mgr.logger.get_live_stats()
        self.assertGreater(stats["total_flows"], 0)
        self.assertGreater(stats["total_packets"], 0)

    def test_08_api_role_access_control(self):
        # 1. Admin allowed
        res_admin = self.client.get(
            "/api/live-detection/interfaces",
            headers={"Authorization": f"Bearer {self.admin_token}"}
        )
        self.assertEqual(res_admin.status_code, 200)

        # 2. Analyst allowed
        res_analyst = self.client.get(
            "/api/live-detection/interfaces",
            headers={"Authorization": f"Bearer {self.analyst_token}"}
        )
        self.assertEqual(res_analyst.status_code, 200)

        # 3. User role forbidden (allowed only Admin and Analyst)
        res_user = self.client.get(
            "/api/live-detection/interfaces",
            headers={"Authorization": f"Bearer {self.user_token}"}
        )
        self.assertEqual(res_user.status_code, 403)
        self.assertIn("Role restriction", res_user.get_json()["error"])

    def test_09_api_traffic_feed_and_csv_export(self):
        # Poll traffic feed
        res_feed = self.client.get(
            "/api/live-detection/traffic",
            headers={"Authorization": f"Bearer {self.analyst_token}"}
        )
        self.assertEqual(res_feed.status_code, 200)
        feed_data = res_feed.get_json()
        self.assertIn("detections", feed_data)
        self.assertIn("stats", feed_data)

        # Test CSV export
        res_csv = self.client.get(
            "/api/live-detection/export",
            headers={"Authorization": f"Bearer {self.admin_token}"}
        )
        self.assertEqual(res_csv.status_code, 200)
        self.assertEqual(res_csv.content_type, "text/csv; charset=utf-8")
        self.assertIn("source_ip,destination_ip", res_csv.get_data(as_text=True))

    def test_10_simulated_stream_capture(self):
        # Test starting live detection in simulated stream mode (zero-permission)
        res_start = self.client.post(
            "/api/live-detection/start",
            headers={"Authorization": f"Bearer {self.admin_token}"},
            json={"interface_id": "default", "mode": "simulated"}
        )
        self.assertEqual(res_start.status_code, 200)
        start_data = res_start.get_json()
        self.assertTrue(start_data["success"])
        self.assertEqual(start_data.get("mode"), "simulated")

        # Verify status endpoint reflects simulated active monitoring
        res_status = self.client.get(
            "/api/live-detection/status",
            headers={"Authorization": f"Bearer {self.admin_token}"}
        )
        self.assertEqual(res_status.status_code, 200)
        status_data = res_status.get_json()
        self.assertTrue(status_data["status"]["is_running"])
        self.assertEqual(status_data["status"]["mode"], "simulated")

        # Stop monitoring safely
        res_stop = self.client.post(
            "/api/live-detection/stop",
            headers={"Authorization": f"Bearer {self.admin_token}"}
        )
        self.assertEqual(res_stop.status_code, 200)
        self.assertTrue(res_stop.get_json()["success"])

    def test_11_remove_active_detection_model(self):
        # Remove the active detection model via POST /api/live-detection/models/remove
        res_rem = self.client.post(
            "/api/live-detection/models/remove",
            headers={"Authorization": f"Bearer {self.admin_token}"},
            json={"model_id": "all"}
        )
        self.assertEqual(res_rem.status_code, 200)
        rem_data = res_rem.get_json()
        self.assertTrue(rem_data["success"])
        self.assertIsNone(rem_data["active_model"])
        self.assertFalse(rem_data["has_trained_model"])
        self.assertEqual(len(rem_data["models"]), 0)


    @classmethod
    def tearDownClass(cls):
        import shutil
        from database.init_db import ModelHistory
        with cls.app.app_context():
            ModelHistory.query.delete()
            for row in getattr(cls, "_backup_models", []):
                db.session.add(ModelHistory(**row))
            db.session.commit()

        test_dir = os.path.abspath(os.path.join("models", "test_run"))
        if os.path.exists(test_dir):
            shutil.rmtree(test_dir, ignore_errors=True)


if __name__ == "__main__":
    unittest.main()

