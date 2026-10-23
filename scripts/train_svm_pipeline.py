import sys
import os
import time

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app
from database.init_db import db, DatasetHistory, ModelHistory
from training.train_model import start_training_in_background, training_status

def main():
    print("=" * 80)
    print(">>> LAUNCHING SVM REPLACEMENT TRAINING PIPELINE")
    print("=" * 80)

    app = create_app()
    with app.app_context():
        # Identify active dataset
        active_ds = DatasetHistory.query.filter_by(is_selected=True).first()
        if not active_ds:
            active_ds = DatasetHistory.query.first()

        print(f"[1/4] Target Dataset: {active_ds.filename} ({active_ds.dataset_type})")
        print(f"[2/4] Initializing SVM Model Training on {active_ds.dataset_type} with 20,000 stratified samples...")

        # Hyperparameters for SVM with RBF kernel and Platt probability calibration
        svm_hyperparams = {
            "C": 1.0,
            "kernel": "rbf",
            "gamma": "scale",
            "class_weight": "balanced",
            "probability": True,
            "cache_size": 1000,
            "tol": 0.01,
            "random_state": 42
        }

        # Start background training thread
        run_id = start_training_in_background(
            app=app,
            dataset_id=active_ds.id,
            model_type="svm",
            training_rows=20000,
            hyperparams=svm_hyperparams,
            random_seed=42
        )

        print(f"[3/4] SVM Training run '{run_id}' launched. Awaiting convergence...")

        # Monitor progress until finished
        time.sleep(1.0)
        last_epoch = -1
        while training_status.get("is_training", False):
            time.sleep(1.5)
            cur_epoch = training_status.get("current_epoch", 0)
            tot_epoch = training_status.get("total_epochs", 5)
            stage = training_status.get("stage", "working")
            msg = training_status.get("message", "")
            if cur_epoch != last_epoch and cur_epoch > 0:
                print(f"  [Progress] Step {cur_epoch}/{tot_epoch} | Stage: {stage} | {msg}")
                last_epoch = cur_epoch

        print("-" * 80)
        print("[4/4] Training Complete! Fetching latest ModelHistory from database...")
        latest_mh = ModelHistory.query.order_by(ModelHistory.id.desc()).first()
        if latest_mh:
            print(f"Model ID: {latest_mh.id}")
            print(f"Model Name: {latest_mh.model_name}")
            print(f"Algorithm: {latest_mh.algorithm}")
            print(f"Framework: {latest_mh.framework}")
            print(f"Accuracy: {latest_mh.accuracy * 100:.2f}%")
            print(f"Precision: {latest_mh.precision * 100:.2f}%")
            print(f"Recall: {latest_mh.recall * 100:.2f}%")
            print(f"F1-Score: {latest_mh.f1_score * 100:.2f}%")
            print(f"Training Time: {latest_mh.training_time:.2f}s")
            print(f"Is Active: {latest_mh.is_active}")
            print(f"Artifact Dir: {latest_mh.artifact_path}")
        else:
            print("[Warning] No ModelHistory record found.")

    print("=" * 80)

if __name__ == "__main__":
    main()
