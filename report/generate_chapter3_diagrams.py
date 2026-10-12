import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Polygon

FIG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures")
os.makedirs(FIG_DIR, exist_ok=True)

# Academic Color Palette
NAVY = "#0F172A"
BLUE = "#1D4ED8"
BLUE_LIGHT = "#EFF6FF"
TEAL = "#0F766E"
TEAL_LIGHT = "#F0FDFA"
INDIGO = "#4338CA"
INDIGO_LIGHT = "#EEF2FF"
AMBER = "#B45309"
AMBER_LIGHT = "#FFFBEB"
CRIMSON = "#B91C1C"
CRIMSON_LIGHT = "#FEF2F2"
GREEN = "#15803D"
GREEN_LIGHT = "#F0FDF4"
SLATE = "#334155"
SLATE_LIGHT = "#F8FAFC"
BORDER = "#94A3B8"


def draw_box(ax, x, y, w, h, title, subtitle="", bg=BLUE_LIGHT, border=BLUE, title_color=NAVY, fontsize=8.2, sub_fontsize=7.3):
    box = FancyBboxPatch(
        (x - w / 2, y - h / 2), w, h,
        boxstyle="round,pad=0.02,rounding_size=0.12",
        facecolor=bg, edgecolor=border, linewidth=1.6, zorder=3
    )
    ax.add_patch(box)
    if subtitle:
        ax.text(x, y + h * 0.17, title, ha="center", va="center", fontsize=fontsize,
                fontweight="bold", color=title_color, family="sans-serif", zorder=4)
        ax.text(x, y - h * 0.17, subtitle, ha="center", va="center", fontsize=sub_fontsize,
                color=SLATE, family="sans-serif", zorder=4)
    else:
        ax.text(x, y, title, ha="center", va="center", fontsize=fontsize,
                fontweight="bold", color=title_color, family="sans-serif", zorder=4)


def draw_diamond(ax, x, y, w, h, text, bg=AMBER_LIGHT, border=AMBER, text_color=NAVY, fontsize=7.8):
    pts = [
        (x, y + h / 2),
        (x + w / 2, y),
        (x, y - h / 2),
        (x - w / 2, y)
    ]
    poly = Polygon(pts, closed=True, facecolor=bg, edgecolor=border, linewidth=1.6, zorder=3)
    ax.add_patch(poly)
    ax.text(x, y, text, ha="center", va="center", fontsize=fontsize,
            fontweight="bold", color=text_color, family="sans-serif", zorder=4)


def draw_arrow(ax, x1, y1, x2, y2, label="", color=SLATE, rad=0.0, label_offset=(0, 0)):
    conn = f"arc3,rad={rad}"
    ax.annotate(
        "", xy=(x2, y2), xytext=(x1, y1),
        arrowprops=dict(arrowstyle="-|>,head_length=0.55,head_width=0.32", color=color, lw=1.5, connectionstyle=conn),
        zorder=2
    )
    if label:
        mx = (x1 + x2) / 2 + label_offset[0]
        my = (y1 + y2) / 2 + label_offset[1]
        ax.text(mx, my, label, ha="center", va="center", fontsize=7.5, fontweight="bold",
                color=color, bbox=dict(boxstyle="round,pad=0.15", facecolor="white", edgecolor="none", alpha=0.88), zorder=5)


def setup_canvas(width=11, height=7.5, xlim=(0, 10), ylim=(0, 10), title=""):
    fig, ax = plt.subplots(figsize=(width, height), dpi=300)
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.axis("off")
    if title:
        ax.text((xlim[0] + xlim[1]) / 2, ylim[1] - 0.32, title,
                ha="center", va="center", fontsize=11.5, fontweight="bold", color=NAVY, family="sans-serif")
    return fig, ax


def save_fig(fig, filename):
    out_path = os.path.join(FIG_DIR, filename)
    fig.savefig(out_path, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"Generated: {out_path}")


