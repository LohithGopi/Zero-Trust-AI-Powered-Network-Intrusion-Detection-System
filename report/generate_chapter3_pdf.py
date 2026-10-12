import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether, HRFlowable, Image, Preformatted
)
from reportlab.pdfgen import canvas

REPORT_DIR = os.path.dirname(os.path.abspath(__file__))
FIG_DIR = os.path.join(REPORT_DIR, "figures")
OUTPUT_PDF = os.path.join(REPORT_DIR, "Chapter_3_System_Design_and_Implementation.pdf")


class Chapter3NumberedCanvas(canvas.Canvas):
    """Two-pass canvas that renders academic headers, footers, and total page count."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        print(f"Total PDF Pages Generated: {num_pages}")
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_decorations(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_decorations(self, page_count):
        self.saveState()
        width, height = A4

        # Header
        self.setFont("Times-Italic", 9.5)
        self.setFillColor(colors.HexColor("#334155"))
        self.drawString(54, height - 38, "AI-Powered Zero Trust Network Intrusion Detection System (NIDS)")
        self.drawRightString(width - 54, height - 38, "Chapter 3: System Design and Implementation")
        self.setStrokeColor(colors.HexColor("#94A3B8"))
        self.setLineWidth(0.6)
        self.line(54, height - 44, width - 54, height - 44)

        # Footer
        self.line(54, 46, width - 54, 46)
        self.setFont("Times-Roman", 9.5)
        self.drawString(54, 32, "Dept. of Information Science & Engineering, JNNCE Shivamogga (Batch No. 34)")
        self.drawRightString(width - 54, 32, f"Page {self._pageNumber} of {page_count}")
        self.restoreState()


def build_styles():
    base = getSampleStyleSheet()
    NAVY = colors.HexColor("#0F172A")
    BLUE = colors.HexColor("#1D4ED8")
    SLATE = colors.HexColor("#1E293B")

    styles = {
        "ChapterHeader": ParagraphStyle(
            "ChapterHeader", parent=base["Normal"], fontName="Times-Bold",
            fontSize=15, leading=20, alignment=TA_CENTER, textColor=BLUE, spaceAfter=4
        ),
        "ChapterTitle": ParagraphStyle(
            "ChapterTitle", parent=base["Normal"], fontName="Times-Bold",
            fontSize=20, leading=26, alignment=TA_CENTER, textColor=NAVY, spaceAfter=12
        ),
        "H1": ParagraphStyle(
            "H1", parent=base["Normal"], fontName="Times-Bold",
            fontSize=14.5, leading=19, textColor=NAVY, spaceBefore=12, spaceAfter=6, keepWithNext=True
        ),
        "H2": ParagraphStyle(
            "H2", parent=base["Normal"], fontName="Times-Bold",
            fontSize=12, leading=16, textColor=BLUE, spaceBefore=10, spaceAfter=5, keepWithNext=True
        ),
        "H3": ParagraphStyle(
            "H3", parent=base["Normal"], fontName="Times-BoldItalic",
            fontSize=11, leading=15, textColor=NAVY, spaceBefore=7, spaceAfter=3, keepWithNext=True
        ),
        "Body": ParagraphStyle(
            "Body", parent=base["Normal"], fontName="Times-Roman",
            fontSize=11.6, leading=18.3, alignment=TA_JUSTIFY, textColor=SLATE, spaceAfter=7.5
        ),
        "Bullet": ParagraphStyle(
            "Bullet", parent=base["Normal"], fontName="Times-Roman",
            fontSize=11.3, leading=17.5, alignment=TA_JUSTIFY, leftIndent=18, firstLineIndent=-10,
            textColor=SLATE, spaceAfter=5.5
        ),
        "Caption": ParagraphStyle(
            "Caption", parent=base["Normal"], fontName="Times-BoldItalic",
            fontSize=10.0, leading=14.0, alignment=TA_CENTER, textColor=NAVY, spaceBefore=5, spaceAfter=10
        ),
        "TableTitle": ParagraphStyle(
            "TableTitle", parent=base["Normal"], fontName="Times-Bold",
            fontSize=10.5, leading=14.0, alignment=TA_LEFT, textColor=NAVY, spaceBefore=10, spaceAfter=4, keepWithNext=True
        ),
        "TblHeader": ParagraphStyle(
            "TblHeader", parent=base["Normal"], fontName="Times-Bold",
            fontSize=9.2, leading=12.0, textColor=colors.white
        ),
        "TblCell": ParagraphStyle(
            "TblCell", parent=base["Normal"], fontName="Times-Roman",
            fontSize=9.0, leading=12.5, textColor=SLATE
        ),
        "Equation": ParagraphStyle(
            "Equation", parent=base["Normal"], fontName="Times-BoldItalic",
            fontSize=11.0, leading=15.0, alignment=TA_CENTER, textColor=NAVY
        ),
        "EqTag": ParagraphStyle(
            "EqTag", parent=base["Normal"], fontName="Times-Bold",
            fontSize=10.5, leading=15.0, alignment=TA_CENTER, textColor=BLUE
        ),
        "Code": ParagraphStyle(
            "Code", parent=base["Normal"], fontName="Courier",
            fontSize=8.2, leading=11.0, textColor=NAVY
        )
    }
    return styles


def add_equation(story, styles, expr_html, eq_num):
    tbl = Table(
        [[Paragraph(expr_html, styles["Equation"]), Paragraph(f"({eq_num})", styles["EqTag"])]],
        colWidths=[425, 60]
    )
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F8FAFC")),
        ("BOX", (0, 0), (-1, -1), 0.75, colors.HexColor("#CBD5E1")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(Spacer(1, 3))
    story.append(tbl)
    story.append(Spacer(1, 5))


def add_figure(story, styles, filename, caption, max_height=245):
    path = os.path.join(FIG_DIR, filename)
    if not os.path.exists(path):
        return
    img = Image(path)
    avail_w = 485.0
    ratio = img.imageHeight / float(img.imageWidth)
    w = avail_w
    h = w * ratio
    if h > max_height:
        h = max_height
        w = h / ratio
    img.drawWidth = w
    img.drawHeight = h
    img.hAlign = "CENTER"
    story.append(Spacer(1, 6))
    story.append(KeepTogether([img, Paragraph(caption, styles["Caption"])]))
    story.append(Spacer(1, 5))


def add_table(story, styles, title, headers, rows, col_widths):
    story.append(Paragraph(title, styles["TableTitle"]))
    data = [[Paragraph(h, styles["TblHeader"]) for h in headers]]
    for r in rows:
        data.append([Paragraph(str(c), styles["TblCell"]) for c in r])
    t = Table(data, colWidths=col_widths, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0F172A")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
        ("BOX", (0, 0), (-1, -1), 0.8, colors.HexColor("#94A3B8")),
        ("INNERGRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#CBD5E1")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
    ]))
    story.append(t)
    story.append(Spacer(1, 8))


def add_code_block(story, styles, title, code_text):
    hdr = Paragraph(f"<b>{title}</b>", ParagraphStyle(
        "AlgoHdr", fontName="Times-Bold", fontSize=9.6, leading=12, textColor=colors.white
    ))
    pre = Preformatted(code_text.strip(), styles["Code"])
    t = Table([[hdr], [pre]], colWidths=[485])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, 0), colors.HexColor("#1E3A8A")),
        ("BACKGROUND", (0, 1), (0, 1), colors.HexColor("#F8FAFC")),
        ("BOX", (0, 0), (-1, -1), 0.9, colors.HexColor("#1E3A8A")),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
    ]))
    story.append(Spacer(1, 4))
    story.append(t)
    story.append(Spacer(1, 6))


def generate_pdf():
    doc = SimpleDocTemplate(
        OUTPUT_PDF, pagesize=A4,
        leftMargin=54, rightMargin=54, topMargin=56, bottomMargin=56
    )
    styles = build_styles()
    story = []

    # ==========================================================================
    # CHAPTER BANNER & OVERVIEW
    # ==========================================================================
    story.append(Paragraph("CHAPTER 3", styles["ChapterHeader"]))
    story.append(Paragraph("SYSTEM DESIGN AND IMPLEMENTATION", styles["ChapterTitle"]))
    story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor("#1D4ED8"), spaceBefore=0, spaceAfter=10))

    story.append(Paragraph(
        "This chapter presents the engineering design, multi-tier software architecture, mathematical model, formal algorithms, flowcharts, and implementation details of the proposed <b>AI-Powered Zero Trust Network Intrusion Detection System (Zero Trust NIDS)</b>. All sections are arranged separately for clarity: <b>Section 3.1</b> provides a detailed description of the proposed work; <b>Section 3.2</b> explains the system architecture and block diagrams; <b>Section 3.3</b> formulates the mathematical model of the system; <b>Section 3.4</b> presents the algorithms and flowcharts; and <b>Section 3.5</b> summarizes the module implementation and experimental convergence verification.",
        styles["Body"]
    ))

    # ==========================================================================
    # SECTION 3.1: DETAILED DESCRIPTION OF THE PROPOSED WORK
    # ==========================================================================
    story.append(Paragraph("3.1 Detailed Description of the Proposed Work", styles["H1"]))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#CBD5E1"), spaceBefore=0, spaceAfter=6))

    story.append(Paragraph("3.1.1 Problem Context and Proposed Zero Trust NIDS Paradigm", styles["H2"]))
    story.append(Paragraph(
        "Conventional enterprise networks rely on perimeter-based security models where internal local area network (LAN) traffic is implicitly trusted, alongside signature-based Network Intrusion Detection Systems (NIDS) that match static byte rules. Such systems suffer from three major limitations: (1) inability to detect polymorphic or zero-day attacks that alter packet timing and payload patterns; (2) vulnerability to insider threats and lateral movement once the perimeter is breached; and (3) lack of cryptographic authentication and role-based access control over the NIDS management plane itself.",
        styles["Body"]
    ))
    story.append(Paragraph(
        "To resolve these limitations, the proposed work develops an integrated <b>AI-Powered Zero Trust Network Intrusion Detection System</b>. The system combines two core security principles:",
        styles["Body"]
    ))
    story.append(Paragraph("• <b>Zero Trust Security Enforcement ('Never Trust, Always Verify'):</b> Aligned with NIST SP 800-207 guidelines, no user, API request, or network flow is trusted by default. Every administrative and analytical endpoint is protected by <b>12-round salted Bcrypt password hashing</b>, stateless <b>HMAC-SHA256 JSON Web Tokens (JWT)</b>, strict <b>Role-Based Access Control (Admin vs. Analyst)</b>, and immutable <b>SQLite audit logging</b>.", styles["Bullet"]))
    story.append(Paragraph("• <b>Deep Neural Network Traffic Classification & Live Flow Inference:</b> Instead of static signatures, the system learns non-linear statistical patterns across multi-dimensional network flow features. It supports three benchmark intrusion datasets—<b>CIC-IDS2017</b>, <b>UNSW-NB15</b>, and <b>NSL-KDD</b>—via a leakage-free preprocessing pipeline, trains a Multi-Layer Perceptron (MLP) neural classifier with epoch-by-epoch convergence tracking, and deploys the trained model into a <b>Passive Live Network Detection Engine</b> that captures live packets, aggregates bidirectional 5-tuple flows, and assigns real-time risk scores (<code>LOW</code>, <code>MEDIUM</code>, <code>HIGH</code>).", styles["Bullet"]))

    story.append(Paragraph("3.1.2 Core Functional Modules of the Proposed System", styles["H2"]))
    pillars = [
        ("1. Zero Trust Identity, Authentication & RBAC Module (security/)",
         "Intercepts every incoming HTTP request via a global Flask security filter (@app.before_request). Passwords are hashed using 12-round salted Bcrypt (security/password.py). Upon login, the server issues an 8-hour HS256 JWT token (security/jwt_auth.py) carrying user_id, username, and role. State-modifying endpoints (dataset upload/delete, model training) are restricted to the Admin role via @require_role(['Admin']) (security/zero_trust.py), while monitoring and live detection views are accessible to both Admin and Analyst roles. All events are recorded in the SQLite audit_logs table."),
        ("2. Multi-Dataset Ingestion & Leakage-Free Preprocessing Module (preprocessing/)",
         "Processes benchmark datasets containing millions of rows (CIC-IDS2017, UNSW-NB15, NSL-KDD). StratifiedNIDSSampler (preprocessing/sampler.py) performs deterministic stratified sampling (seed = 42) to preserve exact class proportions without generating synthetic rows. BaseNIDSPreprocessor (preprocessing/preprocess.py) enforces a strict anti-leakage protocol: infinite values (+/-Inf) are replaced with NaN, exact duplicate rows are removed prior to splitting, missing values are imputed via column median (numerical) or mode (categorical), session metadata columns (Flow ID, IPs, Timestamps) are removed, data is partitioned into 70% Train / 15% Validation / 15% Test splits, and StandardScaler is fitted exclusively on the 70% training split."),
        ("3. Asynchronous Neural Network Training & Evaluation Module (training/)",
         "Executes model training in a background daemon thread (training/train_model.py) so the web interface remains responsive. NIDSTrainer trains a (64, 32) ReLU Multi-Layer Perceptron optimized via mini-batch Adam (learning_rate = 0.001, batch_size = 32), recording training/validation cross-entropy loss, accuracy, and the Frobenius weight norm Delta W at every epoch. ModelEvaluator (training/evaluate_model.py) evaluates the unseen 15% test split to compute Accuracy, Precision, Recall, F1-Score, Confusion Matrix, and ROC-AUC, saving artifacts to models/<dataset_type>/<run_id>/."),
        ("4. Passive Live Packet Capture & Bidirectional Flow Detection Module (live_detection/)",
         "Passively monitors host network interfaces via Scapy and Windows Npcap (packet_capture.py) without injecting traffic. FlowManager (flow_manager.py) aggregates raw IPv4/IPv6 TCP and UDP packets into canonical 5-tuple bidirectional flows bounded by an LRU cache of 5,000 flows. Flows are emitted on TCP FIN/RST teardown, every 5 packets, or after a 2.0-second idle timeout. FlowFeatureExtractor (feature_extractor.py) extracts 22-, 15-, or 19-dimensional feature vectors aligned with the active model schema, and LivePredictor (live_predictor.py) standardizes the vector, computes Softmax probabilities, assigns Zero Trust risk scores (LOW, MEDIUM, HIGH), and logs detections to SQLite.")
    ]
    for p_title, p_body in pillars:
        story.append(Paragraph(p_title, styles["H3"]))
        story.append(Paragraph(p_body, styles["Body"]))

    story.append(Paragraph("3.1.3 End-to-End Operational Workflow", styles["H2"]))
    story.append(Paragraph("The proposed system operates across two synchronized execution workflows:", styles["Body"]))
    story.append(Paragraph("<b>A. Offline Model Training Workflow:</b> (1) Operator authenticates via JWT; (2) Benchmark CSV dataset is registered and inspected for missing/infinite values; (3) <code>StratifiedNIDSSampler</code> extracts a balanced class-preserving subset; (4) <code>DataPreprocessor</code> cleans infinities, removes duplicates before splitting, imputes nulls, drops identifier columns, splits into 70/15/15 partitions, and fits <code>StandardScaler</code> on the training split; (5) <code>NIDSTrainer</code> executes mini-batch Adam optimization across epochs while streaming live loss and accuracy metrics; (6) <code>ModelEvaluator</code> computes holdout test metrics and serializes <code>model.joblib</code>, <code>scaler.pkl</code>, and <code>encoder.pkl</code>.", styles["Bullet"]))
    story.append(Paragraph("<b>B. Online Live Intrusion Detection Workflow:</b> (1) Analyst selects a network adapter and trained model; (2) <code>PacketCaptureManager</code> passively sniffs packets via Scapy/Npcap; (3) <code>FlowManager</code> aggregates packets into bidirectional 5-tuple flows and emits completed/active flows; (4) <code>FlowFeatureExtractor</code> computes the 22-, 15-, or 19-feature vector; (5) <code>LivePredictor</code> scales the vector, predicts the traffic class and confidence, and assigns a <code>LOW</code>, <code>MEDIUM</code>, or <code>HIGH</code> risk badge; (6) <code>DetectionLogger</code> updates the SOC dashboard and persists records to SQLite.", styles["Bullet"]))

    story.append(Paragraph("3.1.4 Technology Stack and Multi-Dataset Schema Compatibility", styles["H2"]))
    add_table(
        story, styles,
        "Table 3.1: Hardware and Software Technology Stack Specifications",
        ["Layer", "Technology / Package", "Specification", "Implementation Purpose"],
        [
            ["Operating System", "Microsoft Windows", "Windows 10 / 11 (64-bit)", "Host runtime environment and Npcap packet capture driver support"],
            ["Backend Framework", "Python & Flask", "Python 3.11+, Flask 3.0", "Application Factory (app.py), REST Blueprints, Zero Trust middleware"],
            ["Database & ORM", "SQLite 3 & SQLAlchemy", "Flask-SQLAlchemy 3.1", "Persistent storage (database.db) for users, roles, logs, models, alerts"],
            ["Machine Learning", "Scikit-Learn & Joblib", "Scikit-Learn 1.4+", "MLPClassifier(64, 32), StandardScaler, LabelEncoder, evaluation metrics"],
            ["Data Engineering", "Pandas & NumPy", "Pandas 2.2, NumPy 1.26", "Stratified sampling, pre-split deduplication, median/mode imputation"],
            ["Live Packet Sniffing", "Scapy & Npcap", "Scapy 2.7+, wpcap.dll", "Passive layer-3/layer-4 packet capture and interface enumeration"],
            ["Security & Auth", "PyJWT & Bcrypt", "HS256 JWT, 12-Round Bcrypt", "Stateless token authentication, password hashing, RBAC decorators"],
            ["Frontend Interface", "Web SOC Dashboard", "React 18 / HTML5 / JS", "Interactive dataset catalog, live training charts, and alert console"]
        ],
        [90, 105, 100, 190]
    )

    add_table(
        story, styles,
        "Table 3.2: Multi-Dataset Schema Specifications Supported by the System",
        ["Dataset Schema", "Dimensions", "Supported Attack Categories", "Extracted Flow Features"],
        [
            ["CIC-IDS2017", "22 Features", "BENIGN, DDoS, DoS GoldenEye, DoS Hulk, FTP-Patator, PortScan, Web Attack", "Destination Port, Flow Duration, Total Fwd/Bwd Packets, Total Length Fwd/Bwd Packets, Fwd/Bwd Packet Length Max/Min/Mean, Flow Bytes/s, Flow Packets/s, Flow IAT Mean/Std, FIN/SYN/RST/PSH/ACK/URG Flag Counts"],
            ["UNSW-NB15", "15 Live / 40 Raw", "Normal, Generic, Exploits, Fuzzers, DoS, Reconnaissance, Analysis, Backdoor, Shellcode, Worms", "dur, proto, service, state, spkts, dpkts, sbytes, dbytes, rate, sttl, dttl, sload, dload, sloss, dloss"],
            ["NSL-KDD", "19 Live / 41 Raw", "normal, DoS (neptune), Probe (satan, ipsweep, portsweep), R2L, U2R", "duration, protocol_type, service, flag, src_bytes, dst_bytes, land, wrong_fragment, urgent, hot, num_failed_logins, logged_in, count, srv_count, serror_rate, same_srv_rate, diff_srv_rate, dst_host_count, dst_host_srv_count"]
        ],
        [75, 68, 122, 220]
    )

    story.append(PageBreak())

    # ==========================================================================
    # SECTION 3.2: SYSTEM ARCHITECTURE AND BLOCK DIAGRAMS
    # ==========================================================================
    story.append(Paragraph("3.2 System Architecture and Block Diagrams", styles["H1"]))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#CBD5E1"), spaceBefore=0, spaceAfter=6))

    story.append(Paragraph("3.2.1 Five-Tier System Architecture Overview", styles["H2"]))
    story.append(Paragraph(
        "The proposed system is designed around a modular <b>Five-Tier Layered Architecture</b> that separates user visualization, Zero Trust security enforcement, REST API routing, core machine learning and packet processing engines, and persistent storage. Table 3.3 summarizes the five architectural tiers, and Figure 3.1 presents the Master System Architecture Block Diagram.",
        styles["Body"]
    ))
    add_table(
        story, styles,
        "Table 3.3: Five-Tier Architectural Decomposition of the Zero Trust NIDS",
        ["Architectural Tier", "Source Modules", "Core Responsibilities"],
        [
            ["Tier 1: Presentation & SOC Visualization Tier", "templates/*.html, static/js/*, frontend/src/pages/dashboard/*", "Provides the authenticated SOC dashboard for dataset management, model training visualization, live traffic monitoring, and security audit review."],
            ["Tier 2: Zero Trust Security & RBAC Middleware", "security/password.py, security/jwt_auth.py, security/zero_trust.py", "Enforces 'Never Trust, Always Verify' on every request via 12-round Bcrypt hashing, HS256 JWT validation, and @require_role(['Admin','Analyst']) checks."],
            ["Tier 3: Application Controller & REST API Tier", "app.py, api/auth_routes.py, dataset_routes.py, model_routes.py, live_detection_routes.py", "Implements the Flask Application Factory and four modular Blueprints (/api/auth, /api/dataset, /api/model, /api/live-detection)."],
            ["Tier 4: ML Pipeline & Live Detection Engine", "preprocessing/*, training/*, live_detection/*", "Executes stratified sampling, leakage-free preprocessing, asynchronous neural network training, Scapy packet sniffing, 5-tuple flow aggregation, and risk scoring."],
            ["Tier 5: Persistence & Artifact Storage Tier", "database/init_db.py, database.db, models/*, datasets/*", "Manages 6 SQLite tables via SQLAlchemy ORM and stores versioned model checkpoints (model.joblib, scaler.pkl, encoder.pkl, evaluation_report.json)."]
        ],
        [115, 135, 235]
    )

    add_figure(story, styles, "fig3_1_master_architecture.png",
               "Figure 3.1: Master Five-Tier System Architecture Block Diagram of the AI-Powered Zero Trust NIDS.", max_height=240)

    story.append(Paragraph("<b>Explanation of Master Architecture Blocks (Figure 3.1):</b>", styles["Body"]))
    story.append(Paragraph("• <b>Tier 1 (SOC Visualization Client):</b> Dispatches REST API requests with <code>Authorization: Bearer &lt;JWT&gt;</code> headers and renders real-time training convergence curves, confusion matrices, and live flow alert tables.", styles["Bullet"]))
    story.append(Paragraph("• <b>Tier 2 (Zero Trust Security Gateway):</b> Intercepts every request via <code>@app.before_request</code>, validates the JWT signature and expiration timestamp, binds <code>g.user</code>, and enforces role permissions before any controller executes.", styles["Bullet"]))
    story.append(Paragraph("• <b>Tier 3 (Flask Blueprint Controllers):</b> Routes validated requests to specialized domain handlers for authentication, dataset catalog operations, background neural training, and live packet capture control.", styles["Bullet"]))
    story.append(Paragraph("• <b>Tier 4A & 4B (Offline ML & Online Live Detection Planes):</b> Tier 4A performs stratified sampling, anti-leakage preprocessing, and mini-batch neural training; Tier 4B captures live packets, aggregates bidirectional 5-tuple flows, extracts schema-aligned features, and predicts threat risk levels.", styles["Bullet"]))
    story.append(Paragraph("• <b>Tier 5A & 5B (SQLite Database & Artifact Repository):</b> Persists relational metadata and audit trails in SQLite (<code>database.db</code>) while storing trained models and scalers in <code>models/</code>.", styles["Bullet"]))

    story.append(Paragraph("3.2.2 Zero Trust Authentication and RBAC Middleware Architecture", styles["H2"]))
    story.append(Paragraph(
        "Figure 3.2 illustrates the block diagram of the <b>Zero Trust Authentication, JWT Verification, and Role-Based Access Control (RBAC) Subsystem</b>, and Table 3.4 defines the access control matrix enforced across the platform.",
        styles["Body"]
    ))
    add_figure(story, styles, "fig3_2_zero_trust_architecture.png",
               "Figure 3.2: Block Diagram of the Zero Trust Authentication, JWT Verification, and RBAC Enforcement Subsystem.", max_height=215)

    story.append(Paragraph("• <b>Bcrypt Password Vault (security/password.py):</b> Hashes plaintext passwords using 12-round salted Eksblowfish key expansion, preventing rainbow-table and credential-stuffing attacks.", styles["Bullet"]))
    story.append(Paragraph("• <b>Stateless HS256 JWT Engine (security/jwt_auth.py):</b> Issues signed tokens containing <code>{user_id, username, role, iat, exp}</code> valid for 8 hours and verifies token integrity on every API call.", styles["Bullet"]))
    story.append(Paragraph("• <b>RBAC Policy Gate (security/zero_trust.py) & Audit Logger (utils/logger.py):</b> Enforces least-privilege separation between <code>Admin</code> and <code>Analyst</code> roles and logs all authorized and rejected events to <code>audit_logs</code>.", styles["Bullet"]))

    add_table(
        story, styles,
        "Table 3.4: Zero Trust Role-Based Access Control (RBAC) Permission Matrix",
        ["System Operation", "API Endpoint", "Admin", "Analyst", "Unauthenticated"],
        [
            ["Operator Login & Token Issuance", "POST /api/auth/login", "Allowed", "Allowed", "Allowed"],
            ["Inspect & Compare Benchmark Datasets", "GET /dataset-list, /dataset-compare", "Allowed", "Allowed", "Denied (401)"],
            ["Upload, Select, or Delete Dataset", "POST /upload, /select; DELETE /delete", "Allowed", "Denied (403)", "Denied (401)"],
            ["Start Neural Training & Delete Model", "POST /api/model/train, /delete-active", "Allowed", "Denied (403)", "Denied (401)"],
            ["View Model Evaluation & Status", "GET /api/model/status, /report", "Allowed", "Allowed", "Denied (401)"],
            ["Control Live Capture & Export Alerts", "POST /start, /stop; GET /traffic, /export", "Allowed", "Allowed", "Denied (401)"],
            ["Inspect Immutable Security Audit Logs", "GET /audit-logs", "Allowed", "Allowed", "Denied (401)"]
        ],
        [155, 135, 60, 65, 70]
    )

    story.append(Paragraph("3.2.3 Leakage-Free Preprocessing and Neural Training Architecture", styles["H2"]))
    story.append(Paragraph(
        "Figure 3.3 presents the block diagram of the <b>Offline Data Preprocessing and Asynchronous Neural Network Training Pipeline</b> implemented in <code>preprocessing/</code> and <code>training/</code>.",
        styles["Body"]
    ))
    add_figure(story, styles, "fig3_3_preprocessing_training_architecture.png",
               "Figure 3.3: Block Diagram of the Leakage-Free Stratified Preprocessing and Asynchronous Neural Training Pipeline.", max_height=255)

    story.append(Paragraph("• <b>Blocks 1–2 (DatasetLoader & StratifiedNIDSSampler):</b> Loads raw CSV benchmarks and extracts a stratified sample (seed = 42) that preserves exact multi-class attack ratios without synthetic data fabrication.", styles["Bullet"]))
    story.append(Paragraph("• <b>Blocks 3–5 (Pre-Split Sanitizer, Imputer & Leakage Filter):</b> Converts <code>+/-Inf</code> to <code>NaN</code>, drops duplicate rows <i>before</i> train/test splitting to eliminate cross-split data leakage, imputes missing values via median/mode, and drops session identifiers (Flow ID, IPs, Timestamps).", styles["Bullet"]))
    story.append(Paragraph("• <b>Blocks 6–9 (70/15/15 Split, Train-Only Scaler, Neural Trainer & Evaluator):</b> Partitions data into 70% Train, 15% Validation, and 15% Test; fits <code>StandardScaler</code> strictly on the training set; trains the <code>(64, 32)</code> ReLU MLP via mini-batch Adam; evaluates the unseen test split; and saves versioned artifacts.", styles["Bullet"]))

    story.append(Paragraph("3.2.4 Passive Live Packet Capture and Bidirectional Flow Inference Architecture", styles["H2"]))
    story.append(Paragraph(
        "Figure 3.4 illustrates the block diagram of the <b>Passive Live Network Traffic Capture and Real-Time Zero Trust Inference Engine</b> implemented in <code>live_detection/</code>.",
        styles["Body"]
    ))
    add_figure(story, styles, "fig3_4_live_detection_architecture.png",
               "Figure 3.4: Block Diagram of Passive Live Packet Capture, 5-Tuple Flow Aggregation, and Real-Time Risk Scoring.", max_height=255)

    story.append(Paragraph("• <b>Blocks 1–4 (PacketCaptureManager & Bidirectional FlowManager):</b> Passively sniffs IP/TCP/UDP packets from the host interface using Scapy/Npcap and groups them into canonical 5-tuple bidirectional conversations in an LRU table (<code>max_flows = 5000</code>), emitting flows on TCP <code>FIN</code>/<code>RST</code>, every 5 packets, or after a 2.0s idle timeout.", styles["Bullet"]))
    story.append(Paragraph("• <b>Blocks 5–8 (FlowFeatureExtractor, LivePredictor, Risk Scorer & DetectionLogger):</b> Dynamically extracts 22 (CIC-IDS2017), 15 (UNSW-NB15), or 19 (NSL-KDD) features, applies the saved <code>StandardScaler</code>, runs neural inference, assigns <code>LOW</code>, <code>MEDIUM</code>, or <code>HIGH</code> risk levels, and logs detections to memory buffers and SQLite.", styles["Bullet"]))

    story.append(Paragraph("3.2.5 Relational Database Entity-Relationship (ER) Architecture", styles["H2"]))
    story.append(Paragraph(
        "Figure 3.5 shows the <b>Entity-Relationship (ER) Diagram</b> of the SQLite database (<code>database/init_db.py</code>), and Table 3.5 summarizes the schema and role of each of the six relational tables.",
        styles["Body"]
    ))
    add_figure(story, styles, "fig3_5_database_er_diagram.png",
               "Figure 3.5: Entity-Relationship (ER) Diagram of the SQLite Relational Persistence Layer.", max_height=255)

    add_table(
        story, styles,
        "Table 3.5: Summary of Relational Database Tables in database/init_db.py",
        ["Table Name", "Primary / Foreign Keys", "Key Columns & Attributes", "System Purpose"],
        [
            ["roles", "PK: id", "name (UNIQUE), description", "Stores Admin and Analyst RBAC role definitions."],
            ["users", "PK: id | FK: role_id -> roles.id", "username, email, password_hash, created_at", "Stores operator accounts and 12-round Bcrypt hashes."],
            ["audit_logs", "PK: id | FK: user_id -> users.id", "username, action, ip_address, status, timestamp, details", "Immutable compliance log of all security and API actions."],
            ["dataset_history", "PK: id", "filename, dataset_type, total_rows, training_rows, is_selected, missing/duplicate/infinite_count", "Catalogs benchmark CSVs, pre-scanned data quality stats, and class distributions."],
            ["model_history", "PK: id", "model_name, dataset_name, accuracy, loss, precision, recall, f1_score, artifact_path", "Records trained neural network runs, metrics, and artifact directory paths."],
            ["live_detections", "PK: id | IX: timestamp, risk_level", "source_ip, destination_ip, ports, protocol, flow_duration, packet_count, prediction, confidence, risk_level", "Persists real-time network flow classifications and Zero Trust risk alerts."]
        ],
        [75, 105, 145, 160]
    )

    story.append(PageBreak())

    # ==========================================================================
    # SECTION 3.3: MATHEMATICAL MODEL OF THE PROPOSED SYSTEM
    # ==========================================================================
    story.append(Paragraph("3.3 Mathematical Model of the Proposed System", styles["H1"]))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#CBD5E1"), spaceBefore=0, spaceAfter=6))

    story.append(Paragraph("3.3.1 Formal System State-Space Representation", styles["H2"]))
    story.append(Paragraph(
        "The proposed <b>AI-Powered Zero Trust Network Intrusion Detection System</b> is formally modeled as a 7-tuple state transformation system <i>S</i>:",
        styles["Body"]
    ))
    add_equation(story, styles, "S = &lt; I,  P,  F,  M<sub>&theta;</sub>,  Z<sub>ZT</sub>,  R<sub>risk</sub>,  O &gt;", "3.1")
    story.append(Paragraph(
        "where <i>I</i> is the input space of offline tabular datasets <i>D<sub>raw</sub></i> and live packet streams <i>P<sub>stream</sub></i>; <i>P</i> is the leakage-free preprocessing operator; <i>F</i> is the bidirectional 5-tuple flow feature extraction operator projecting packets into R<sup>1&times;d</sup> (for <i>d</i> &isin; {22, 15, 19}); <i>M<sub>&theta;</sub></i> is the parameterized neural network mapping standardized features onto the <i>C</i>-class probability simplex; <i>Z<sub>ZT</sub></i> is the Zero Trust cryptographic and RBAC verification gate; <i>R<sub>risk</sub></i> is the piecewise risk scoring function; and <i>O</i> is the relational persistence and telemetry output space.",
        styles["Body"]
    ))

    story.append(Paragraph("3.3.2 Stratified Subsampling and Data Sanitization Model", styles["H2"]))
    story.append(Paragraph(
        "Let a raw benchmark dataset <i>D<sub>raw</sub> = {(x<sub>i</sub>, y<sub>i</sub>)}<sub>i=1..N_raw</sub></i> be partitioned into <i>C</i> disjoint class subsets <i>D<sub>1</sub>, ..., D<sub>C</sub></i> where <i>|D<sub>c</sub>| = N<sub>c</sub></i>. Given a target sample size <i>N<sub>target</sub> &le; N<sub>raw</sub></i> and fixed random seed <i>S = 42</i>, <code>StratifiedNIDSSampler</code> computes the subsampling ratio <i>r</i> and per-class allocation <i>N<sub>c,sampled</sub></i>:",
        styles["Body"]
    ))
    add_equation(story, styles, "r = N<sub>target</sub> / N<sub>raw</sub> ,      N<sub>c,sampled</sub> = &lfloor; (N<sub>target</sub> / N<sub>raw</sub>) &middot; N<sub>c</sub> + 0.5 &rfloor;", "3.2")
    story.append(Paragraph(
        "This guarantees class-prior invariance: <i>P<sub>sampled</sub>(y = c) &approx; P<sub>raw</sub>(y = c) = N<sub>c</sub> / N<sub>raw</sub></i>. Next, non-finite values (<code>+/-Inf</code>) caused by zero-duration packet bursts are coerced to <code>NaN</code>, and exact duplicate records are eliminated prior to splitting. Missing numerical attributes <i>X<sub>j</sub></i> are imputed using the robust order-statistic median, while categorical attributes are imputed using the empirical mode:",
        styles["Body"]
    ))
    add_equation(story, styles, "x&#771;<sub>i,j</sub> = Median(X<sub>j</sub><sup>obs</sup>)   [if X<sub>j</sub> numeric],      x&#771;<sub>i,j</sub> = argmax<sub>v</sub> &Sigma; I(x<sub>k,j</sub> = v)   [if X<sub>j</sub> categorical]", "3.3")

    story.append(Paragraph("3.3.3 Leakage-Free Partitioning and Z-Score Standardization", styles["H2"]))
    story.append(Paragraph(
        "After removing non-generalizable session identifiers (Flow ID, IPs, Timestamps) and integer-encoding categorical strings via <code>LabelEncoder</code>, the deduplicated dataset <i>D<sub>clean</sub></i> of size <i>N</i> is partitioned via two-stage stratified splitting into <b>70% Training</b>, <b>15% Validation</b>, and <b>15% Testing</b> subsets:",
        styles["Body"]
    ))
    add_equation(story, styles, "N<sub>train</sub> = &lfloor; 0.70 &middot; N &rfloor;,    N<sub>val</sub> = &lfloor; 0.15 &middot; N &rfloor;,    N<sub>test</sub> = N - N<sub>train</sub> - N<sub>val</sub>", "3.4")
    story.append(Paragraph(
        "To prevent test distribution leakage, the feature mean vector <i>&mu;<sub>train</sub></i> and standard deviation vector <i>&sigma;<sub>train</sub></i> are fitted <b>exclusively on the 70% training partition</b>:",
        styles["Body"]
    ))
    add_equation(story, styles, "&mu;<sub>train,j</sub> = (1 / N<sub>train</sub>) &Sigma;<sub>i &isin; Train</sub> x<sub>i,j</sub> ,      &sigma;<sub>train,j</sub> = &radic;[ (1 / N<sub>train</sub>) &Sigma;<sub>i &isin; Train</sub> (x<sub>i,j</sub> - &mu;<sub>train,j</sub>)<sup>2</sup> ]", "3.5")
    story.append(Paragraph(
        "All three partitions (and subsequent live network flows) are transformed using the frozen training parameters:",
        styles["Body"]
    ))
    add_equation(story, styles, "z<sub>i,j</sub> = ( x<sub>i,j</sub> - &mu;<sub>train,j</sub> ) / ( &sigma;<sub>train,j</sub> + &epsilon; ) ,      &forall; i &isin; {Train, Val, Test, Live}", "3.6")

    story.append(Paragraph("3.3.4 Multi-Layer Neural Network Forward Propagation and Loss Function", styles["H2"]))
    story.append(Paragraph(
        "The classification engine employs a Multi-Layer Perceptron (<code>MLPClassifier</code>) with input dimension <i>d</i>, two hidden ReLU layers of widths <i>d<sub>1</sub> = 64</i> and <i>d<sub>2</sub> = 32</i>, and a <i>C</i>-unit Softmax output layer. For a standardized input flow vector <i>z &isin; R<sup>d</sup></i>, forward propagation computes:",
        styles["Body"]
    ))
    add_equation(story, styles, "h<sup>(1)</sup> = ReLU( W<sup>(1)</sup> z + b<sup>(1)</sup> ) ,      where  ReLU(u) = max(0, u) ,   W<sup>(1)</sup> &isin; R<sup>64 &times; d</sup>", "3.7")
    add_equation(story, styles, "h<sup>(2)</sup> = ReLU( W<sup>(2)</sup> h<sup>(1)</sup> + b<sup>(2)</sup> ) ,      where  W<sup>(2)</sup> &isin; R<sup>32 &times; 64</sup>,   b<sup>(2)</sup> &isin; R<sup>32</sup>", "3.8")
    add_equation(story, styles, "a = W<sup>(3)</sup> h<sup>(2)</sup> + b<sup>(3)</sup> ,      where  W<sup>(3)</sup> &isin; R<sup>C &times; 32</sup>,   b<sup>(3)</sup> &isin; R<sup>C</sup>", "3.9")
    story.append(Paragraph(
        "The output logits <i>a = [a<sub>1</sub>, ..., a<sub>C</sub>]<sup>T</sup></i> are normalized via the numerically stabilized Softmax function to yield the posterior probability distribution <i>p&#770;</i>:",
        styles["Body"]
    ))
    add_equation(story, styles, "p&#770;<sub>c</sub> = P(y = c | z; &theta;) = exp(a<sub>c</sub> - max<sub>k</sub> a<sub>k</sub>) / &Sigma;<sub>j=1..C</sub> exp(a<sub>j</sub> - max<sub>k</sub> a<sub>k</sub>)", "3.10")
    story.append(Paragraph(
        "The predicted class index is <i>y&#770; = argmax<sub>c</sub> p&#770;<sub>c</sub></i> with confidence <i>Conf = max<sub>c</sub> p&#770;<sub>c</sub></i>. During training over mini-batches of size <i>B = 32</i>, the network minimizes the L2-regularized multi-class Categorical Cross-Entropy Loss:",
        styles["Body"]
    ))
    add_equation(story, styles, "L(&theta;) = - (1 / B) &Sigma;<sub>i=1..B</sub> &Sigma;<sub>c=1..C</sub> y<sub>i,c</sub> ln( p&#770;<sub>i,c</sub> ) + (&alpha; / 2B) &Sigma;<sub>l=1..3</sub> || W<sup>(l)</sup> ||<sub>F</sub><sup>2</sup>", "3.11")

    story.append(Paragraph("3.3.5 Adam Optimization and Frobenius Weight Convergence Metric", styles["H2"]))
    story.append(Paragraph(
        "Network parameters <i>&theta;</i> are updated at mini-batch step <i>t</i> using the Adaptive Moment Estimation (Adam) optimizer with learning rate <i>&eta; = 0.001</i>, first-moment decay <i>&beta;<sub>1</sub> = 0.9</i>, and second-moment decay <i>&beta;<sub>2</sub> = 0.999</i>:",
        styles["Body"]
    ))
    add_equation(story, styles, "m<sub>t</sub> = &beta;<sub>1</sub> m<sub>t-1</sub> + (1 - &beta;<sub>1</sub>) &nabla;<sub>&theta;</sub> L(&theta;<sub>t-1</sub>) ,      v<sub>t</sub> = &beta;<sub>2</sub> v<sub>t-1</sub> + (1 - &beta;<sub>2</sub>) [ &nabla;<sub>&theta;</sub> L(&theta;<sub>t-1</sub>) ]<sup>2</sup>", "3.12")
    add_equation(story, styles, "m&#770;<sub>t</sub> = m<sub>t</sub> / (1 - &beta;<sub>1</sub><sup>t</sup>) ,    v&#770;<sub>t</sub> = v<sub>t</sub> / (1 - &beta;<sub>2</sub><sup>t</sup>) ,    &theta;<sub>t</sub> = &theta;<sub>t-1</sub> - &eta; &middot; m&#770;<sub>t</sub> / ( &radic;v&#770;<sub>t</sub> + 10<sup>-8</sup> )", "3.13")
    story.append(Paragraph(
        "To mathematically verify training convergence at the end of each epoch <i>e &isin; {1, ..., E}</i>, <code>NIDSTrainer</code> computes the cumulative Frobenius weight update norm <i>&Delta;W<sup>(e)</sup></i> across all three layer weight matrices:",
        styles["Body"]
    ))
    add_equation(story, styles, "&Delta;W<sup>(e)</sup> = &Sigma;<sub>l=1..3</sub> || W<sup>(l, e)</sup> - W<sup>(l, e-1)</sup> ||<sub>F</sub> = &Sigma;<sub>l=1..3</sub> &radic;[ &Sigma;<sub>p</sub> &Sigma;<sub>q</sub> | W<sub>p,q</sub><sup>(l, e)</sup> - W<sub>p,q</sub><sup>(l, e-1)</sup> |<sup>2</sup> ]", "3.14")

    story.append(Paragraph("3.3.6 Bidirectional 5-Tuple Network Flow Feature Formulation", styles["H2"]))
    story.append(Paragraph(
        "In the live detection engine (<code>FlowManager</code> and <code>FlowFeatureExtractor</code>), each packet with endpoints <i>e<sub>src</sub> = (IP<sub>src</sub>, Port<sub>src</sub>)</i>, <i>e<sub>dst</sub> = (IP<sub>dst</sub>, Port<sub>dst</sub>)</i>, and protocol <i>proto</i> is mapped to a direction-invariant canonical 5-tuple key:",
        styles["Body"]
    ))
    add_equation(story, styles, "Key(p) = min(e<sub>src</sub>, e<sub>dst</sub>)  &lt;-&gt;  max(e<sub>src</sub>, e<sub>dst</sub>)  @  proto", "3.15")
    story.append(Paragraph(
        "For a bidirectional flow comprising <i>K</i> packets with arrival timestamps <i>t<sub>1</sub> &le; t<sub>2</sub> &le; ... &le; t<sub>K</sub></i>, forward bytes <i>B<sub>fwd</sub></i>, and backward bytes <i>B<sub>bwd</sub></i>, the flow duration <i>T<sub>dur</sub></i>, byte throughput, and packet rate are:",
        styles["Body"]
    ))
    add_equation(story, styles, "T<sub>dur</sub> = max( t<sub>K</sub> - t<sub>1</sub>, 10<sup>-6</sup> ) ,    Bytes/s = (B<sub>fwd</sub> + B<sub>bwd</sub>) / T<sub>dur</sub> ,    Pkts/s = K / T<sub>dur</sub>", "3.16")
    story.append(Paragraph(
        "Given consecutive packet inter-arrival times <i>&Delta;t<sub>k</sub> = (t<sub>k+1</sub> - t<sub>k</sub>) &times; 10<sup>6</sup></i> (in microseconds for CIC-IDS2017), the flow IAT mean and standard deviation are:",
        styles["Body"]
    ))
    add_equation(story, styles, "&mu;<sub>IAT</sub> = [ 1 / (K - 1) ] &Sigma;<sub>k=1..K-1</sub> &Delta;t<sub>k</sub> ,      &sigma;<sub>IAT</sub> = &radic;[ (1 / (K - 1)) &Sigma;<sub>k=1..K-1</sub> (&Delta;t<sub>k</sub> - &mu;<sub>IAT</sub>)<sup>2</sup> ]", "3.17")

    story.append(Paragraph("3.3.7 Zero Trust Cryptographic Verification and Risk Scoring Model", styles["H2"]))
    story.append(Paragraph(
        "Every protected API request carrying a JWT token <i>H.P.S<sub>sig</sub></i> and targeting an endpoint with allowed roles <i>R<sub>allowed</sub></i> is evaluated by the boolean Zero Trust gate <i>Z<sub>ZT</sub></i>:",
        styles["Body"]
    ))
    add_equation(story, styles, "Z<sub>ZT</sub> = I( HMAC-SHA256(K<sub>secret</sub>, H.P) == S<sub>sig</sub> ) &and; I( t<sub>now</sub> &lt; exp ) &and; I( role &isin; R<sub>allowed</sub> )", "3.18")
    story.append(Paragraph(
        "For live network flows classified by <code>LivePredictor</code> with decoded label <i>L&#770;</i> and Softmax confidence <i>Conf = max<sub>c</sub> p&#770;<sub>c</sub></i>, the Zero Trust risk level is assigned via the piecewise function:",
        styles["Body"]
    ))
    add_equation(story, styles, "R<sub>risk</sub>(L&#770;, Conf) = { LOW, if L&#770; &isin; Benign &or; Conf &lt; 0.60 ;   MEDIUM, if Attack &and; 0.60 &le; Conf &lt; 0.85 ;   HIGH, if Attack &and; Conf &ge; 0.85 }", "3.19")

    story.append(Paragraph("3.3.8 Multi-Class Classification Evaluation Metrics", styles["H2"]))
    story.append(Paragraph(
        "Given the <i>C &times; C</i> confusion matrix <i>M</i> on the unseen 15% test split (where <i>TP<sub>c</sub> = M<sub>c,c</sub></i>, <i>FP<sub>c</sub> = &Sigma;<sub>i&ne;c</sub> M<sub>i,c</sub></i>, and <i>FN<sub>c</sub> = &Sigma;<sub>j&ne;c</sub> M<sub>c,j</sub></i>), overall Accuracy and support-weighted Precision, Recall, and F1-Score are computed as:",
        styles["Body"]
    ))
    add_equation(story, styles, "Accuracy = ( &Sigma;<sub>c=1..C</sub> TP<sub>c</sub> ) / N<sub>test</sub> ,      Precision<sub>c</sub> = TP<sub>c</sub> / (TP<sub>c</sub> + FP<sub>c</sub>) ,      Recall<sub>c</sub> = TP<sub>c</sub> / (TP<sub>c</sub> + FN<sub>c</sub>)", "3.20")
    add_equation(story, styles, "F1<sub>c</sub> = ( 2 &middot; Precision<sub>c</sub> &middot; Recall<sub>c</sub> ) / ( Precision<sub>c</sub> + Recall<sub>c</sub> ) ,      F1<sub>weighted</sub> = &Sigma;<sub>c=1..C</sub> ( N<sub>test,c</sub> / N<sub>test</sub> ) &middot; F1<sub>c</sub>", "3.21")

    story.append(PageBreak())

    # ==========================================================================
    # SECTION 3.4: SYSTEM ALGORITHMS AND FLOWCHARTS
    # ==========================================================================
    story.append(Paragraph("3.4 System Algorithms and Flowcharts", styles["H1"]))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#CBD5E1"), spaceBefore=0, spaceAfter=6))

    story.append(Paragraph(
        "This section presents the five core algorithms and their corresponding execution flowcharts (Figures 3.6 through 3.10) governing Zero Trust security enforcement, leakage-free data preprocessing, asynchronous neural network training, passive 5-tuple flow aggregation, and real-time threat inference.",
        styles["Body"]
    ))

    # Algorithm 3.1
    story.append(Paragraph("3.4.1 Algorithm 3.1 & Flowchart: Zero Trust JWT Authentication and RBAC Enforcement", styles["H2"]))
    algo3_1 = """Input  : Incoming HTTP Request R, Secret Key K_secret, Endpoint Allowed Roles R_allowed
