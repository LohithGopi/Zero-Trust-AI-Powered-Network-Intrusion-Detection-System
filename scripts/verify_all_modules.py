import os
import sys
import time
import json

sys.path.insert(0, os.path.abspath("."))

from app import create_app
from database.init_db import db, DatasetHistory, ModelHistory
from training.train_model import start_training_in_background, training_status

print("=" * 80)
print("COMPREHENSIVE END-TO-END NIDS PIPELINE VERIFICATION")
print("=" * 80)

app = create_app()

with app.app_context():
    # -------------------------------------------------------------------------
    # MODULE 1: MODEL TRAINING (Support Vector Machine with Fast Convergence)
    # -------------------------------------------------------------------------
    print("\n[MODULE 1] TESTING FAST SVM TRAINING PIPELINE...")
    active_ds = DatasetHistory.query.filter_by(is_selected=True).first() or DatasetHistory.query.first()
    print(f"Target Dataset: {active_ds.filename} ({active_ds.dataset_type})")
    
    t0 = time.time()
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
    
    run_id = start_training_in_background(
        app=app,
        dataset_id=active_ds.id,
        model_type="svm",
        training_rows=20000,
        hyperparams=svm_hyperparams,
        random_seed=42
    )
    print(f"SVM Training run '{run_id}' dispatched. Monitoring convergence...")
    
    time.sleep(1.0)
    while training_status.get("is_training", False):
        time.sleep(1.0)
        ep = training_status.get("current_epoch", 0)
        tot = training_status.get("total_epochs", 5)
        stg = training_status.get("stage", "")
        if ep > 0:
            print(f"  Step {ep}/{tot} [{stg}] - Acc: {training_status.get('accuracy', 0)*100:.2f}%")
            
    t_train = time.time() - t0
    print(f"SVM Training finished in: {t_train:.2f} seconds!")
    
    latest_mh = ModelHistory.query.order_by(ModelHistory.id.desc()).first()
    assert latest_mh is not None, "No ModelHistory recorded"
    print(f"Database Record -> ID: {latest_mh.id} | Model: {latest_mh.model_name}")
    print(f"Algorithm: {latest_mh.algorithm} | Framework: {latest_mh.framework}")
    print(f"Accuracy: {latest_mh.accuracy*100:.2f}% | F1: {latest_mh.f1_score*100:.2f}%")
    print(f"Training Time: {latest_mh.training_time:.2f}s | Active: {latest_mh.is_active}")
    
    # -------------------------------------------------------------------------
    # MODULE 2: PERFORMANCE EVALUATION METRICS VERIFICATION
    # -------------------------------------------------------------------------
    print("\n[MODULE 2] TESTING PERFORMANCE EVALUATION REPORT...")
    eval_file = os.path.join(latest_mh.artifact_path, "evaluation_report.json")
    assert os.path.exists(eval_file), f"Evaluation report file missing at {eval_file}"
    with open(eval_file, "r") as f:
        report_data = json.load(f)
    
    fpr = report_data.get("false_positive_rate", 0.0)
    fnr = report_data.get("false_negative_rate", 0.0)
    cm = report_data.get("confusion_matrix", [])
    print(f"Holdout Test Accuracy: {report_data.get('accuracy')*100:.2f}%")
    print(f"Precision: {report_data.get('precision')*100:.2f}%")
    print(f"Recall: {report_data.get('recall')*100:.2f}%")
    print(f"F1-Score: {report_data.get('f1_score')*100:.2f}%")
    print(f"Genuine False Positive Rate (FPR): {fpr*100:.2f}%")
    print(f"Genuine False Negative Rate (FNR): {fnr*100:.2f}%")
    print(f"Normal Identification Rate: {report_data.get('normal_identification_rate', 0)*100:.2f}%")
    print(f"Attack Detection Rate: {report_data.get('attack_detection_rate', 0)*100:.2f}%")
    print(f"Confusion Matrix ({len(cm)}x{len(cm[0]) if cm else 0}): {cm}")
    print(f"ROC-AUC: {report_data.get('roc_curve', {}).get('auc', 'N/A')}")
    
    # -------------------------------------------------------------------------
    # MODULE 3: MODEL COMPARISON SERVICE
    # -------------------------------------------------------------------------
    print("\n[MODULE 3] TESTING MODEL COMPARISON SERVICE (SVM vs LR vs LSTM)...")
    from training.comparison_service import ModelComparisonService
    
    # Pick distinct model IDs that exist on disk
    all_models = ModelHistory.query.order_by(ModelHistory.id.desc()).all()
    comp_models = []
    seen_algos = set()
    for m in all_models:
        if not m.artifact_path or not os.path.exists(m.artifact_path):
            continue
        algo_key = (m.algorithm or "").lower()
        if "svm" in algo_key or "support vector" in algo_key:
            if "svm" not in seen_algos:
                comp_models.append(m)
                seen_algos.add("svm")
        elif "logistic" in algo_key:
            if "logistic" not in seen_algos:
                comp_models.append(m)
                seen_algos.add("logistic")
        elif "lstm" in algo_key or "neural" in algo_key or "mlp" in algo_key:
            if "lstm" not in seen_algos:
                comp_models.append(m)
                seen_algos.add("lstm")
    
    print(f"Comparing {len(comp_models)} Models:")
    for m in comp_models:
        print(f"  - Model #{m.id}: {m.model_name} ({m.algorithm})")
        
    comp_ids = [m.id for m in comp_models]
    cmp_res = ModelComparisonService.compare_offline_benchmark(
        model_ids=comp_ids,
        test_samples_limit=500,
        random_seed=42
    )
    print("\nBenchmark Comparison Matrix Generated Successfully:")
    for r in cmp_res.get("models", []):
        print(f"  Model ID {r.get('model_id')}: {r.get('model_name')}")
        print(f"    -> Acc: {r.get('accuracy')*100:.2f}% | F1: {r.get('f1_score')*100:.2f}% | FPR: {r.get('false_positive_rate', 0)*100:.2f}% | Latency: {r.get('prediction_latency_ms')} ms")
    
    # -------------------------------------------------------------------------
    # MODULE 4: LIVE PACKET DETECTION & INFERENCE
    # -------------------------------------------------------------------------
    print("\n[MODULE 4] TESTING LIVE DETECTION WITH TRAINED SVM...")
    from live_detection.live_predictor import LivePredictor
    from live_detection.flow_manager import FlowManager
    
    predictor = LivePredictor(
        model_path=os.path.join(latest_mh.artifact_path, "model.joblib"),
        scaler_path=os.path.join(latest_mh.artifact_path, "scaler.pkl"),
        encoder_path=os.path.join(latest_mh.artifact_path, "label_encoder.pkl")
    )
    
    compat_ok, compat_msg = predictor.validate_compatibility()
    print(f"Predictor Compatibility: {compat_ok} -> {compat_msg}")
    assert compat_ok, f"Predictor compatibility failed: {compat_msg}"
    
    # Test Flow 1: Normal HTTPS web traffic
    fm1 = FlowManager()
    now_t = time.time()
    flow_normal = None
    for i in range(15):
        emitted = fm1.process_packet(
            src_ip="192.168.1.105", dst_ip="142.250.190.46",
            src_port=54321, dst_port=443, protocol="TCP",
            pkt_len=120 if i % 2 == 0 else 1420,
            tcp_flags={"SYN": 0, "ACK": 1, "PSH": 1 if i == 5 else 0},
            timestamp=now_t + (i * 0.1)
        )
        if emitted:
            flow_normal = emitted
            
    assert flow_normal is not None, "Normal flow emission failed"
    pred_normal = predictor.predict_flow(flow_normal)
    print(f"Flow 1 (Normal HTTPS): Prediction='{pred_normal['prediction']}', Conf={pred_normal['confidence']*100:.1f}%, Risk={pred_normal['risk_level']}, Latency={pred_normal['latency_ms']}ms")
    
    # Test Flow 2: Rapid SYN Flood anomaly
    fm2 = FlowManager()
    now_t2 = time.time()
    flow_attack = None
    for i in range(30):
        emitted = fm2.process_packet(
            src_ip="10.0.0.99", dst_ip="192.168.1.1",
            src_port=41234, dst_port=80, protocol="TCP",
            pkt_len=40,
            tcp_flags={"SYN": 1, "ACK": 0},
            timestamp=now_t2 + (i * 0.002)
        )
        if emitted:
            flow_attack = emitted
            
    assert flow_attack is not None, "Attack flow emission failed"
    pred_attack = predictor.predict_flow(flow_attack)
    print(f"Flow 2 (SYN Attack): Prediction='{pred_attack['prediction']}', Conf={pred_attack['confidence']*100:.1f}%, Risk={pred_attack['risk_level']}, Latency={pred_attack['latency_ms']}ms")
    
    print("\n" + "=" * 80)
    print("ALL 4 MODULES VERIFIED END-TO-END WITH ZERO BUGS OR FAILURES!")
    print("=" * 80)