# ==============================================================================
# FIGURE 3.1: MASTER SYSTEM ARCHITECTURE BLOCK DIAGRAM
# ==============================================================================
def gen_fig3_1():
    fig, ax = setup_canvas(12, 8.2, (0, 12), (0, 10.5),
                           "Figure 3.1: Master Five-Tier System Architecture Block Diagram (Zero Trust NIDS)")
    # Tier 1
    draw_box(ax, 6.0, 9.2, 10.8, 1.0,
             "TIER 1: CLIENT PRESENTATION & SOC VISUALIZATION TIER (Web UI + Chart.js / REST Client)",
             "Zero Trust Login & Role Portal  |  Dataset & Model Training Console  |  Live Threat Telemetry & Alert Dashboard",
             bg=INDIGO_LIGHT, border=INDIGO, fontsize=8.6, sub_fontsize=7.6)
    # Tier 2
    draw_box(ax, 6.0, 7.6, 10.8, 1.0,
             "TIER 2: ZERO TRUST SECURITY & RBAC MIDDLEWARE TIER (security/ & @app.before_request)",
             "Salted 12-Round Bcrypt Vault (password.py)  |  Stateless HS256 JWT Verification (jwt_auth.py)  |  @require_role(['Admin','Analyst']) Gate",
             bg=CRIMSON_LIGHT, border=CRIMSON, fontsize=8.6, sub_fontsize=7.6)
    # Tier 3
    draw_box(ax, 6.0, 6.0, 10.8, 1.0,
             "TIER 3: APPLICATION CONTROLLER & REST API TIER (app.py & Flask Blueprints in api/)",
             "auth_bp (/api/auth/*)   |   dataset_bp (/api/dataset/*)   |   model_bp (/api/model/*)   |   live_detection_bp (/api/live-detection/*)",
             bg=BLUE_LIGHT, border=BLUE, fontsize=8.6, sub_fontsize=7.6)

    # Tier 4 Left (Offline Plane) & Right (Online Plane)
    draw_box(ax, 3.2, 3.8, 5.2, 2.0,
             "TIER 4A: OFFLINE PREPROCESSING & ML TRAINING",
             "• DatasetLoader & StratifiedNIDSSampler (seed=42)\n• Anti-Leakage Clean, Dedup, Mode/Median Impute\n• 70/15/15 Split & Train-Only StandardScaler\n• Async Mini-Batch Neural Trainer (64x32 ReLU / LSTM)\n• Holdout ModelEvaluator (Acc, F1, Confusion, ROC-AUC)",
             bg=TEAL_LIGHT, border=TEAL, fontsize=8.3, sub_fontsize=7.3)

    draw_box(ax, 8.8, 3.8, 5.2, 2.0,
             "TIER 4B: PASSIVE LIVE CAPTURE & FLOW INFERENCE",
             "• PacketCaptureManager (Scapy / Windows Npcap)\n• FlowManager (Canonical 5-Tuple Bidirectional LRU)\n• FlowFeatureExtractor (CIC-22 / UNSW-15 / NSL-19)\n• LivePredictor (StandardScaler + Softmax Posterior)\n• Zero Trust Risk Scorer (LOW / MEDIUM / HIGH)",
             bg=AMBER_LIGHT, border=AMBER, fontsize=8.3, sub_fontsize=7.3)

    # Tier 5 Left (Database) & Right (Artifacts)
    draw_box(ax, 3.2, 1.3, 5.2, 1.4,
             "TIER 5A: RELATIONAL DATABASE (SQLite + SQLAlchemy)",
             "database/database.db: roles, users, audit_logs,\ndataset_history, model_history, live_detections",
             bg=GREEN_LIGHT, border=GREEN, fontsize=8.1, sub_fontsize=7.3)

    draw_box(ax, 8.8, 1.3, 5.2, 1.4,
             "TIER 5B: VERSIONED ARTIFACT & DATASET REPOSITORY",
             "datasets/raw/ & sampled/ (CIC-IDS2017, UNSW, NSL-KDD)\nmodels/<type>/<run_id>/: model.joblib, scaler.pkl, encoder.pkl",
             bg=SLATE_LIGHT, border=SLATE, fontsize=8.1, sub_fontsize=7.3)

    draw_arrow(ax, 6.0, 8.7, 6.0, 8.1, "HTTPS / REST + Bearer JWT")
    draw_arrow(ax, 6.0, 7.1, 6.0, 6.5, "Verified Context g.user")
    draw_arrow(ax, 4.2, 5.5, 3.2, 4.8, "Async Training Dispatch")
    draw_arrow(ax, 7.8, 5.5, 8.8, 4.8, "Sniffer & Telemetry Control")
    draw_arrow(ax, 3.2, 2.8, 3.2, 2.0, "ORM Commits")
    draw_arrow(ax, 3.8, 2.8, 8.0, 2.0, "Serialize .joblib / .pkl", label_offset=(0.3, 0.1))
    draw_arrow(ax, 8.8, 2.0, 8.8, 2.8, "Load Active Model & Scaler", label_offset=(1.1, 0))
    draw_arrow(ax, 8.0, 2.8, 3.8, 2.0, "Persist LiveDetection", label_offset=(-0.3, -0.25))

    save_fig(fig, "fig3_1_master_architecture.png")