Output : Authorized Controller Execution (HTTP 200) or Security Rejection (HTTP 401/403)
----------------------------------------------------------------------------------------
 1: Extract JWT token T from 'Authorization: Bearer' header or 'jwt_token' cookie
 2: if T is NULL or empty then
 3:     Log AuditEvent("UNAUTHORIZED_ACCESS", "REJECTED", R.remote_addr)
 4:     return HTTP 401 Unauthorized
 5: end if
 6: Verify HMAC-SHA256 signature of T using K_secret and check (t_now < payload.exp)
 7: if signature invalid OR token expired then
 8:     Log AuditEvent("INVALID_TOKEN_ACCESS", "REJECTED", R.remote_addr)
 9:     return HTTP 401 Unauthorized
10: end if
11: Bind decoded identity {user_id, username, role} to Flask context g.user
12: if g.user.role not in R_allowed then
13:     Log AuditEvent("RBAC_ACCESS_DENIED", "REJECTED", g.user.username, R.remote_addr)
14:     return HTTP 403 Forbidden
15: end if
16: Execute target Flask Blueprint controller and log action to SQLite audit_logs"""
    add_code_block(story, styles, "ALGORITHM 3.1: Zero Trust JWT Authentication & RBAC Policy Gate", algo3_1)
    add_figure(story, styles, "fig3_6_zero_trust_flowchart.png",
               "Figure 3.6: Flowchart of Zero Trust JWT Authentication and RBAC Policy Enforcement.", max_height=265)
    story.append(Paragraph(
        "<b>Explanation of Algorithm 3.1 & Flowchart 3.6:</b> Every API request is intercepted before controller execution. If the JWT token is missing, tampered with, or expired (> 8 hours), the request is rejected with HTTP 401. Next, the user's role in <code>g.user['role']</code> is checked against the route's allowed roles (<code>Admin</code> vs. <code>Analyst</code>); unauthorized privilege escalation attempts are blocked with HTTP 403 and recorded in <code>audit_logs</code>.",
        styles["Body"]
    ))

    # Algorithm 3.2
    story.append(Paragraph("3.4.2 Algorithm 3.2 & Flowchart: Leakage-Free Stratified Sampling and Data Preprocessing", styles["H2"]))
    algo3_2 = """Input  : Raw Benchmark CSV Path P_raw, Target Sample Size N_target, Random Seed S = 42
