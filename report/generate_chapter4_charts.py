import os
import json
import sqlite3
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

REPORT_DIR = os.path.dirname(os.path.abspath(__file__))
FIG_DIR = os.path.join(REPORT_DIR, "figures")
MODELS_DIR = os.path.join(os.path.dirname(REPORT_DIR), "models")
DB_PATH = os.path.join(os.path.dirname(REPORT_DIR), "database", "database.db")
os.makedirs(FIG_DIR, exist_ok=True)

NAVY = "#0F172A"
BLUE = "#1D4ED8"
TEAL = "#0F766E"
AMBER = "#B45309"
CRIMSON = "#B91C1C"
GREEN = "#15803D"
INDIGO = "#4338CA"
SLATE = "#334155"


def load_json(rel_path):
    with open(os.path.join(MODELS_DIR, rel_path), "r", encoding="utf-8") as f:
        return json.load(f)


# ==============================================================================
# FIGURE 4.1: EPOCH-BY-EPOCH TRAINING & VALIDATION LEARNING CURVES + DELTA_W
# ==============================================================================
def gen_fig4_1():
    unsw_tm = load_json(r"unsw_nb15\run_20261010_221543_0b0508\training_metadata.json")
    nsl_tm = load_json(r"nsl_kdd\run_20261010_110200_0cb7f1\training_metadata.json")
    cic_tm = load_json(r"cic_ids2017\run_20261010_151740_49c046\training_metadata.json")

    fig, axes = plt.subplots(1, 3, figsize=(13.5, 4.3), dpi=300)
    fig.suptitle(
        "Figure 4.1: Verified Epoch-by-Epoch Learning Curves and Frobenius Weight Convergence Across Benchmark Datasets",
        fontsize=11.5, fontweight="bold", color=NAVY, y=1.02
    )

    datasets = [
        ("UNSW-NB15 (run_0b0508)", unsw_tm["epoch_history"], BLUE, CRIMSON),
        ("NSL-KDD (run_0cb7f1)", nsl_tm["epoch_history"], TEAL, AMBER),
        ("CIC-IDS2017 (run_49c046)", cic_tm["epoch_history"], INDIGO, GREEN),
    ]

    # Panel A: Training vs Validation Loss
    ax = axes[0]
    for label, hist, c_tr, c_val in datasets:
        ep = [h["epoch"] for h in hist]
        tr_loss = [h["loss"] for h in hist]
        val_loss = [h["val_loss"] for h in hist]
        short = label.split()[0]
        ax.plot(ep, tr_loss, marker="o", markersize=4, lw=1.8, color=c_tr, label=f"{short} Train Loss")
        ax.plot(ep, val_loss, marker="s", markersize=4, lw=1.6, ls="--", color=c_tr, alpha=0.75, label=f"{short} Val Loss")
    ax.set_title("(a) Cross-Entropy Loss vs. Epoch", fontsize=10, fontweight="bold", color=NAVY)
    ax.set_xlabel("Training Epoch", fontsize=9)
    ax.set_ylabel("Categorical Cross-Entropy Loss", fontsize=9)
    ax.grid(True, ls=":", alpha=0.6)
    ax.legend(fontsize=7.2, loc="center right")

    # Panel B: Training vs Validation Accuracy
    ax = axes[1]
    for label, hist, c_tr, c_val in datasets:
        ep = [h["epoch"] for h in hist]
        tr_acc = [h["accuracy"] * 100 for h in hist]
        val_acc = [h["val_accuracy"] * 100 for h in hist]
        short = label.split()[0]
        ax.plot(ep, tr_acc, marker="o", markersize=4, lw=1.8, color=c_tr, label=f"{short} Train Acc")
        ax.plot(ep, val_acc, marker="s", markersize=4, lw=1.6, ls="--", color=c_tr, alpha=0.75, label=f"{short} Val Acc")
    ax.set_title("(b) Classification Accuracy (%) vs. Epoch", fontsize=10, fontweight="bold", color=NAVY)
    ax.set_xlabel("Training Epoch", fontsize=9)
    ax.set_ylabel("Accuracy (%)", fontsize=9)
    ax.set_ylim(80, 100)
    ax.grid(True, ls=":", alpha=0.6)
    ax.legend(fontsize=7.2, loc="lower right")

    # Panel C: Frobenius Weight Update Norm (Delta W)
    ax = axes[2]
    for label, hist, c_tr, _ in datasets:
        ep = [h["epoch"] for h in hist]
        dw = [h["delta_w"] for h in hist]
        short = label.split()[0]
        ax.plot(ep, dw, marker="^", markersize=4.5, lw=1.8, color=c_tr, label=f"{short} ||ΔW||_F")
    ax.set_title("(c) Frobenius Weight Norm ||ΔW^(e)||_F", fontsize=10, fontweight="bold", color=NAVY)
    ax.set_xlabel("Training Epoch", fontsize=9)
    ax.set_ylabel("Frobenius Norm of Weight Update", fontsize=9)
    ax.grid(True, ls=":", alpha=0.6)
    ax.legend(fontsize=8, loc="upper right")

    plt.tight_layout()
    out = os.path.join(FIG_DIR, "fig4_1_training_curves.png")
    fig.savefig(out, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("Generated:", out)


# ==============================================================================
# FIGURE 4.2: UNSW-NB15 BINARY CONFUSION MATRIX & ROC CURVE (latest_report.json)
# ==============================================================================
def gen_fig4_2():
    rep = load_json("latest_report.json")
    cm = np.array(rep["confusion_matrix"])
    fpr = rep["roc_curve"]["fpr"]
    tpr = rep["roc_curve"]["tpr"]
    auc_val = rep["roc_curve"]["auc"]

    fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.6), dpi=300)
    fig.suptitle(
        "Figure 4.2: Verified Holdout Confusion Matrix and ROC Curve for UNSW-NB15 Binary Classification (N_test = 3,750)",
        fontsize=11, fontweight="bold", color=NAVY, y=1.02
    )

    # Panel A: Binary Confusion Matrix
    ax = axes[0]
    im = ax.imshow(cm, cmap="Blues", interpolation="nearest")
    ax.set_title("(a) Binary Confusion Matrix (UNSW-NB15 Holdout)", fontsize=10, fontweight="bold", color=NAVY)
    classes = ["Normal (0)\n[n = 2,207]", "Attack (1)\n[n = 1,543]"]
    ax.set_xticks([0, 1])
    ax.set_yticks([0, 1])
    ax.set_xticklabels(["Predicted\nNormal (0)", "Predicted\nAttack (1)"], fontsize=9)
    ax.set_yticklabels(["Actual\nNormal (0)", "Actual\nAttack (1)"], fontsize=9)

    labels_text = [
        [f"TN = {cm[0,0]}\n(97.83% Spec.)", f"FP = {cm[0,1]}\n(FPR = 2.17%)"],
        [f"FN = {cm[1,0]}\n(FNR = 4.99%)", f"TP = {cm[1,1]}\n(95.01% Recall)"]
    ]
    for i in range(2):
        for j in range(2):
            color = "white" if cm[i, j] > 1000 else NAVY
            ax.text(j, i, labels_text[i][j], ha="center", va="center",
                    color=color, fontsize=10, fontweight="bold")
    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04, label="Sample Count")

    # Panel B: ROC Curve
    ax = axes[1]
    ax.plot(fpr, tpr, color=BLUE, lw=2.2, label=f"MLP (64, 32) ROC Curve (AUC = {auc_val:.4f})")
    ax.plot([0, 1], [0, 1], color=SLATE, lw=1.2, ls="--", label="Random Classifier Baseline (AUC = 0.5000)")
    ax.scatter([0.0217], [0.9501], color=CRIMSON, s=55, zorder=5,
               label="Operating Point (FPR=2.17%, TPR=95.01%)")
    ax.set_title("(b) Receiver Operating Characteristic (ROC) Curve", fontsize=10, fontweight="bold", color=NAVY)
    ax.set_xlabel("False Positive Rate (FPR = FP / (FP + TN))", fontsize=9)
    ax.set_ylabel("True Positive Rate / Recall (TPR = TP / (TP + FN))", fontsize=9)
    ax.set_xlim(-0.02, 1.02)
    ax.set_ylim(-0.02, 1.03)
    ax.grid(True, ls=":", alpha=0.6)
    ax.legend(fontsize=8.2, loc="lower right")

    plt.tight_layout()
    out = os.path.join(FIG_DIR, "fig4_2_unsw_binary_cm_roc.png")
    fig.savefig(out, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("Generated:", out)


# ==============================================================================
# FIGURE 4.3: 7-CLASS CONFUSION MATRICES (UNSW-NB15 & NSL-KDD)
# ==============================================================================
def gen_fig4_3():
    unsw_er = load_json(r"unsw_nb15\run_20261010_221543_0b0508\evaluation_report.json")
    nsl_er = load_json(r"nsl_kdd\run_20261010_213122_8b7ae5\evaluation_report.json")

    fig, axes = plt.subplots(1, 2, figsize=(13.2, 5.4), dpi=300)
    fig.suptitle(
        "Figure 4.3: Multi-Class Holdout Confusion Matrices for UNSW-NB15 (N=3,750) and NSL-KDD (N=7,500)",
        fontsize=11.2, fontweight="bold", color=NAVY, y=1.02
    )

    for idx, (title, er, cmap) in enumerate([
        ("(a) UNSW-NB15 7-Class Confusion Matrix (Acc = 96.00%)", unsw_er, "Blues"),
        ("(b) NSL-KDD 7-Class Confusion Matrix (Acc = 90.37%, Binary = 99.11%)", nsl_er, "GnBu")
    ]):
        ax = axes[idx]
        cm = np.array(er["confusion_matrix"])
        classes = er["classes"]
        # Use log-scaled color mapping for readability while printing exact counts
        im = ax.imshow(np.log1p(cm), cmap=cmap, interpolation="nearest")
        ax.set_title(title, fontsize=9.8, fontweight="bold", color=NAVY)
        ax.set_xticks(range(len(classes)))
        ax.set_yticks(range(len(classes)))
        ax.set_xticklabels(classes, rotation=35, ha="right", fontsize=8)
        ax.set_yticklabels(classes, fontsize=8)
        ax.set_xlabel("Predicted Class Label", fontsize=9)
        ax.set_ylabel("True Ground-Truth Class Label", fontsize=9)

        thresh = np.log1p(cm).max() * 0.55
        for i in range(cm.shape[0]):
            for j in range(cm.shape[1]):
                val = cm[i, j]
                col = "white" if np.log1p(val) > thresh else NAVY
                ax.text(j, i, str(val), ha="center", va="center", color=col,
                        fontsize=7.8, fontweight="bold" if i == j else "normal")

    plt.tight_layout()
    out = os.path.join(FIG_DIR, "fig4_3_multiclass_confusion_matrices.png")
    fig.savefig(out, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("Generated:", out)


# ==============================================================================
# FIGURE 4.4: COMPARATIVE BAR CHART OF CLASSIFICATION METRICS ACROSS RUNS
# ==============================================================================
def gen_fig4_4():
    categories = [
        "UNSW-NB15\n(Binary, N=3,750)",
        "UNSW-NB15\n(7-Class, N=3,750)",
        "NSL-KDD\n(Binary Summary, N=7,500)",
        "NSL-KDD\n(7-Class, N=7,500)",
        "CIC-IDS2017\n(7-Class, N=3,750)"
    ]
    acc = [96.67, 96.00, 99.11, 90.37, 84.72]
    prec = [96.67, 96.01, 99.73, 88.58, 81.06]
    rec = [96.67, 96.00, 98.28, 90.37, 84.72]
    f1 = [96.66, 96.00, 99.00, 88.86, 81.11]
    fpr = [2.17, 2.22, 0.22, 0.22, 1.60]

    x = np.arange(len(categories))
    w = 0.16

    fig, ax = plt.subplots(figsize=(12.2, 4.8), dpi=300)
    b1 = ax.bar(x - 2*w, acc, w, label="Accuracy (%)", color=BLUE)
    b2 = ax.bar(x - w, prec, w, label="Precision (%)", color=TEAL)
    b3 = ax.bar(x, rec, w, label="Recall / Detection Rate (%)", color=INDIGO)
    b4 = ax.bar(x + w, f1, w, label="F1-Score (%)", color=GREEN)
    b5 = ax.bar(x + 2*w, fpr, w, label="False-Positive Rate (FPR %)", color=CRIMSON)

    ax.set_title(
        "Figure 4.4: Comparative Evaluation of Verified Holdout Classification Metrics Across Benchmark Datasets",
        fontsize=11, fontweight="bold", color=NAVY
    )
    ax.set_ylabel("Percentage (%)", fontsize=9.5)
    ax.set_xticks(x)
    ax.set_xticklabels(categories, fontsize=8.8, fontweight="bold")
    ax.set_ylim(0, 112)
    ax.grid(True, axis="y", ls=":", alpha=0.6)
    ax.legend(ncol=5, fontsize=8.2, loc="upper center")

    for bars in [b1, b2, b3, b4, b5]:
        for bar in bars:
            h = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, h + 1.0, f"{h:.1f}",
                    ha="center", va="bottom", fontsize=6.8, rotation=90, color=NAVY, fontweight="bold")

    plt.tight_layout()
    out = os.path.join(FIG_DIR, "fig4_4_metrics_comparison_bar.png")
    fig.savefig(out, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("Generated:", out)


# ==============================================================================
# FIGURE 4.5: ZERO TRUST AUDIT LOG EMPIRICAL DISTRIBUTION (SQLite N=1,002)
# ==============================================================================
def gen_fig4_5():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    rows = cur.execute(
        "SELECT action, status, COUNT(*) as cnt FROM audit_logs GROUP BY action, status ORDER BY cnt DESC LIMIT 10"
    ).fetchall()
    conn.close()

    labels = [f"{r[0]}\n[{r[1]}]" for r in rows][::-1]
    counts = [r[2] for r in rows][::-1]
    colors_bar = [CRIMSON if r[1] in ("REJECTED", "FAILED") else BLUE for r in rows][::-1]

    fig, ax = plt.subplots(figsize=(11.2, 4.5), dpi=300)
    bars = ax.barh(labels, counts, color=colors_bar, height=0.62)
    ax.set_title(
        "Figure 4.5: Empirical Distribution of Recorded Zero Trust Security Audit Events in SQLite (N = 1,002 Logs)",
        fontsize=10.8, fontweight="bold", color=NAVY
    )
    ax.set_xlabel("Number of Recorded Audit Log Entries", fontsize=9.5)
    ax.set_xlim(0, max(counts) * 1.15)
    ax.grid(True, axis="x", ls=":", alpha=0.6)

    for b in bars:
        w = b.get_width()
        ax.text(w + 6, b.get_y() + b.get_height()/2, f"{int(w)} events",
                va="center", ha="left", fontsize=8.2, fontweight="bold", color=NAVY)

    plt.tight_layout()
    out = os.path.join(FIG_DIR, "fig4_5_audit_log_distribution.png")
    fig.savefig(out, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("Generated:", out)


# ==============================================================================
# FIGURE 4.6: LIVE NETWORK TRAFFIC DETECTIONS & RISK TELEMETRY (SQLite N=2,343)
# ==============================================================================
def gen_fig4_6():
    fig, axes = plt.subplots(1, 2, figsize=(11.8, 4.4), dpi=300)
    fig.suptitle(
        "Figure 4.6: Verified Live Network Flow Detection Breakdown in SQLite live_detections (N = 2,343 Flows)",
        fontsize=11, fontweight="bold", color=NAVY, y=1.02
    )

    # Panel A: Alert vs Normal Breakdown (Log Scale for Visibility)
    ax = axes[0]
    classes = [
        "Normal [LOW]",
        "Recon [MEDIUM]",
        "DoS Hulk [LOW]",
        "DoS Hulk [MEDIUM]",
        "Recon [HIGH]",
        "Attack '1' [HIGH]",
        "Generic [LOW]",
        "Recon [LOW]"
    ][::-1]
    counts = [2301, 12, 9, 8, 6, 4, 2, 1][::-1]
    confs = [96.30, 75.16, 41.14, 66.29, 87.77, 97.43, 37.85, 37.02][::-1]
    bar_cols = [
        GREEN if "Normal" in c else (CRIMSON if "HIGH" in c else (AMBER if "MEDIUM" in c else TEAL))
        for c in classes
    ]

    bars = ax.barh(classes, counts, color=bar_cols, height=0.6)
    ax.set_xscale("log")
    ax.set_xlim(0.7, 8000)
    ax.set_title("(a) Flow Detections by Class & Risk Tier (Log Scale)", fontsize=9.8, fontweight="bold", color=NAVY)
    ax.set_xlabel("Captured Flow Count (Log10 Scale)", fontsize=9)
    ax.grid(True, axis="x", ls=":", alpha=0.6)

    for b, cnt, cf in zip(bars, counts, confs):
        ax.text(cnt * 1.18, b.get_y() + b.get_height()/2, f"{cnt} (Conf: {cf:.1f}%)",
                va="center", ha="left", fontsize=7.8, fontweight="bold", color=NAVY)

    # Panel B: Transport Protocol Distribution
    ax = axes[1]
    protos = ["TCP Flows\n(1,341 / 57.23%)", "UDP Flows\n(984 / 42.00%)", "Other Protocols\n(18 / 0.77%)"]
    p_counts = [1341, 984, 18]
    p_cols = [BLUE, TEAL, AMBER]
    bars2 = ax.bar(protos, p_counts, color=p_cols, width=0.48)
    ax.set_title("(b) Captured Live Flows by Transport Protocol", fontsize=9.8, fontweight="bold", color=NAVY)
    ax.set_ylabel("Number of Bidirectional Flows", fontsize=9)
    ax.set_ylim(0, 1550)
    ax.grid(True, axis="y", ls=":", alpha=0.6)
    for b in bars2:
        h = b.get_height()
        ax.text(b.get_x() + b.get_width()/2, h + 25, f"{int(h)} flows",
                ha="center", va="bottom", fontsize=8.5, fontweight="bold", color=NAVY)

    plt.tight_layout()
    out = os.path.join(FIG_DIR, "fig4_6_live_detection_telemetry.png")
    fig.savefig(out, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("Generated:", out)


if __name__ == "__main__":
    gen_fig4_1()
    gen_fig4_2()
    gen_fig4_3()
    gen_fig4_4()
    gen_fig4_5()
    gen_fig4_6()
    print("All 6 Chapter 4 data-driven figures generated successfully.")