# ==============================================================================
# FIGURE 3.2: ZERO TRUST SECURITY & RBAC MIDDLEWARE BLOCK DIAGRAM
# ==============================================================================
def gen_fig3_2():
    fig, ax = setup_canvas(11.5, 6.8, (0, 12), (0, 8.5),
                           "Figure 3.2: Zero Trust Authentication, JWT Verification, and RBAC Enforcement Block Diagram")
    draw_box(ax, 2.0, 6.8, 3.1, 1.1, "SOC Operator Client", "React SPA / Browser\n(Credentials or Bearer JWT)", bg=INDIGO_LIGHT, border=INDIGO)
    draw_box(ax, 6.0, 6.8, 3.3, 1.1, "Auth Controller (/api/auth/*)", "Login, Register, Password Change\n(api/auth_routes.py)", bg=BLUE_LIGHT, border=BLUE)
    draw_box(ax, 10.0, 6.8, 3.1, 1.1, "Bcrypt Password Vault", "12-Round Salted Eksblowfish\n(security/password.py)", bg=TEAL_LIGHT, border=TEAL)

    draw_box(ax, 6.0, 4.7, 3.5, 1.1, "HS256 JWT Token Engine", "Signs & Verifies {user_id, role, exp=8h}\n(security/jwt_auth.py)", bg=AMBER_LIGHT, border=AMBER)
    draw_box(ax, 2.0, 4.7, 3.1, 1.1, "Global Request Interceptor", "@app.before_request Hook\nExtracts Token -> g.user", bg=BLUE_LIGHT, border=BLUE)
    draw_box(ax, 6.0, 2.6, 3.7, 1.2, "Zero Trust RBAC Policy Gate", "@jwt_required & @require_role\nVerifies g.user['role'] in Allowed Roles", bg=CRIMSON_LIGHT, border=CRIMSON)

    draw_box(ax, 2.0, 1.1, 3.3, 1.1, "Protected API Controllers", "Dataset Upload/Delete, Model Train,\nLive Capture (Admin / Analyst)", bg=GREEN_LIGHT, border=GREEN)
    draw_box(ax, 10.0, 2.6, 3.3, 1.2, "Immutable Audit Logger", "log_audit_event() -> SQLite\naudit_logs & logs/app.log", bg=SLATE_LIGHT, border=SLATE)

    draw_arrow(ax, 3.55, 6.8, 4.35, 6.8, "POST /login")
    draw_arrow(ax, 7.65, 6.8, 8.45, 6.8, "check_password()")
    draw_arrow(ax, 6.0, 6.25, 6.0, 5.25, "generate_token()")
    draw_arrow(ax, 4.25, 4.7, 3.55, 4.7, "decode_token()")
    draw_arrow(ax, 2.0, 6.25, 2.0, 5.25, "API Request")
    draw_arrow(ax, 3.55, 4.4, 4.5, 3.2, "g.user Context")
    draw_arrow(ax, 4.15, 2.6, 2.6, 1.65, "Authorized (200)")
    draw_arrow(ax, 7.85, 2.6, 8.35, 2.6, "Log Event")
    draw_arrow(ax, 7.65, 6.4, 9.5, 3.2, "Login Audit", label_offset=(0.5, 0.2))

    save_fig(fig, "fig3_2_zero_trust_architecture.png")


# ==============================================================================
# FIGURE 3.3: PREPROCESSING & TRAINING ARCHITECTURE BLOCK DIAGRAM
# ==============================================================================
def gen_fig3_3():
    fig, ax = setup_canvas(12, 7.2, (0, 12), (0, 9),
                           "Figure 3.3: Leakage-Free Stratified Preprocessing and Asynchronous Neural Training Block Diagram")
    draw_box(ax, 2.2, 7.4, 3.4, 1.1, "1. Raw Benchmark CSVs", "CIC-IDS2017 (2.83M), UNSW (2.54M),\nNSL-KDD (148.5K) in datasets/raw/", bg=SLATE_LIGHT, border=SLATE)
    draw_box(ax, 6.2, 7.4, 3.4, 1.1, "2. StratifiedNIDSSampler", "Preserves Class Ratios (seed=42)\nZero Synthetic Rows (25K-50K)", bg=BLUE_LIGHT, border=BLUE)
    draw_box(ax, 10.0, 7.4, 3.2, 1.1, "3. Pre-Split Sanitizer", "Coerce ±Inf -> NaN & Drop\nDuplicates BEFORE Splitting", bg=TEAL_LIGHT, border=TEAL)

    draw_box(ax, 10.0, 5.2, 3.2, 1.1, "4. Statistical Imputer", "Numeric -> Order-Stat Median\nCategorical -> Mode + LabelEncoder", bg=TEAL_LIGHT, border=TEAL)
    draw_box(ax, 6.2, 5.2, 3.4, 1.1, "5. Leakage Column Filter", "Drops Flow ID, Source/Dest IP,\nTimestamp, difficulty_level", bg=AMBER_LIGHT, border=AMBER)
    draw_box(ax, 2.2, 5.2, 3.4, 1.1, "6. Stratified 70/15/15 Split", "70% Train | 15% Val | 15% Test\nFit StandardScaler ONLY on Train", bg=INDIGO_LIGHT, border=INDIGO)

    draw_box(ax, 2.2, 2.8, 3.4, 1.3, "7. Async Neural Trainer", "MLPClassifier(64, 32, ReLU) / LSTM\nMini-Batch Adam partial_fit()\nTracks Frobenius Norm ΔW^(e)", bg=CRIMSON_LIGHT, border=CRIMSON)
    draw_box(ax, 6.2, 2.8, 3.4, 1.3, "8. Holdout ModelEvaluator", "Evaluates Unseen 15% Test Split\nAccuracy, Weighted P/R/F1,\nConfusion Matrix & ROC-AUC", bg=GREEN_LIGHT, border=GREEN)
    draw_box(ax, 10.0, 2.8, 3.2, 1.3, "9. Versioned Artifact Store", "models/<type>/<run_id>/: model.joblib,\nscaler.pkl, encoder.pkl, report.json\n+ SQLite ModelHistory Commit", bg=BLUE_LIGHT, border=BLUE)

    draw_arrow(ax, 3.9, 7.4, 4.5, 7.4)
    draw_arrow(ax, 7.9, 7.4, 8.4, 7.4)
    draw_arrow(ax, 10.0, 6.85, 10.0, 5.75)
    draw_arrow(ax, 8.4, 5.2, 7.9, 5.2)
    draw_arrow(ax, 4.5, 5.2, 3.9, 5.2)
    draw_arrow(ax, 2.2, 4.65, 2.2, 3.45, "X_train, X_val")
    draw_arrow(ax, 3.9, 2.8, 4.5, 2.8, "Converged Model")
    draw_arrow(ax, 2.8, 4.65, 5.5, 3.45, "Unseen X_test", label_offset=(0.4, 0.1))
    draw_arrow(ax, 7.9, 2.8, 8.4, 2.8, "Metrics & Checkpoints")

    save_fig(fig, "fig3_3_preprocessing_training_architecture.png")