Output : Standardized Tensors (X_train, y_train, X_val, y_val, X_test, y_test), Scaler, Encoder
----------------------------------------------------------------------------------------
 1: Load raw DataFrame D_raw from P_raw and identify target label column
 2: if N_target < |D_raw| then
 3:     Perform stratified sampling (seed S=42) to extract D_s preserving class ratios
 4: else Set D_s <- D_raw
 5: Replace all +Inf and -Inf values in numerical columns of D_s with NaN
 6: Deduplicate rows BEFORE splitting: D_clean <- D_s.drop_duplicates()
 7: Impute remaining NaNs: Categorical -> Mode(X_j) | Numerical -> Median(X_j)
 8: Drop leakage metadata columns (Flow ID, Source/Dest IP, Source Port, Timestamp)
 9: Encode categorical features and target label vector y via LabelEncoder
10: Perform two-stage stratified split: 70% Train | 15% Validation | 15% Test
11: Fit StandardScaler ONLY on X_train_raw to compute (mu_train, sigma_train)
12: Transform X_train, X_val, and X_test using frozen (mu_train, sigma_train)
13: Serialize scaler.pkl and label_encoder.pkl; return standardized splits"""
    add_code_block(story, styles, "ALGORITHM 3.2: Leakage-Free Stratified Sampling & Data Preprocessing", algo3_2)
    add_figure(story, styles, "fig3_7_preprocessing_flowchart.png",
               "Figure 3.7: Flowchart of the Leakage-Free Stratified Sampling and Preprocessing Pipeline.", max_height=230)
    story.append(Paragraph(
        "<b>Explanation of Algorithm 3.2 & Flowchart 3.7:</b> Preserves exact minority and majority attack proportions during subsampling (Lines 2–4), eliminates duplicate records <i>prior</i> to splitting so identical rows cannot leak across train and test sets (Line 6), imputes nulls via median/mode (Line 7), strips session identifiers (Line 8), and fits <code>StandardScaler</code> strictly on the 70% training partition (Lines 10–12).",
        styles["Body"]
    ))

    # Algorithm 3.3
    story.append(Paragraph("3.4.3 Algorithm 3.3 & Flowchart: Asynchronous Mini-Batch Neural Network Training", styles["H2"]))
    algo3_3 = """Input  : Standardized Splits (X_train, y_train, X_val, y_val, X_test, y_test),
         Epochs E = 10, Batch Size B = 32, Learning Rate eta = 0.001, Seed S = 42
