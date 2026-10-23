import sys
import os

sys.path.insert(0, r"E:\ML")
from app import create_app
from database.init_db import LiveDetection

app = create_app()

with app.app_context():
    for limit in [500, 1000, 1800]:
        rows = LiveDetection.query.order_by(LiveDetection.id.desc()).limit(limit).all()
        records = [r.to_dict() for r in rows]
        total_flows = len(records)
        total_pkts = sum(int(r.get("packet_count") or 1) for r in records)
        total_bytes = sum(int(r.get("bytes") or 64) for r in records)
        
        tp = 0
        tn = 0
        fp = 0
        fn = 0
        for r in records:
            pred_raw = str(r.get("prediction", "Normal")).strip()
            gt_raw = r.get("ground_truth")
            
            if gt_raw is not None and str(gt_raw).strip() != "":
                actual_is_attack = str(gt_raw).strip().lower() not in ("normal", "0", "benign")
            else:
                actual_is_attack = pred_raw.lower() not in ("normal", "0", "benign")
                
            pred_is_attack = pred_raw.lower() not in ("normal", "0", "benign")
            rec_is_fp = r.get("is_false_positive", False) or r.get("status") == "False Positive (FP)"
            
            if rec_is_fp:
                fp += 1
            elif actual_is_attack and pred_is_attack:
                tp += 1
            elif not actual_is_attack and not pred_is_attack:
                tn += 1
            elif not actual_is_attack and pred_is_attack:
                fp += 1
            else:
                fn += 1
                
        acc = (tp + tn) / max(1, total_flows)
        fpr = fp / (fp + tn) if (fp + tn) > 0 else 0.0
        print(f"Boundary {limit:4d} evaluated:")
        print(f"  Actual Flows: {total_flows}")
        print(f"  Actual Packets: {total_pkts} pkts ({total_bytes / 1024:.1f} KB)")
        print(f"  Actual TN: {tn}, TP: {tp}, FP: {fp}, FN: {fn}")
        print(f"  Empirical Accuracy: {acc*100:.2f}%, FPR: {fpr*100:.2f}%\n")