# ==============================================================================
# FIGURE 3.4: LIVE PACKET CAPTURE & FLOW INFERENCE BLOCK DIAGRAM
# ==============================================================================
def gen_fig3_4():
    fig, ax = setup_canvas(12, 7.0, (0, 12), (0, 8.8),
                           "Figure 3.4: Passive Live Network Traffic Capture and Real-Time Zero Trust Inference Block Diagram")
    draw_box(ax, 2.2, 7.1, 3.4, 1.2, "1. Host Network Interface", "Wi-Fi / Ethernet / Loopback\nWindows Npcap Driver (wpcap.dll)\nor Controlled Replay Stream", bg=SLATE_LIGHT, border=SLATE)
    draw_box(ax, 6.2, 7.1, 3.4, 1.2, "2. PacketCaptureManager", "_sniff_worker (Scapy store=False)\n_reaper_worker (1.0s Idle Scan)\nParses IP/TCP/UDP Headers", bg=BLUE_LIGHT, border=BLUE)
    draw_box(ax, 10.0, 7.1, 3.2, 1.2, "3. Bidirectional FlowManager", "Canonical 5-Tuple Key (LRU=5000)\nTracks Fwd/Bwd Pkts, Bytes, IAT,\nTCP Flags, Seq Loss & State", bg=TEAL_LIGHT, border=TEAL)

    draw_box(ax, 10.0, 4.6, 3.2, 1.2, "4. Flow Boundary Emitter", "Triggers on:\n• TCP FIN or RST Flag\n• Batch >= 5 Packets\n• Idle Timeout >= 2.0s", bg=AMBER_LIGHT, border=AMBER)
    draw_box(ax, 6.2, 4.6, 3.4, 1.2, "5. FlowFeatureExtractor", "Dynamic Schema Alignment:\n• CIC-IDS2017 (22 Features)\n• UNSW-NB15 (15 Features)\n• NSL-KDD (19 Window Features)", bg=INDIGO_LIGHT, border=INDIGO)
    draw_box(ax, 2.2, 4.6, 3.4, 1.2, "6. LivePredictor Engine", "Applies scaler.pkl (Z-Score)\nRuns Neural predict_proba()\nDecodes Label via encoder.pkl", bg=CRIMSON_LIGHT, border=CRIMSON)

    draw_box(ax, 3.8, 2.1, 4.2, 1.2, "7. Zero Trust Risk Scorer", "LOW: Benign or Conf < 60%\nMEDIUM: Attack & 60% <= Conf < 85%\nHIGH: Attack & Conf >= 85%", bg=AMBER_LIGHT, border=AMBER)
    draw_box(ax, 8.8, 2.1, 4.2, 1.2, "8. DetectionLogger & SOC UI", "Rolling Deques (300 Flows / 100 Alerts)\nSQLite live_detections Persistence\nOne-Click CSV Export (/export)", bg=GREEN_LIGHT, border=GREEN)

    draw_arrow(ax, 3.9, 7.1, 4.5, 7.1, "Raw Frames")
    draw_arrow(ax, 7.9, 7.1, 8.4, 7.1, "_on_packet()")
    draw_arrow(ax, 10.0, 6.5, 10.0, 5.2, "State Update")
    draw_arrow(ax, 8.4, 4.6, 7.9, 4.6, "NetworkFlow")
    draw_arrow(ax, 4.5, 4.6, 3.9, 4.6, "X_raw (1 x d)")
    draw_arrow(ax, 2.2, 4.0, 3.2, 2.7, "Class + Conf")
    draw_arrow(ax, 5.9, 2.1, 6.7, 2.1, "Risk Badge")

    save_fig(fig, "fig3_4_live_detection_architecture.png")