Output : Serialized Model model.joblib, Evaluation Report evaluation_report.json
----------------------------------------------------------------------------------------
 1: Spawn background daemon thread executing NIDSTrainer.train()
 2: Initialize MLPClassifier(hidden_layer_sizes=(64, 32), activation="relu",
                             solver="adam", learning_rate_init=eta, random_state=S)
 3: for epoch e = 1 to E do
 4:     Shuffle (X_train, y_train) using deterministic seed (S + e)
 5:     for each mini-batch (X_b, y_b) of size B = 32 do
 6:         Execute Adam gradient update: nn.partial_fit(X_b, y_b, classes=all_classes)
 7:     end for
 8:     Compute training and validation Accuracy and Cross-Entropy Loss (log_loss)
 9:     Compute Frobenius weight update norm: Delta_W^(e) = Sum_l || W_l^(e) - W_l^(e-1) ||_F
10:     Update live training_status telemetry dictionary for UI polling
11: end for
12: Evaluate unseen 15% test split (X_test, y_test) via ModelEvaluator.evaluate()
13: Save model.joblib, scaler.pkl, encoder.pkl, and report JSON; commit ModelHistory to DB"""
    add_code_block(story, styles, "ALGORITHM 3.3: Asynchronous Mini-Batch Neural Training & Convergence Tracking", algo3_3)
    add_figure(story, styles, "fig3_8_training_flowchart.png",
               "Figure 3.8: Flowchart of Asynchronous Mini-Batch Neural Training and Frobenius Convergence Verification.", max_height=230)
    story.append(Paragraph(
        "<b>Explanation of Algorithm 3.3 & Flowchart 3.8:</b> Runs in a background worker thread so the Flask server remains responsive. Each epoch shuffles the training data with seed <code>S + e</code>, iterates over mini-batches of 32 flows using <code>partial_fit</code>, and logs training/validation cross-entropy loss, accuracy, and the Frobenius weight norm <code>Delta_W^(e)</code> before evaluating the unseen 15% holdout test split.",
        styles["Body"]
    ))

    # Algorithm 3.4
    story.append(Paragraph("3.4.4 Algorithm 3.4 & Flowchart: Passive Packet Capture and 5-Tuple Flow Aggregation", styles["H2"]))
    algo3_4 = """Input  : Network Interface iface, Idle Timeout T_idle = 2.0s, Batch Threshold K_emit = 5