# ==============================================================================
# FIGURE 3.5: DATABASE ENTITY-RELATIONSHIP (ER) DIAGRAM
# ==============================================================================
def gen_fig3_5():
    fig, ax = setup_canvas(12, 7.5, (0, 12), (0, 9.2),
                           "Figure 3.5: Entity-Relationship (ER) Diagram of the SQLite Relational Persistence Layer")
    draw_box(ax, 2.2, 7.2, 3.4, 1.6, "TABLE: roles",
             "PK  id : INTEGER\nUQ  name : VARCHAR(50)\n    description : VARCHAR(200)",
             bg=INDIGO_LIGHT, border=INDIGO)
    draw_box(ax, 6.2, 7.2, 3.6, 1.8, "TABLE: users",
             "PK  id : INTEGER\nUQ  username : VARCHAR(80)\nUQ  email : VARCHAR(120)\n    password_hash : VARCHAR(255)\nFK  role_id : INTEGER -> roles.id\n    created_at : DATETIME",
             bg=BLUE_LIGHT, border=BLUE)
    draw_box(ax, 10.1, 7.2, 3.3, 1.8, "TABLE: audit_logs",
             "PK  id : INTEGER\nFK  user_id : INTEGER -> users.id\n    username : VARCHAR(80)\n    action : VARCHAR(150)\n    ip_address : VARCHAR(50)\n    status : VARCHAR(50) | timestamp",
             bg=CRIMSON_LIGHT, border=CRIMSON)

    draw_box(ax, 2.3, 3.2, 3.6, 2.4, "TABLE: dataset_history",
             "PK  id : INTEGER\n    filename : VARCHAR(255)\n    dataset_type : VARCHAR(50)\n    total_rows / training_rows : INT\n    col_count : INT | file_size_mb : FLOAT\n    is_selected : BOOLEAN\n    target_col : VARCHAR(100)\n    missing / duplicate / infinite_count\n    class_distribution_json : TEXT",
             bg=TEAL_LIGHT, border=TEAL)
    draw_box(ax, 6.3, 3.2, 3.6, 2.4, "TABLE: model_history",
             "PK  id : INTEGER\n    model_name : VARCHAR(150)\n    dataset_name : VARCHAR(255)\n    accuracy / loss : FLOAT\n    precision / recall / f1_score : FLOAT\n    training_time / prediction_time : FLOAT\n    model_type / framework : VARCHAR\n    params_json : TEXT\n    artifact_path : VARCHAR(500)",
             bg=AMBER_LIGHT, border=AMBER)
    draw_box(ax, 10.1, 3.2, 3.3, 2.4, "TABLE: live_detections",
             "PK  id : INTEGER\nIX  timestamp : DATETIME\n    source_ip / destination_ip : VARCHAR\n    source_port / destination_port : INT\n    protocol : VARCHAR(16)\n    flow_duration : FLOAT\n    packet_count / bytes : INTEGER\nIX  prediction : VARCHAR(64)\n    confidence : FLOAT\nIX  risk_level : VARCHAR(16)",
             bg=GREEN_LIGHT, border=GREEN)

    draw_arrow(ax, 3.9, 7.2, 4.4, 7.2, "1 : N (role_id)")
    draw_arrow(ax, 8.0, 7.2, 8.45, 7.2, "1 : N (user_id)")
    draw_arrow(ax, 4.1, 3.2, 4.5, 3.2, "1 : N (dataset_name)")
    draw_arrow(ax, 8.1, 3.2, 8.45, 3.2, "1 : N (Active Model)")

    save_fig(fig, "fig3_5_database_er_diagram.png")


# ==============================================================================
# FIGURE 3.6: FLOWCHART OF ALGORITHM 3.1 (ZERO TRUST AUTH & RBAC)
# ==============================================================================
def gen_fig3_6():
    fig, ax = setup_canvas(11.5, 8.5, (0, 12), (0, 11),
                           "Figure 3.6: Flowchart of Zero Trust JWT Authentication and RBAC Policy Enforcement")
    draw_box(ax, 5.2, 9.9, 4.8, 0.7, "START: Incoming HTTP API Request R", bg=SLATE_LIGHT, border=SLATE)
    draw_box(ax, 5.2, 8.8, 5.6, 0.75, "Extract Token from Authorization: Bearer Header\nor jwt_token Cookie (get_token_from_request)", bg=BLUE_LIGHT, border=BLUE)
    draw_diamond(ax, 5.2, 7.4, 3.6, 1.1, "Is Token Present\nin Request?")
    draw_diamond(ax, 5.2, 5.7, 3.8, 1.1, "Verify HS256 Signature\n& Expiration (t_now < exp)?")
    draw_box(ax, 5.2, 4.3, 5.6, 0.7, "Bind Decoded Payload {user_id, username, role} to g.user", bg=TEAL_LIGHT, border=TEAL)
    draw_diamond(ax, 5.2, 2.9, 3.8, 1.1, "Is g.user['role'] in\nEndpoint Allowed Roles?")
    draw_box(ax, 5.2, 1.3, 5.6, 0.8, "GRANT ACCESS: Execute Flask Blueprint Controller\n& Log Authorized Action to SQLite audit_logs", bg=GREEN_LIGHT, border=GREEN)

    # Rejection blocks on right
    draw_box(ax, 9.8, 6.5, 3.4, 0.9, "Log UNAUTHORIZED / INVALID\nReturn HTTP 401 Unauthorized", bg=CRIMSON_LIGHT, border=CRIMSON)
    draw_box(ax, 9.8, 2.9, 3.4, 0.9, "Log RBAC_ACCESS_DENIED\nReturn HTTP 403 Forbidden", bg=CRIMSON_LIGHT, border=CRIMSON)

    draw_arrow(ax, 5.2, 9.55, 5.2, 9.18)
    draw_arrow(ax, 5.2, 8.42, 5.2, 7.95)
    draw_arrow(ax, 5.2, 6.85, 5.2, 6.25, "YES")
    draw_arrow(ax, 7.0, 7.4, 9.8, 6.95, "NO")
    draw_arrow(ax, 7.1, 5.7, 9.8, 6.05, "INVALID / EXPIRED")
    draw_arrow(ax, 5.2, 5.15, 5.2, 4.65, "VALID")
    draw_arrow(ax, 5.2, 3.95, 5.2, 3.45)
    draw_arrow(ax, 5.2, 2.35, 5.2, 1.7, "YES")
    draw_arrow(ax, 7.1, 2.9, 8.1, 2.9, "NO")

    save_fig(fig, "fig3_6_zero_trust_flowchart.png")


# ==============================================================================
# FIGURE 3.7: FLOWCHART OF ALGORITHM 3.2 (PREPROCESSING PIPELINE)
# ==============================================================================
def gen_fig3_7():
    fig, ax = setup_canvas(11.5, 8.8, (0, 12), (0, 11.5),
                           "Figure 3.7: Flowchart of Leakage-Free Stratified Sampling and Data Preprocessing Pipeline")
    draw_box(ax, 5.2, 10.5, 6.0, 0.65, "START: Load Raw Benchmark CSV (DatasetLoader.load_dataset)", bg=SLATE_LIGHT, border=SLATE)
    draw_diamond(ax, 5.2, 9.3, 3.8, 1.0, "Is N_target < N_raw?")
    draw_box(ax, 9.6, 9.3, 3.6, 0.75, "Stratified Subsample (seed=42)\nPreserve Class Proportions", bg=BLUE_LIGHT, border=BLUE)
    draw_box(ax, 5.2, 8.0, 6.4, 0.7, "Sanitize Domain: Replace +Inf and -Inf with NaN", bg=TEAL_LIGHT, border=TEAL)
    draw_box(ax, 5.2, 7.0, 6.4, 0.7, "Deduplicate Rows BEFORE Split: df.drop_duplicates()", bg=TEAL_LIGHT, border=TEAL)
    draw_box(ax, 5.2, 6.0, 6.4, 0.75, "Statistical Imputation: Categorical -> Mode | Numeric -> Median", bg=AMBER_LIGHT, border=AMBER)
    draw_box(ax, 5.2, 5.0, 6.4, 0.7, "Drop Leakage Metadata (Flow ID, IPs, Timestamp) & LabelEncode", bg=AMBER_LIGHT, border=AMBER)
    draw_box(ax, 5.2, 4.0, 6.4, 0.7, "Two-Stage Stratified Split: 70% Train | 15% Val | 15% Test", bg=INDIGO_LIGHT, border=INDIGO)
    draw_box(ax, 5.2, 2.9, 6.4, 0.75, "Fit StandardScaler ONLY on X_train (Compute μ_train, σ_train)\nTransform X_val and X_test using Frozen Parameters", bg=CRIMSON_LIGHT, border=CRIMSON)
    draw_box(ax, 5.2, 1.7, 6.4, 0.75, "END: Serialize scaler.pkl & encoder.pkl; Output Standardized Tensors", bg=GREEN_LIGHT, border=GREEN)

    draw_arrow(ax, 5.2, 10.17, 5.2, 9.8)
    draw_arrow(ax, 7.1, 9.3, 7.8, 9.3, "YES")
    draw_arrow(ax, 9.6, 8.92, 6.8, 8.35)
    draw_arrow(ax, 5.2, 8.8, 5.2, 8.35, "NO (Full)")
    draw_arrow(ax, 5.2, 7.65, 5.2, 7.35)
    draw_arrow(ax, 5.2, 6.65, 5.2, 6.38)
    draw_arrow(ax, 5.2, 5.62, 5.2, 5.35)
    draw_arrow(ax, 5.2, 4.65, 5.2, 4.35)
    draw_arrow(ax, 5.2, 3.65, 5.2, 3.28)
    draw_arrow(ax, 5.2, 2.52, 5.2, 2.08)

    save_fig(fig, "fig3_7_preprocessing_flowchart.png")