Output : Emitted Bidirectional NetworkFlow Records for Real-Time Inference
----------------------------------------------------------------------------------------
 1: Initialize LRU flow cache active_flows <- OrderedDict(max_flows = 5000)
 2: Start background threads: _sniff_worker(iface) and _reaper_worker(interval = 1.0s)
 3: for each captured packet pkt from Scapy sniff(iface, store=False) do
 4:     Parse IP/TCP/UDP headers (src_ip, dst_ip, src_port, dst_port, proto, pkt_len, flags)
 5:     Construct canonical key: min((src_ip,sport),(dst_ip,dport)) <-> max(...) @ proto
 6:     Create or retrieve NetworkFlow in active_flows (evict oldest LRU if full)
 7:     if pkt direction matches flow initiator (Forward) then
 8:         Increment fwd_packets, fwd_bytes, fwd_lengths, sttl, and sloss
 9:     else Increment bwd_packets, bwd_bytes, bwd_lengths, dttl, and dloss
10:     Update TCP flag counters (FIN, SYN, RST, PSH, ACK, URG) and connection state
11:     if (FIN or RST in flags) OR (total_pkts - last_emitted >= K_emit) then
12:         Emit NetworkFlow snapshot to FlowFeatureExtractor and LivePredictor
13:     end if
14: end for
15: [Reaper Thread]: Every 1.0s, emit and remove flows where (t_now - last_time >= T_idle)"""
    add_code_block(story, styles, "ALGORITHM 3.4: Passive Packet Sniffing & Bidirectional 5-Tuple Flow Aggregation", algo3_4)
    add_figure(story, styles, "fig3_9_flow_aggregation_flowchart.png",
               "Figure 3.9: Flowchart of Passive Packet Sniffing and Canonical 5-Tuple Bidirectional Flow Aggregation.", max_height=265)
    story.append(Paragraph(
        "<b>Explanation of Algorithm 3.4 & Flowchart 3.9:</b> Maps both forward and backward packets of a network conversation to a single canonical 5-tuple key in an LRU cache (<code>max_flows = 5000</code>). Tracks directional byte counts, packet lengths, inter-arrival times, and TCP flags, emitting flows immediately upon connection teardown (<code>FIN</code>/<code>RST</code>), every 5 packets, or after 2.0 seconds of inactivity.",
        styles["Body"]
    ))

    # Algorithm 3.5
    story.append(Paragraph("3.4.5 Algorithm 3.5 & Flowchart: Dynamic Feature Extraction, Live Inference, and Risk Scoring", styles["H2"]))
    algo3_5 = """Input  : Emitted NetworkFlow F, Active Model M_theta, Fitted Scaler S_train, Encoder E_y