# ==============================================================================
# FIGURE 3.8: FLOWCHART OF ALGORITHM 3.3 (ASYNC NEURAL TRAINING)
# ==============================================================================
def gen_fig3_8():
    fig, ax = setup_canvas(11.5, 8.6, (0, 12), (0, 11.2),
                           "Figure 3.8: Flowchart of Asynchronous Mini-Batch Neural Training and Convergence Tracking")
    draw_box(ax, 4.8, 10.2, 6.0, 0.65, "START: Spawn Background Thread (NIDSTrainer.train)", bg=SLATE_LIGHT, border=SLATE)
    draw_box(ax, 4.8, 9.2, 6.2, 0.7, "Initialize Neural Network (64, 32 ReLU / LSTM) & Adam (η=0.001)\nSet epoch e = 1, prev_weights = NULL", bg=BLUE_LIGHT, border=BLUE)
    draw_diamond(ax, 4.8, 7.9, 3.4, 0.95, "Is Epoch e <= E?")
    draw_box(ax, 4.8, 6.7, 6.2, 0.7, "Shuffle (X_train, y_train) with Deterministic Seed (S + e)", bg=TEAL_LIGHT, border=TEAL)
    draw_box(ax, 4.8, 5.7, 6.2, 0.7, "Mini-Batch Loop (size B=32): Execute Adam partial_fit(X_b, y_b)", bg=TEAL_LIGHT, border=TEAL)
    draw_box(ax, 4.8, 4.6, 6.4, 0.75, "Compute Train & Val Accuracy, Cross-Entropy Loss (log_loss),\nand Frobenius Weight Convergence Norm ΔW^(e) = Σ||W^(e) - W^(e-1)||_F", bg=AMBER_LIGHT, border=AMBER)
    draw_box(ax, 4.8, 3.5, 6.2, 0.65, "Broadcast Epoch Telemetry to training_status; Set e = e + 1", bg=INDIGO_LIGHT, border=INDIGO)

    draw_box(ax, 9.8, 6.2, 3.6, 1.1, "Evaluate Holdout (X_test, y_test)\nCompute Acc, Precision, Recall,\nF1, Confusion Matrix, ROC-AUC", bg=GREEN_LIGHT, border=GREEN)
    draw_box(ax, 9.8, 4.3, 3.6, 1.1, "END: Save model.joblib,\nevaluation_report.json &\nInsert SQLite ModelHistory", bg=CRIMSON_LIGHT, border=CRIMSON)

    draw_arrow(ax, 4.8, 9.87, 4.8, 9.55)
    draw_arrow(ax, 4.8, 8.85, 4.8, 8.38)
    draw_arrow(ax, 4.8, 7.42, 4.8, 7.05, "YES")
    draw_arrow(ax, 4.8, 6.35, 4.8, 6.05)
    draw_arrow(ax, 4.8, 5.35, 4.8, 4.98)
    draw_arrow(ax, 4.8, 4.22, 4.8, 3.83)
    # Loop back from 3.5 to 7.9 on left side
    ax.plot([1.7, 0.9, 0.9, 3.1], [3.5, 3.5, 7.9, 7.9], color=BLUE, lw=1.5)
    ax.annotate("", xy=(3.1, 7.9), xytext=(2.8, 7.9),
                arrowprops=dict(arrowstyle="-|>,head_length=0.5,head_width=0.3", color=BLUE, lw=1.5))
    ax.text(0.9, 5.7, "Next Epoch", ha="center", va="center", rotation=90, fontsize=7.8, fontweight="bold",
            color=BLUE, bbox=dict(boxstyle="round,pad=0.15", facecolor="white", edgecolor="none"))

    draw_arrow(ax, 6.5, 7.9, 9.8, 6.75, "NO (e > E)")
    draw_arrow(ax, 9.8, 5.65, 9.8, 4.85)

    save_fig(fig, "fig3_8_training_flowchart.png")


# ==============================================================================
# FIGURE 3.9: FLOWCHART OF ALGORITHM 3.4 (5-TUPLE FLOW AGGREGATION)
# ==============================================================================
def gen_fig3_9():
    fig, ax = setup_canvas(11.5, 8.5, (0, 12), (0, 11),
                           "Figure 3.9: Flowchart of Passive Packet Sniffing and Canonical 5-Tuple Flow Aggregation")
    draw_box(ax, 5.2, 10.0, 5.8, 0.65, "START: Capture Packet pkt from Adapter (_on_packet)", bg=SLATE_LIGHT, border=SLATE)
    draw_box(ax, 5.2, 9.0, 6.0, 0.7, "Parse IP/TCP/UDP Headers & Build Canonical 5-Tuple Key:\nmin((src_ip,sport),(dst_ip,dport)) <-> max(...) @ proto", bg=BLUE_LIGHT, border=BLUE)
    draw_diamond(ax, 5.2, 7.7, 3.4, 0.95, "Is Key in\nactive_flows?")
    draw_box(ax, 9.7, 7.7, 3.5, 0.85, "Create New NetworkFlow\n(Evict Oldest LRU if >= 5000)", bg=TEAL_LIGHT, border=TEAL)
    draw_diamond(ax, 5.2, 6.2, 3.6, 1.0, "Packet Matches\nFlow Initiator (Fwd)?")
    draw_box(ax, 2.3, 4.8, 3.8, 0.85, "Update Forward Counters:\nfwd_pkts, fwd_bytes, sttl, sloss", bg=INDIGO_LIGHT, border=INDIGO)
    draw_box(ax, 8.1, 4.8, 3.8, 0.85, "Update Backward Counters:\nbwd_pkts, bwd_bytes, dttl, dloss", bg=INDIGO_LIGHT, border=INDIGO)
    draw_box(ax, 5.2, 3.5, 6.0, 0.7, "Update TCP Flag Counts (FIN,SYN,RST,PSH,ACK,URG) & State", bg=AMBER_LIGHT, border=AMBER)
    draw_diamond(ax, 5.2, 2.2, 4.2, 1.05, "FIN/RST Flag OR\nBatch >= 5 Pkts OR Idle >= 2s?")
    draw_box(ax, 5.2, 0.8, 6.0, 0.7, "EMIT NetworkFlow to FlowFeatureExtractor & LivePredictor", bg=GREEN_LIGHT, border=GREEN)
    draw_box(ax, 9.9, 2.2, 3.1, 0.75, "Retain in active_flows\nAwait Next Packet", bg=SLATE_LIGHT, border=SLATE)

    draw_arrow(ax, 5.2, 9.67, 5.2, 9.35)
    draw_arrow(ax, 5.2, 8.65, 5.2, 8.18)
    draw_arrow(ax, 6.9, 7.7, 7.95, 7.7, "NO")
    draw_arrow(ax, 9.7, 7.27, 6.2, 6.55)
    draw_arrow(ax, 5.2, 7.22, 5.2, 6.7, "YES")
    draw_arrow(ax, 3.4, 6.2, 2.3, 5.23, "YES (Fwd)")
    draw_arrow(ax, 7.0, 6.2, 8.1, 5.23, "NO (Bwd)")
    draw_arrow(ax, 2.3, 4.37, 4.2, 3.85)
    draw_arrow(ax, 8.1, 4.37, 6.2, 3.85)
    draw_arrow(ax, 5.2, 3.15, 5.2, 2.73)
    draw_arrow(ax, 5.2, 1.67, 5.2, 1.15, "YES (Emit)")
    draw_arrow(ax, 7.3, 2.2, 8.35, 2.2, "NO")

    save_fig(fig, "fig3_9_flow_aggregation_flowchart.png")


# ==============================================================================
# FIGURE 3.10: FLOWCHART OF ALGORITHM 3.5 (LIVE INFERENCE & RISK SCORING)
# ==============================================================================
def gen_fig3_10():
    fig, ax = setup_canvas(11.5, 8.5, (0, 12), (0, 11),
                           "Figure 3.10: Flowchart of Dynamic Schema Feature Extraction, Inference, and Zero Trust Risk Scoring")
    draw_box(ax, 5.8, 10.1, 6.2, 0.65, "START: Receive Emitted NetworkFlow F in LivePredictor", bg=SLATE_LIGHT, border=SLATE)
    draw_diamond(ax, 5.8, 8.9, 3.8, 0.95, "Check Active Model\nSchema Dimension d?")

    draw_box(ax, 1.9, 7.4, 3.4, 0.85, "d = 22 (CIC-IDS2017)\nExtract 22 Flow/Flag/IAT\nAttributes", bg=BLUE_LIGHT, border=BLUE)
    draw_box(ax, 5.8, 7.4, 3.4, 0.85, "d = 15 (UNSW-NB15)\nExtract 15 Dur/Rate/TTL/\nBitload/Loss Attributes", bg=TEAL_LIGHT, border=TEAL)
    draw_box(ax, 9.7, 7.4, 3.4, 0.85, "d = 19 (NSL-KDD)\nExtract 19 Flow + 2.0s\nSliding Window Rates", bg=INDIGO_LIGHT, border=INDIGO)

    draw_box(ax, 5.8, 5.9, 7.2, 0.75, "Standardize Vector Z = scaler.transform(X_raw) & Run predict_proba(Z)\nCompute y_hat = argmax(P), Conf = max(P), Decode Label L_hat", bg=AMBER_LIGHT, border=AMBER)
    draw_diamond(ax, 5.8, 4.4, 4.0, 1.05, "Is L_hat an Attack AND\nConf >= 0.60?")

    draw_box(ax, 1.9, 2.9, 3.3, 0.85, "Assign Risk = LOW\nStatus = 'Normal'", bg=GREEN_LIGHT, border=GREEN)
    draw_diamond(ax, 7.9, 2.9, 3.4, 0.95, "Is Confidence\nConf >= 0.85?")
    draw_box(ax, 5.6, 1.4, 3.3, 0.8, "Assign Risk = MEDIUM\nStatus = 'Alert'", bg=AMBER_LIGHT, border=AMBER)
    draw_box(ax, 9.7, 1.4, 3.3, 0.8, "Assign Risk = HIGH\nStatus = 'Alert'", bg=CRIMSON_LIGHT, border=CRIMSON)

    draw_box(ax, 5.8, 0.35, 8.2, 0.6, "END: Push to Rolling Memory Deques & Persist Row to SQLite live_detections", bg=SLATE_LIGHT, border=SLATE)

    draw_arrow(ax, 5.8, 9.77, 5.8, 9.38)
    draw_arrow(ax, 3.9, 8.9, 1.9, 7.83, "d = 22")
    draw_arrow(ax, 5.8, 8.42, 5.8, 7.83, "d = 15")
    draw_arrow(ax, 7.7, 8.9, 9.7, 7.83, "d = 19")

    draw_arrow(ax, 1.9, 6.97, 4.5, 6.28)
    draw_arrow(ax, 5.8, 6.97, 5.8, 6.28)
    draw_arrow(ax, 9.7, 6.97, 7.1, 6.28)

    draw_arrow(ax, 5.8, 5.52, 5.8, 4.93)
    draw_arrow(ax, 3.8, 4.4, 1.9, 3.33, "NO (Benign / <60%)")
    draw_arrow(ax, 7.8, 4.4, 7.9, 3.38, "YES (Attack)")
    draw_arrow(ax, 6.2, 2.9, 5.6, 1.8, "NO (60-85%)")
    draw_arrow(ax, 9.6, 2.9, 9.7, 1.8, "YES (>=85%)")

    draw_arrow(ax, 1.9, 2.47, 3.8, 0.65)
    draw_arrow(ax, 5.6, 1.0, 5.6, 0.65)
    draw_arrow(ax, 9.7, 1.0, 7.7, 0.65)

    save_fig(fig, "fig3_10_live_inference_flowchart.png")


if __name__ == "__main__":
    gen_fig3_1()
    gen_fig3_2()
    gen_fig3_3()
    gen_fig3_4()
    gen_fig3_5()
    gen_fig3_6()
    gen_fig3_7()
    gen_fig3_8()
    gen_fig3_9()
    gen_fig3_10()
    print("All 10 figures generated successfully in report/figures/")