Output : Persisted LiveDetection Record & Real-Time SOC Alert
----------------------------------------------------------------------------------------
 1: Read expected feature dimension d <- S_train.n_features_in_
 2: if d == 22 then Extract 22 CIC-IDS2017 flow, length, IAT, and flag features -> X_raw
 3: else if d == 15 then Extract 15 UNSW-NB15 dur, rate, TTL, load, and loss features -> X_raw
 4: else if d == 19 then Extract 19 NSL-KDD flow and 2.0s sliding-window features -> X_raw
 5: Replace any NaN/Inf in X_raw with 0.0 and standardize: Z_flow <- S_train.transform(X_raw)
 6: Compute Softmax posteriors P_hat <- M_theta.predict_proba(Z_flow)[0]
 7: Set y_hat <- argmax(P_hat), Confidence Conf <- max(P_hat)
 8: Decode class label L_hat <- E_y.inverse_transform([y_hat])[0]
 9: if L_hat in {"normal", "benign", "0"} OR Conf < 0.60 then
10:     risk_level <- "LOW"; status <- "Normal"
11: else if Conf >= 0.85 then risk_level <- "HIGH"; status <- "Alert"
12: else risk_level <- "MEDIUM"; status <- "Alert"
13: Append record to DetectionLogger ring buffers and insert row into SQLite live_detections"""
    add_code_block(story, styles, "ALGORITHM 3.5: Dynamic Schema Feature Extraction, Inference & Risk Scoring", algo3_5)
    add_figure(story, styles, "fig3_10_live_inference_flowchart.png",
               "Figure 3.10: Flowchart of Dynamic Schema Feature Extraction, Neural Inference, and Zero Trust Risk Scoring.", max_height=265)
    story.append(Paragraph(
        "<b>Explanation of Algorithm 3.5 & Flowchart 3.10:</b> Inspects the active model's feature dimensionality (<code>d = 22, 15, or 19</code>) to compute the exact feature vector required, normalizes the vector using the training scaler, executes Softmax inference, applies the Zero Trust risk thresholds (<code>0.60</code> and <code>0.85</code>), and persists the detection to memory ring buffers and SQLite.",
        styles["Body"]
    ))

    story.append(PageBreak())

    # ==========================================================================
    # SECTION 3.5: SYSTEM IMPLEMENTATION AND VERIFICATION SUMMARY
    # ==========================================================================
    story.append(Paragraph("3.5 System Implementation and Verification Summary", styles["H1"]))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#CBD5E1"), spaceBefore=0, spaceAfter=6))

    story.append(Paragraph("3.5.1 RESTful API Controller Implementation Summary", styles["H2"]))
    story.append(Paragraph(
        "The backend application is initialized via the <code>create_app()</code> factory in <code>app.py</code>, which configures SQLite persistence, seeds the default roles (<code>Admin</code>, <code>Analyst</code>) and benchmark catalogs, and registers four modular Flask Blueprints. Table 3.6 summarizes the core REST API endpoints implemented in <code>api/</code>.",
        styles["Body"]
    ))
    add_table(
        story, styles,
        "Table 3.6: Core RESTful API Endpoints Implemented Across Flask Blueprints",
        ["Blueprint Module", "HTTP Endpoint", "Access Policy", "Functional Implementation"],
        [
            ["auth_routes.py", "POST /api/auth/login", "Public", "Verifies 12-round Bcrypt hash, logs USER_LOGIN, issues 8-hour HS256 JWT."],
            ["auth_routes.py", "POST /api/auth/change-password", "@jwt_required", "Validates current password hash and updates Bcrypt digest in SQLite."],
            ["dataset_routes.py", "POST /api/dataset/upload, /select", "Admin Only", "Uploads CSV, scans NaNs/duplicates/classes, and marks active dataset."],
            ["model_routes.py", "POST /api/model/train", "Admin Only", "Validates parameters and spawns async thread start_training_in_background."],
            ["model_routes.py", "GET /api/model/status, /report", "@jwt_required", "Streams live epoch progress, loss/accuracy curves, and holdout test report."],
            ["live_detection_routes.py", "GET /interfaces, /models", "Admin, Analyst", "Lists Windows network adapters, Npcap status, and compatible models."],
            ["live_detection_routes.py", "POST /start, /stop, /replay", "Admin, Analyst", "Starts/stops passive Scapy sniffer or replays test flows through LivePredictor."],
            ["live_detection_routes.py", "GET /traffic, /export", "Admin, Analyst", "Returns live flow table, high-risk alerts, throughput KPIs, and CSV export."]
        ],
        [90, 125, 65, 205]
    )

    story.append(Paragraph("3.5.2 Experimental Training Convergence Verification on CIC-IDS2017", styles["H2"]))
    story.append(Paragraph(
        "To verify the end-to-end implementation of the stratified sampler, anti-leakage preprocessor, and mini-batch neural network trainer, Table 3.7 presents the recorded epoch-by-epoch convergence telemetry on the <b>CIC-IDS2017</b> benchmark dataset (<code>N<sub>sampled</sub> = 25,000</code> flows, 70/15/15 split, <code>batch_size = 32</code>, <code>learning_rate = 0.001</code>, <code>seed = 42</code>). Across 10 epochs, training loss decreases monotonically from <code>0.8588</code> to <code>0.5273</code>, the Frobenius weight norm <code>Delta W</code> converges from <code>13.6815</code> to <code>1.1323</code>, and holdout test evaluation achieves <b>84.72% accuracy</b> and a <b>0.9728 macro ROC-AUC</b>.",
        styles["Body"]
    ))
    add_table(
        story, styles,
        "Table 3.7: Verified Epoch-by-Epoch Neural Network Convergence on CIC-IDS2017",
        ["Epoch", "Train Accuracy", "Validation Accuracy", "Train Cross-Entropy Loss", "Validation Loss", "Frobenius Norm (Delta W)"],
        [
            ["Epoch 1", "74.26%", "74.43%", "0.8588", "0.8657", "13.6815"],
            ["Epoch 2", "76.78%", "76.80%", "0.7069", "0.7158", "3.5882"],
            ["Epoch 3", "78.08%", "78.37%", "0.6606", "0.6691", "2.6581"],
            ["Epoch 4", "79.77%", "80.11%", "0.6305", "0.6388", "2.1895"],
            ["Epoch 5", "80.52%", "80.93%", "0.6087", "0.6186", "1.8841"],
            ["Epoch 6", "81.65%", "81.95%", "0.5892", "0.5994", "1.6498"],
            ["Epoch 7", "82.61%", "82.88%", "0.5718", "0.5819", "1.4723"],
            ["Epoch 8", "83.48%", "83.73%", "0.5564", "0.5668", "1.3311"],
            ["Epoch 9", "84.12%", "84.29%", "0.5421", "0.5529", "1.2189"],
            ["Epoch 10", "84.60%", "84.69%", "0.5273", "0.5389", "1.1323"],
            ["Holdout Test (15%)", "—", "84.72% (Test Acc)", "—", "0.5355 (Test Loss)", "Macro ROC-AUC = 0.9728"]
        ],
        [80, 75, 85, 85, 80, 80]
    )

    story.append(Paragraph("3.5.3 Chapter Summary", styles["H2"]))
    story.append(Paragraph(
        "This chapter presented the system design and implementation of the <b>AI-Powered Zero Trust Network Intrusion Detection System</b>. Section 3.1 described the proposed work, core modules, workflows, and multi-dataset compatibility. Section 3.2 detailed the five-tier system architecture and block diagrams (Figures 3.1–3.5). Section 3.3 formulated the mathematical model covering stratified sampling, leakage-free scaling, neural network forward/backward propagation, 5-tuple flow kinematics, and Zero Trust risk scoring (Equations 3.1–3.21). Section 3.4 presented the five formal system algorithms and flowcharts (Algorithms 3.1–3.5, Figures 3.6–3.10), and Section 3.5 summarized the REST API implementation and experimental training convergence.",
        styles["Body"]
    ))

    doc.build(story, canvasmaker=Chapter3NumberedCanvas)
    print(f"Successfully generated PDF: {OUTPUT_PDF}")


if __name__ == "__main__":
    generate_pdf()
