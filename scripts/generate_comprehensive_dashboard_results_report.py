import os
import shutil
import sqlite3
import json

# ReportLab imports
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    KeepTogether, HRFlowable, PageBreak, Image as RLImage
)
from reportlab.pdfgen import canvas

# Docx imports
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

OUTPUT_DIR = r"E:\ML\reports"
DESKTOP_DIR = r"C:\Users\HP\OneDrive\Desktop\ML"
FIG_DIR = r"E:\ML\report\figures"

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(DESKTOP_DIR, exist_ok=True)

PDF_FILENAME = "Zero_Trust_AI_NIDS_Comprehensive_Dashboard_Execution_Report.pdf"
DOCX_FILENAME = "Zero_Trust_AI_NIDS_Comprehensive_Dashboard_Execution_Report.docx"

PDF_PATH = os.path.join(OUTPUT_DIR, PDF_FILENAME)
DOCX_PATH = os.path.join(OUTPUT_DIR, DOCX_FILENAME)

class NumberedCanvas(canvas.Canvas):
    """Two-pass canvas for header and Page X of Y footer."""
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
            self.draw_page_decorations(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_decorations(self, page_count):
        self.saveState()
        w, h = A4
        if self._pageNumber > 1:
            # Header
            self.setFont("Helvetica-Bold", 8)
            self.setFillColor(colors.HexColor("#1E3A8A"))
            self.drawString(48, h - 34, "ZERO-TRUST AI-POWERED NETWORK INTRUSION DETECTION SYSTEM")
            self.setFont("Helvetica", 8)
            self.setFillColor(colors.HexColor("#64748B"))
            self.drawRightString(w - 48, h - 34, "Dashboard Execution & Technical Analysis Report")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.7)
            self.line(48, h - 40, w - 48, h - 40)

        # Footer
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.7)
        self.line(48, 42, w - 48, 42)
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        self.drawString(48, 30, "JNNCE — Dept. of Information Science & Engineering (Batch 34)")
        self.drawRightString(w - 48, 30, f"Page {self._pageNumber} of {page_count}")
        self.restoreState()

def build_pdf():
    doc = SimpleDocTemplate(
        PDF_PATH,
        pagesize=A4,
        leftMargin=48,
        rightMargin=48,
        topMargin=50,
        bottomMargin=50
    )

    styles = getSampleStyleSheet()
    normal = styles["Normal"]

    # Typography styles
    title_style = ParagraphStyle(
        "DocTitle", parent=normal,
        fontName="Helvetica-Bold", fontSize=18, leading=22,
        textColor=colors.HexColor("#0F172A"), alignment=TA_CENTER
    )
    subtitle_style = ParagraphStyle(
        "DocSubTitle", parent=normal,
        fontName="Helvetica-Bold", fontSize=10.5, leading=14,
        textColor=colors.HexColor("#1E3A8A"), alignment=TA_CENTER
    )
    meta_style = ParagraphStyle(
        "MetaText", parent=normal,
        fontName="Helvetica", fontSize=8.5, leading=12,
        textColor=colors.HexColor("#475569"), alignment=TA_CENTER
    )
    h1_style = ParagraphStyle(
        "Heading1_Custom", parent=normal,
        fontName="Helvetica-Bold", fontSize=12, leading=15,
        textColor=colors.HexColor("#1E3A8A"), spaceBefore=8, spaceAfter=4,
        keepWithNext=True
    )
    h2_style = ParagraphStyle(
        "Heading2_Custom", parent=normal,
        fontName="Helvetica-Bold", fontSize=9.5, leading=12.5,
        textColor=colors.HexColor("#0F172A"), spaceBefore=5, spaceAfter=2,
        keepWithNext=True
    )
    body_style = ParagraphStyle(
        "Body_Custom", parent=normal,
        fontName="Times-Roman", fontSize=8.8, leading=12.2,
        textColor=colors.HexColor("#1E293B"), alignment=TA_JUSTIFY,
        spaceAfter=4
    )
    bullet_style = ParagraphStyle(
        "Bullet_Custom", parent=body_style,
        leftIndent=12, firstLineIndent=-8, spaceAfter=2
    )
    term_box = ParagraphStyle(
        "TermBox", parent=normal,
        fontName="Times-Italic", fontSize=8.4, leading=11.4,
        textColor=colors.HexColor("#0369A1"), leftIndent=10, spaceAfter=3
    )
    fig_caption = ParagraphStyle(
        "FigCaption", parent=normal,
        fontName="Helvetica-Bold", fontSize=8, leading=10.5,
        textColor=colors.HexColor("#334155"), alignment=TA_CENTER, spaceBefore=3, spaceAfter=6
    )
    tbl_cell = ParagraphStyle(
        "TableCell", parent=normal,
        fontName="Helvetica", fontSize=7.5, leading=9.5,
        textColor=colors.HexColor("#0F172A")
    )
    tbl_cell_bold = ParagraphStyle("TableCellBold", parent=tbl_cell, fontName="Helvetica-Bold")
    tbl_cell_hdr = ParagraphStyle("TableCellHdr", parent=tbl_cell, fontName="Helvetica-Bold", textColor=colors.white)

    story = []

    # ================= PAGE 1: TITLE & EXECUTIVE SUMMARY =================
    story.append(Paragraph("ZERO-TRUST AI-POWERED NETWORK INTRUSION DETECTION SYSTEM", title_style))
    story.append(Spacer(1, 3))
    story.append(Paragraph("Operational Dashboard Guide, Sequential Execution Analysis & Technical Telemetry", subtitle_style))
    story.append(Spacer(1, 3))
    story.append(Paragraph("<b>Author:</b> Lohith Gopi (Batch 34) &nbsp;|&nbsp; <b>Institution:</b> JNNCE, Shivamogga &nbsp;|&nbsp; <b>Dept:</b> Information Science & Engineering", meta_style))
    story.append(Spacer(1, 5))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#1E3A8A"), spaceAfter=8))

    story.append(Paragraph("1. Executive Summary & Sequential Execution Framework", h1_style))
    story.append(Paragraph(
        "This technical document provides an exhaustive, visual, and operational analysis of the <b>Zero-Trust AI-Powered Network Intrusion Detection System (Zero-Trust NIDS)</b>. "
        "The platform bridges machine learning classification with a live, modern Security Operations Center (SOC) dashboard. "
        "Unlike monolithic academic scripts, this system enforces the Zero-Trust security paradigm—<b>'Never Trust, Always Verify'</b>—across all interactive web views and background pipelines.",
        body_style
    ))
    story.append(Paragraph(
        "To provide a defensible foundation for faculty review and technical viva examinations, this report captures each dashboard interface in its <b>exact chronological order of execution</b>. "
        "For every operational view, three dimensions are rigorously presented: (1) <b>Visual Interface Breakdown</b>, explaining all metric cards, badges, and controls; "
        "(2) <b>Theoretical & Technical Terms</b>, defining the underlying computer science, cybersecurity, and mathematical principles; and "
        "(3) <b>Underlying Process</b>, detailing the API interactions, database operations, and algorithmic routines triggered by the user.",
        body_style
    ))

    story.append(Paragraph("<b>End-to-End System Execution Sequence:</b>", h2_style))
    exec_steps = [
        "<b>Stage 0: Portal Entry & Authentication:</b> Single-Page Application (SPA) initialization, identity assertion, 12-round Bcrypt hash verification, and stateless HS256 JWT issuance.",
        "<b>Stage 1: Ingestion & Dataset Preparation:</b> Benchmark dataset cataloging (UNSW-NB15, NSL-KDD, CIC-IDS2017), stratified sampling, deduplication, and zero-leakage feature scaling.",
        "<b>Stage 2: Offline Model Training & Convergence:</b> Asynchronous multi-algorithm optimization (SVM RBF, Random Forest, Logistic Regression, Deep MLP), loss tracking, and weight update Frobenius norm evaluation.",
        "<b>Stage 3: Holdout Performance Evaluation:</b> Testing on unseen 15% partitions ($N_{test}=3,750$), computing Confusion Matrices, ROC-AUC curves, and multi-class precision/recall metrics.",
        "<b>Stage 4: Model Checkpointing & Hot-Swapping:</b> Serializing optimal weights into `.joblib` checkpoints, registering active metadata, and binding the model to the live inference engine.",
        "<b>Stage 5: Live Network Sniffing & Real-Time Classification:</b> Capturing live raw 802.11/Ethernet packets via Scapy, assembling bidirectional 5-tuple flows, and assigning piecewise threat risk tiers.",
        "<b>Stage 6: Zero-Trust Governance & Forensic Auditing:</b> Enforcing Role-Based Access Control (`Admin` vs `Analyst`), intercepting privilege escalation attempts, and recording tamper-evident audit logs."
    ]
    for step in exec_steps:
        story.append(Paragraph(f"• {step}", bullet_style))

    story.append(PageBreak())

    # ================= PAGE 2: MASTER ARCHITECTURE & ROLES =================
    story.append(Paragraph("2. Master Architectural Workflow & Role Separation", h1_style))
    story.append(Paragraph(
        "The system follows a multi-tier decoupled architecture: a React 18 Single-Page Application frontend communicates via authenticated REST APIs with a Python Flask backend, supported by SQLite persistence and Scapy network capture.",
        body_style
    ))
    img_arch = os.path.join(FIG_DIR, "fig3_1_master_architecture.png")
    if os.path.exists(img_arch):
        story.append(RLImage(img_arch, width=460, height=195))
        story.append(Paragraph("Figure 2.1: Master Architecture Diagram Illustrating End-to-End Data, Control, and Model Flows", fig_caption))

    story.append(Paragraph("<b>Zero-Trust Role Separation (Admin vs Analyst):</b>", h2_style))
    story.append(Paragraph(
        "A cornerstone of the system is the practical implementation of the <b>Principle of Least Privilege (PoLP)</b> and <b>Separation of Duties (SoD)</b>:",
        body_style
    ))
    story.append(Paragraph(
        "• <b>Administrator (`Admin`):</b> Full system authority. Can initiate asynchronous model training runs, activate/hot-swap active detection models, delete existing model checkpoints, and delete cataloged datasets. Has access to all 8 dashboard tabs.",
        bullet_style
    ))
    story.append(Paragraph(
        "• <b>Security Analyst (`Analyst`):</b> Restricted monitoring authority. Can view datasets, inspect comparison matrices, initiate live packet sniffing, monitor live threat alerts, evaluate model performance, and examine audit logs. The Model Training tab is dynamically removed from their UI, direct URL navigation is redirected, and API endpoints return HTTP 403 Forbidden.",
        bullet_style
    ))
    story.append(Paragraph(
        "• <b>Analyst Live Training HUD:</b> When an Admin triggers background training, logged-in Analysts receive a prominent read-only telemetry banner (<i>'⚡ LIVE ADMIN TRAINING'</i>) displaying live epoch progress, loss, and accuracy without giving them controls to disrupt training.",
        bullet_style
    ))
    story.append(PageBreak())

    # ================= PAGE 3: SCREEN 1 - LANDING PAGE =================
    story.append(Paragraph("3. Screen 1: Academic Landing Page & Public SOC Portal Entry", h1_style))
    story.append(Paragraph(
        "The landing page serves as the public-facing entry point, establishing institutional attributions, project context, and the identity boundary for Zero-Trust access.",
        body_style
    ))
    img_s1 = os.path.join(FIG_DIR, "ui_1_landing_page.png")
    if os.path.exists(img_s1):
        story.append(RLImage(img_s1, width=440, height=185))
        story.append(Paragraph("Figure 3.1: Academic Landing Page of the Proposed Zero-Trust AI-Powered NIDS", fig_caption))

    story.append(Paragraph("<b>A. Visual Interface Breakdown:</b>", h2_style))
    story.append(Paragraph("• <b>Hero Header & Institutional Branding:</b> Identifies the project under the Department of Information Science & Engineering, JNNCE Shivamogga, Batch No. 34.", bullet_style))
    story.append(Paragraph("• <b>System Status Indicator:</b> Displays real-time operational status (Active Model Version, Database Connection State, Passive Sniffer Readiness).", bullet_style))
    story.append(Paragraph("• <b>Access Control CTA Button:</b> A prominent <i>'Launch Security Portal'</i> button directing the user to the Zero-Trust authentication gateway.", bullet_style))

    story.append(Paragraph("<b>B. Theoretical & Technical Terms:</b>", h2_style))
    story.append(Paragraph("<b>Single-Page Application (SPA):</b> A web application architecture that loads a single HTML page and dynamically updates content as the user interacts, eliminating full-page browser reloads.", term_box))
    story.append(Paragraph("<b>Identity Boundary:</b> The security demarcation line separating unauthenticated public traffic from protected internal system endpoints.", term_box))
    story.append(Paragraph("<b>Client-Side State Hydration:</b> The process wherein React initializes local user tokens from browser storage (`localStorage`) upon application startup.", term_box))

    story.append(Paragraph("<b>C. Underlying Process:</b>", h2_style))
    story.append(Paragraph(
        "When a user opens `http://127.0.0.1:5000/`, React mounts `App.jsx`. The application queries `AuthContext.jsx` to verify if a valid, unexpired JSON Web Token exists in storage. "
        "If a valid token is found, the user is automatically transitioned to the SOC Dashboard; otherwise, the public Landing View is rendered. No sensitive telemetry or model weights are exposed prior to authentication.",
        body_style
    ))
    story.append(PageBreak())

    # ================= PAGE 4: SCREEN 2 - LOGIN PORTAL =================
    story.append(Paragraph("4. Screen 2: Zero-Trust Security Portal & Role-Based Authentication", h1_style))
    story.append(Paragraph(
        "The security portal authenticates users and establishes cryptographically verifiable identity claims prior to granting access to any network or model controls.",
        body_style
    ))
    img_s2 = os.path.join(FIG_DIR, "ui_2_login_portal.png")
    if os.path.exists(img_s2):
        story.append(RLImage(img_s2, width=440, height=185))
        story.append(Paragraph("Figure 4.1: Zero-Trust Security Portal and Role-Based Authentication Interface", fig_caption))

    story.append(Paragraph("<b>A. Visual Interface Breakdown:</b>", h2_style))
    story.append(Paragraph("• <b>Role Selection Selector:</b> Visual pills allowing quick credential pre-filling for test roles (`Admin`, `Analyst`, `User`).", bullet_style))
    story.append(Paragraph("• <b>Credential Input Fields:</b> Username and masked password inputs with client-side format validation.", bullet_style))
    story.append(Paragraph("• <b>Security Banner:</b> Re-asserts the Zero-Trust mandate: <i>'Never Trust, Always Verify. Continuous Authentication & Tamper-Evident Auditing.'</i>", bullet_style))

    story.append(Paragraph("<b>B. Theoretical & Technical Terms:</b>", h2_style))
    story.append(Paragraph("<b>Bcrypt Hashing (12 Salt Rounds):</b> A computationally expensive, adaptive key-derivation function that protects passwords against brute-force and rainbow-table attacks via blowfish block cipher hashing.", term_box))
    story.append(Paragraph("<b>JSON Web Token (JWT):</b> A compact, URL-safe standard (`RFC 7519`) representing claims transferred between client and server, cryptographically signed using HMAC-SHA256 (`HS256`).", term_box))
    story.append(Paragraph("<b>Bearer Token Scheme:</b> An HTTP authentication scheme where the client attaches the JWT inside the `Authorization: Bearer <token>` header on every subsequent API call.", term_box))

    story.append(Paragraph("<b>C. Underlying Process:</b>", h2_style))
    story.append(Paragraph(
        "1. The user enters credentials and clicks 'Sign In', transmitting a `POST` request to `/api/auth/login`.<br/>"
        "2. The Flask server queries the `users` table in `database.db` and validates the plaintext password against the stored salted hash using `bcrypt.check_password_hash()`.<br/>"
        "3. On success, the server creates an 8-hour JWT containing `user_id`, `username`, and `role` claims, signed with the server's private secret key. A `USER_LOGIN [SUCCESS]` record is appended to `audit_logs`.<br/>"
        "4. If invalid, access is rejected with `HTTP 401 Unauthorized`, and a `USER_LOGIN [FAILED]` security event is permanently recorded.",
        body_style
    ))
    story.append(PageBreak())

    # ================= PAGE 5: SCREEN 3 - ADMIN DASHBOARD =================
    story.append(Paragraph("5. Screen 3: Administrator SOC Overview & 8-Stage Pipeline Tracker", h1_style))
    story.append(Paragraph(
        "The Administrator Security Operations Center (SOC) Overview serves as the centralized mission control, providing high-level telemetry, active model status, and lifecycle stage tracking.",
        body_style
    ))
    img_s3 = os.path.join(FIG_DIR, "ui_3_admin_dashboard.png")
    if os.path.exists(img_s3):
        story.append(RLImage(img_s3, width=440, height=185))
        story.append(Paragraph("Figure 5.1: Administrator Security Operations Dashboard and 8-Stage Pipeline Tracker", fig_caption))

    story.append(Paragraph("<b>A. Visual Interface Breakdown:</b>", h2_style))
    story.append(Paragraph("• <b>Active Model Badge:</b> Displays the deployed model name (`Support Vector Machine (UNSW-NB15)`), version ID (`v_c01de4`), and training benchmark.", bullet_style))
    story.append(Paragraph("• <b>Telemetry Counter Cards:</b> 4 top-level KPI cards displaying Total Captured Flows (`1,384+`), Cataloged Datasets (`4`), Active Threat Deviations (`5`), and Audit Records (`1,316+`).", bullet_style))
    story.append(Paragraph("• <b>8-Stage Lifecycle Progress Trackers:</b> Step-by-step visual cards tracking Ingestion, Sampling, Normalization, Training, Evaluation, Registry, Sniffing, and Auditing.", bullet_style))
    story.append(Paragraph("• <b>System Health & Resource Gauges:</b> Real-time CPU, RAM, and Disk utilization meters querying host workstation hardware.", bullet_style))

    story.append(Paragraph("<b>B. Theoretical & Technical Terms:</b>", h2_style))
    story.append(Paragraph("<b>Security Operations Center (SOC):</b> A centralized facility and visual dashboard where enterprise information systems are monitored, assessed, and protected against intrusions.", term_box))
    story.append(Paragraph("<b>Telemetry:</b> Automated communication processes by which measurements and operational data are collected at remote or isolated points and transmitted to receiving equipment for monitoring.", term_box))
    story.append(Paragraph("<b>Pipeline State Machine:</b> A formal architectural construct tracking the deterministic progression of data from raw packets to evaluated model checkpoints.", term_box))

    story.append(Paragraph("<b>C. Underlying Process:</b>", h2_style))
    story.append(Paragraph(
        "Upon loading `OverviewView.jsx`, the frontend dispatches parallel asynchronous requests to `/api/system/status`, `/api/model/active`, `/api/live-detection/status`, and `/api/behavioral-analytics`. "
        "The Flask backend queries SQLite, computes aggregate statistics, checks system memory availability via `psutil`, and returns JSON payloads. The UI state updates reactively without blocking user interactions.",
        body_style
    ))
    story.append(PageBreak())

    # ================= PAGE 6: SCREEN 4 - DATASETS MANAGEMENT =================
    story.append(Paragraph("6. Screen 4: Datasets Inventory, Partitioning & Management (Stage 1)", h1_style))
    story.append(Paragraph(
        "The Datasets Inventory interface governs CSV ingestion, pre-ingestion validation, stratified subsampling, and target benchmark selection for model training.",
        body_style
    ))
    img_s4 = os.path.join(FIG_DIR, "ui_4_datasets_management.png")
    if os.path.exists(img_s4):
        story.append(RLImage(img_s4, width=440, height=185))
        story.append(Paragraph("Figure 6.1: Zero-Trust Datasets Inventory and Target Selection Interface", fig_caption))

    story.append(Paragraph("<b>A. Visual Interface Breakdown:</b>", h2_style))
    story.append(Paragraph("• <b>Cataloged Datasets Table:</b> Displays all uploaded benchmark CSVs, file sizes, total record counts, dimensionality, and upload timestamps.", bullet_style))
    story.append(Paragraph("• <b>Active Selection Indicator:</b> A green checkmark badge denoting the currently selected dataset (`unsw_nb15_raw.csv`).", bullet_style))
    story.append(Paragraph("• <b>RBAC Action Buttons:</b> 'Select Target' and 'Upload CSV' are available to both Admin and Analyst. The red 'Delete' trash can icon is strictly rendered for Administrators only.", bullet_style))

    story.append(Paragraph("<b>B. Theoretical & Technical Terms:</b>", h2_style))
    story.append(Paragraph("<b>Stratified Sampling:</b> Partitioning a dataset such that the exact proportion of benign and diverse attack categories is identically preserved in the subsample without synthesis.", term_box))
    story.append(Paragraph("<b>Data Leakage Prevention:</b> Guaranteeing that feature transformation statistics ($\mu_{train}, \sigma_{train}$) are computed strictly on training rows prior to any testing.", term_box))
    story.append(Paragraph("<b>Zero-Day Baseline Simulation:</b> Evaluating model generalization on unseen holdout splits that represent novel, unobserved network environments.", term_box))

    story.append(Paragraph("<b>C. Underlying Process & Partition Table:</b>", h2_style))
    story.append(Paragraph(
        "When an Admin selects a dataset, `POST /api/dataset/select` is triggered. The server updates `is_selected=1` in `dataset_history` and loads the data into `BaseNIDSPreprocessor`. "
        "The preprocessor drops session identifiers (`Flow ID`, `Source/Destination IP`, `Timestamp`), handles missing values via median imputation, and applies stratified 70/15/15 partitioning.",
        body_style
    ))

    # Small table
    t_ds_data = [
        [Paragraph("Dataset Filename", tbl_cell_hdr), Paragraph("Family", tbl_cell_hdr), Paragraph("Total Rows", tbl_cell_hdr), Paragraph("Sampled (N)", tbl_cell_hdr), Paragraph("Train (70%)", tbl_cell_hdr), Paragraph("Val (15%)", tbl_cell_hdr), Paragraph("Test (15%)", tbl_cell_hdr)],
        [Paragraph("unsw_nb15_raw.csv (Active)", tbl_cell_bold), Paragraph("UNSW-NB15", tbl_cell), Paragraph("2,540,044", tbl_cell), Paragraph("25,000", tbl_cell), Paragraph("17,500", tbl_cell), Paragraph("3,750", tbl_cell), Paragraph("3,750", tbl_cell)],
        [Paragraph("nsl_kdd_raw.csv", tbl_cell_bold), Paragraph("NSL-KDD", tbl_cell), Paragraph("148,517", tbl_cell), Paragraph("50,000", tbl_cell), Paragraph("35,000", tbl_cell), Paragraph("7,500", tbl_cell), Paragraph("7,500", tbl_cell)],
        [Paragraph("cicids2017_raw.csv", tbl_cell_bold), Paragraph("CIC-IDS2017", tbl_cell), Paragraph("2,830,743", tbl_cell), Paragraph("25,000", tbl_cell), Paragraph("17,500", tbl_cell), Paragraph("3,750", tbl_cell), Paragraph("3,750", tbl_cell)]
    ]
    t_ds = Table(t_ds_data, colWidths=[120, 55, 55, 55, 55, 55, 55])
    t_ds.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1E3A8A")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('TOPPADDING', (0,0), (-1,-1), 2), ('BOTTOMPADDING', (0,0), (-1,-1), 2)
    ]))
    story.append(t_ds)
    story.append(PageBreak())

    # ================= PAGE 7: SCREEN 5 - DATASET COMPARISON =================
    story.append(Paragraph("7. Screen 5: Multi-Dataset Structural Comparison Matrix", h1_style))
    story.append(Paragraph(
        "The comparison view allows security teams to contrast structural, dimensional, and class distribution differences across standard intrusion benchmarks.",
        body_style
    ))
    img_s5 = os.path.join(FIG_DIR, "ui_5_dataset_comparison.png")
    if os.path.exists(img_s5):
        story.append(RLImage(img_s5, width=440, height=185))
        story.append(Paragraph("Figure 7.1: Multi-Dataset Comparison Matrix Interface Contrasting NSL-KDD, CIC-IDS2017, and UNSW-NB15", fig_caption))

    story.append(Paragraph("<b>A. Visual Interface Breakdown:</b>", h2_style))
    story.append(Paragraph("• <b>Side-by-Side Comparison Cards:</b> Contrasts row volume, file size, target column name, feature counts, and clean hygiene status.", bullet_style))
    story.append(Paragraph("• <b>Class Distribution Visualizations:</b> Horizontal bar charts indicating class imbalance (e.g., 75.2% BENIGN in CIC-IDS2017 vs 58.8% Normal in UNSW-NB15).", bullet_style))
    story.append(Paragraph("• <b>Feature Schema Alignment Badges:</b> Highlights the live feature count mapped to each benchmark (15 live features for UNSW, 19 for NSL-KDD, 22 for CIC-IDS2017).", bullet_style))

    story.append(Paragraph("<b>B. Theoretical & Technical Terms:</b>", h2_style))
    story.append(Paragraph("<b>Class Imbalance Ratio:</b> The proportional disparity between majority benign flows and rare attack types, which can bias naive machine learning models toward false negatives.", term_box))
    story.append(Paragraph("<b>Schema Alignment:</b> The deterministic transformation mapping raw CSV headers to the canonical features extracted during real-time network packet sniffing.", term_box))
    story.append(Paragraph("<b>Nominal vs Continuous Network Attributes:</b> Differentiating discrete categorical values (`protocol_type`) from continuous numerical rates (`flow_bytes_per_sec`, `packet_iat_mean`).", term_box))

    story.append(Paragraph("<b>C. Underlying Process:</b>", h2_style))
    story.append(Paragraph(
        "Navigating to `/compare` triggers `GET /api/datasets/compare`. The Flask backend retrieves cataloged metadata from `dataset_history`, deserializes the `class_distribution_json` column, "
        "and computes relative class frequencies. Linking each benchmark directly to its live `FlowFeatureExtractor` schema ensures that switching datasets automatically adapts the feature extractor without code reconfiguration.",
        body_style
    ))
    story.append(PageBreak())

    # ================= PAGE 8: SCREEN 6 - MODEL TRAINING CONSOLE =================
    story.append(Paragraph("8. Screen 6: AI Model Training Console & Convergence Telemetry (Stage 2)", h1_style))
    story.append(Paragraph(
        "The Model Training Console provides an interactive interface for configuring and executing machine learning training runs across multiple algorithmic families.",
        body_style
    ))
    img_s6 = os.path.join(FIG_DIR, "ui_6_model_training.png")
    if os.path.exists(img_s6):
        story.append(RLImage(img_s6, width=440, height=185))
        story.append(Paragraph("Figure 8.1: AI Model Training Console Configuring Stratified Sample Size, Seed, and Hyperparameters", fig_caption))

    story.append(Paragraph("<b>A. Visual Interface Breakdown:</b>", h2_style))
    story.append(Paragraph("• <b>Algorithm Architecture Selector:</b> Dropdown enabling selection between Support Vector Machines (SVM RBF), Random Forest, Logistic Regression, and Deep MLP.", bullet_style))
    story.append(Paragraph("• <b>Hyperparameter Controls:</b> Input sliders and fields for Sample Size ($N=25,000$), Random Seed (`42`), Epochs (`10`), Batch Size (`32`), and Learning Rate (`0.001`).", bullet_style))
    story.append(Paragraph("• <b>Live Training Progress Bar:</b> Dynamic progress indicator showing active epoch progress, loss values, and real-time training accuracy updates.", bullet_style))
    story.append(Paragraph("• <b>Analyst Read-Only Banner:</b> For non-Admin users, training controls are disabled and replaced by the read-only live training HUD.", bullet_style))

    story.append(Paragraph("<b>B. Theoretical & Technical Terms:</b>", h2_style))
    story.append(Paragraph("<b>Support Vector Classifier (RBF Kernel):</b> A non-linear kernel method projecting input features into infinite-dimensional Hilbert space via $K(x, x') = \exp(-\gamma \|x - x'\|^2)$ to separate overlapping classes.", term_box))
    story.append(Paragraph("<b>Cross-Entropy Loss:</b> The objective function measuring prediction error during training: $\mathcal{L} = -\sum y_i \log(\hat{y}_i)$.", term_box))
    story.append(Paragraph("<b>Adam Optimizer:</b> An adaptive learning rate optimization algorithm combining momentum with Root Mean Square Propagation (RMSProp).", term_box))

    story.append(Paragraph("<b>C. Underlying Process:</b>", h2_style))
    story.append(Paragraph(
        "When an Admin clicks 'Start Training', `POST /api/model/train` is invoked. The server spawns a background thread running `NIDSTrainer.train()`. "
        "The trainer fits `StandardScaler` strictly on the training partition ($17,500$ rows), initiates model fitting, evaluates validation performance at each epoch, and writes training telemetry to memory. "
        "Once complete, the model checkpoint is serialized to disk (`model.joblib`), indexed in SQLite `model_history`, and marked as ready for evaluation.",
        body_style
    ))
    story.append(PageBreak())

    # ================= PAGE 9: TRAINING CURVES & MATHEMATICAL PROOF =================
    story.append(Paragraph("9. Empirical Training Curves & Mathematical Weight Stabilization", h1_style))
    story.append(Paragraph(
        "To verify algorithmic convergence and eliminate overfitting, optimization telemetry was tracked across 10 complete epochs.",
        body_style
    ))
    img_curves = os.path.join(FIG_DIR, "fig4_1_training_curves.png")
    if os.path.exists(img_curves):
        story.append(RLImage(img_curves, width=460, height=155))
        story.append(Paragraph("Figure 9.1: Verified 10-Epoch Learning Curves (Loss, Accuracy, and Frobenius Weight Update Norm) Across Datasets", fig_caption))

    story.append(Paragraph("<b>Mathematical Proof of Convergence:</b>", h2_style))
    story.append(Paragraph(
        "Model convergence was verified using the <b>Frobenius Weight Update Norm</b> ($\|\Delta W^{(e)}\|_F$), defined as the Euclidean magnitude of weight matrix modifications between successive epochs: "
        "$$\|\Delta W^{(e)}\|_F = \sqrt{\sum_{i,j} (W_{ij}^{(e)} - W_{ij}^{(e-1)})^2}$$ "
        "In Epoch 1, the optimizer makes large coarse updates ($\|\Delta W^{(1)}\|_F = 13.4667$). By Epoch 2, the update norm sharply contracts to $0.9260$ and stabilizes below $0.80$ by Epoch 10, confirming mathematical convergence.",
        body_style
    ))

    t_conv_data = [
        [Paragraph("Epoch", tbl_cell_hdr), Paragraph("Training Loss", tbl_cell_hdr), Paragraph("Training Acc (%)", tbl_cell_hdr), Paragraph("Validation Loss", tbl_cell_hdr), Paragraph("Validation Acc (%)", tbl_cell_hdr), Paragraph("Frobenius Norm (||ΔW||_F)", tbl_cell_hdr)],
        [Paragraph("1", tbl_cell), Paragraph("0.1373", tbl_cell), Paragraph("96.97%", tbl_cell), Paragraph("0.1637", tbl_cell), Paragraph("96.24%", tbl_cell), Paragraph("13.4667 (Initial Step)", tbl_cell)],
        [Paragraph("2", tbl_cell), Paragraph("0.1363", tbl_cell), Paragraph("96.97%", tbl_cell), Paragraph("0.1649", tbl_cell), Paragraph("96.24%", tbl_cell), Paragraph("0.9260", tbl_cell)],
        [Paragraph("4", tbl_cell), Paragraph("0.1356", tbl_cell), Paragraph("96.97%", tbl_cell), Paragraph("0.1614", tbl_cell), Paragraph("96.24%", tbl_cell), Paragraph("0.7239", tbl_cell)],
        [Paragraph("6", tbl_cell), Paragraph("0.1338", tbl_cell), Paragraph("96.97%", tbl_cell), Paragraph("0.1635", tbl_cell), Paragraph("96.24%", tbl_cell), Paragraph("0.7383", tbl_cell)],
        [Paragraph("8", tbl_cell), Paragraph("0.1358", tbl_cell), Paragraph("96.97%", tbl_cell), Paragraph("0.1682", tbl_cell), Paragraph("96.24%", tbl_cell), Paragraph("0.7277", tbl_cell)],
        [Paragraph("10", tbl_cell_bold), Paragraph("0.1326", tbl_cell_bold), Paragraph("96.97%", tbl_cell_bold), Paragraph("0.1633", tbl_cell_bold), Paragraph("96.24%", tbl_cell_bold), Paragraph("0.7955 (Converged)", tbl_cell_bold)]
    ]
    t_conv = Table(t_conv_data, colWidths=[40, 75, 75, 75, 75, 120])
    t_conv.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1E3A8A")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('TOPPADDING', (0,0), (-1,-1), 2), ('BOTTOMPADDING', (0,0), (-1,-1), 2)
    ]))
    story.append(t_conv)
    story.append(PageBreak())

    # ================= PAGE 10: SCREEN 7 - PERFORMANCE EVALUATION =================
    story.append(Paragraph("10. Screen 7: Model Performance Evaluation & Holdout Analytics (Stage 3)", h1_style))
    story.append(Paragraph(
        "The Performance Evaluation dashboard renders comprehensive holdout test analytics on unseen partitions ($N_{test}=3,750$ for UNSW-NB15), ensuring rigorous assessment without optimistic bias.",
        body_style
    ))
    img_s7 = os.path.join(FIG_DIR, "ui_7_performance_evaluation.png")
    if os.path.exists(img_s7):
        story.append(RLImage(img_s7, width=440, height=185))
        story.append(Paragraph("Figure 10.1: AI Model Performance Evaluation Dashboard Displaying Confusion Matrix and Metric Cards", fig_caption))

    story.append(Paragraph("<b>A. Visual Interface Breakdown:</b>", h2_style))
    story.append(Paragraph("• <b>Top-Level Metric Cards:</b> 6 KPI cards displaying Accuracy (`96.00%`), Precision (`96.01%`), Recall (`96.00%`), F1-Score (`96.00%`), False Positive Rate (`2.22%`), and ROC-AUC (`0.9853`).", bullet_style))
    story.append(Paragraph("• <b>Interactive Confusion Matrix Heatmap:</b> Displays cell counts for $TP, TN, FP, FN$ with intensity shading.", bullet_style))
    story.append(Paragraph("• <b>Classification Report Table:</b> Displays class-wise Precision, Recall, and F1-Scores across all 7 traffic categories.", bullet_style))
    story.append(Paragraph("• <b>ROC Curve Plotter:</b> Interactive visualization plotting True Positive Rate ($TPR$) vs False Positive Rate ($FPR$) across classification thresholds.", bullet_style))

    story.append(Paragraph("<b>B. Theoretical & Technical Terms:</b>", h2_style))
    story.append(Paragraph("<b>False Positive Rate (FPR):</b> $FP / (FP + TN)$. The probability of raising false alarms on normal traffic. Kept at 2.22% to eliminate SOC alert fatigue.", term_box))
    story.append(Paragraph("<b>Recall / Attack Detection Rate (ADR):</b> $TP / (TP + FN)$. The proportion of actual cyberattacks successfully detected (96.69% on attack flows).", term_box))
    story.append(Paragraph("<b>ROC-AUC (Area Under ROC Curve):</b> A threshold-independent metric measuring class separability ($0.9853$ indicates exceptional discriminatory power).", term_box))

    story.append(Paragraph("<b>C. Underlying Process:</b>", h2_style))
    story.append(Paragraph(
        "The dashboard calls `GET /api/model/evaluation/<id>`. The backend loads the serialized model and transforms the unseen holdout test split ($X_{test}$) using the frozen scaler parameters ($\mu_{train}, \sigma_{train}$). "
        "Scikit-learn computes `confusion_matrix()`, `precision_recall_fscore_support()`, and `roc_curve()`, serializing metrics to `latest_report.json` and returning the JSON payload to the UI.",
        body_style
    ))
    story.append(PageBreak())

    # ================= PAGE 11: CONFUSION MATRICES & BENCHMARKS =================
    story.append(Paragraph("11. Confusion Matrix Analysis & Comparative Benchmarking", h1_style))
    story.append(Paragraph(
        "Evaluating classification matrices reveals the granular distribution of correct classifications and misclassifications across binary and multi-class boundaries.",
        body_style
    ))
    img_cm = os.path.join(FIG_DIR, "fig4_2_unsw_binary_cm_roc.png")
    if os.path.exists(img_cm):
        story.append(RLImage(img_cm, width=460, height=155))
        story.append(Paragraph("Figure 11.1: Verified Holdout Confusion Matrix and ROC Curve (AUC = 0.9853) for UNSW-NB15 Classification", fig_caption))

    story.append(Paragraph("<b>Binary & Multi-Class Confusion Matrix Breakdown:</b>", h2_style))
    story.append(Paragraph(
        "On the 3,750 unseen UNSW-NB15 holdout test flows, the active Support Vector Machine correctly identified <b>2,158 Normal flows ($TN$)</b> and <b>1,492 Attack flows ($TP$)</b>, "
        "with only <b>49 False Alarms ($FP$, FPR = 2.22%)</b> and <b>51 Missed Attacks ($FN$, FNR = 3.31%)</b>.",
        body_style
    ))

    # Multi-class table
    t_mc_data = [
        [Paragraph("Traffic Category", tbl_cell_hdr), Paragraph("Precision", tbl_cell_hdr), Paragraph("Recall (ADR)", tbl_cell_hdr), Paragraph("F1-Score", tbl_cell_hdr), Paragraph("Test Support (Rows)", tbl_cell_hdr), Paragraph("Detection Analysis", tbl_cell_hdr)],
        [Paragraph("Normal (Baseline)", tbl_cell_bold), Paragraph("97.69%", tbl_cell), Paragraph("97.78%", tbl_cell), Paragraph("97.74%", tbl_cell), Paragraph("2,207", tbl_cell), Paragraph("Near-zero false alarms on benign flows", tbl_cell)],
        [Paragraph("Generic", tbl_cell_bold), Paragraph("94.44%", tbl_cell), Paragraph("94.44%", tbl_cell), Paragraph("94.44%", tbl_cell), Paragraph("611", tbl_cell), Paragraph("Strong detection of common exploit scripts", tbl_cell)],
        [Paragraph("Exploits", tbl_cell_bold), Paragraph("91.30%", tbl_cell), Paragraph("94.20%", tbl_cell), Paragraph("92.73%", tbl_cell), Paragraph("379", tbl_cell), Paragraph("High recall on vulnerability attacks", tbl_cell)],
        [Paragraph("Fuzzers", tbl_cell_bold), Paragraph("94.54%", tbl_cell), Paragraph("93.75%", tbl_cell), Paragraph("94.14%", tbl_cell), Paragraph("240", tbl_cell), Paragraph("Accurate capture of malformed payloads", tbl_cell)],
        [Paragraph("Denial of Service (DoS)", tbl_cell_bold), Paragraph("94.52%", tbl_cell), Paragraph("91.39%", tbl_cell), Paragraph("92.93%", tbl_cell), Paragraph("151", tbl_cell), Paragraph("Rapid identification of volumetric floods", tbl_cell)],
        [Paragraph("Reconnaissance", tbl_cell_bold), Paragraph("94.81%", tbl_cell), Paragraph("91.25%", tbl_cell), Paragraph("92.99%", tbl_cell), Paragraph("80", tbl_cell), Paragraph("Flags port sweeps and network scans", tbl_cell)],
        [Paragraph("Analysis", tbl_cell_bold), Paragraph("92.31%", tbl_cell), Paragraph("87.80%", tbl_cell), Paragraph("90.00%", tbl_cell), Paragraph("82", tbl_cell), Paragraph("Catches web scanning and HTML intrusions", tbl_cell)],
        [Paragraph("Weighted Average", tbl_cell_bold), Paragraph("96.01%", tbl_cell_bold), Paragraph("96.00%", tbl_cell_bold), Paragraph("96.00%", tbl_cell_bold), Paragraph("3,750", tbl_cell_bold), Paragraph("Overall FPR = 2.22% | ROC-AUC = 0.9853", tbl_cell_bold)]
    ]
    t_mc = Table(t_mc_data, colWidths=[90, 50, 60, 50, 65, 145])
    t_mc.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1E3A8A")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('TOPPADDING', (0,0), (-1,-1), 2), ('BOTTOMPADDING', (0,0), (-1,-1), 2)
    ]))
    story.append(t_mc)
    story.append(PageBreak())

    # ================= PAGE 12: SCREEN 8 - LIVE DETECTION CONSOLE =================
    story.append(Paragraph("12. Screen 8: Real-Time Live Network Detection Console (Stage 5)", h1_style))
    story.append(Paragraph(
        "The live detection module inspects incoming network traffic passively on the host machine, performing real-time flow aggregation, feature extraction, and AI risk scoring.",
        body_style
    ))
    img_s8 = os.path.join(FIG_DIR, "ui_8_live_detection.png")
    if os.path.exists(img_s8):
        story.append(RLImage(img_s8, width=440, height=185))
        story.append(Paragraph("Figure 12.1: Real-Time Live Network Detection Console with Interface Sniffer Controls and Threat Stream", fig_caption))

    story.append(Paragraph("<b>A. Visual Interface Breakdown:</b>", h2_style))
    story.append(Paragraph("• <b>Network Interface Discovery:</b> Dropdown enumerating available network adapters (e.g., `Wi-Fi` Realtek RTL8821CE `172.20.10.8`).", bullet_style))
    story.append(Paragraph("• <b>Capture Controls:</b> 'Start Live Monitoring', 'Stop Monitoring', and 'Replay Test Flow' buttons.", bullet_style))
    story.append(Paragraph("• <b>Streaming Flow Telemetry Feed:</b> Live scrolling table displaying Timestamp, 5-Tuple endpoints, Protocol (`TCP`/`UDP`), Flow Duration, Packet/Byte counts, AI Prediction, Confidence, and Risk Badges.", bullet_style))
    story.append(Paragraph("• <b>Piecewise Risk Scoring Badges:</b> Green (`LOW` Risk, $<60\%$), Amber (`MEDIUM` Risk, $60\%\text{--}85\%$), and Red (`HIGH` Risk, $\ge 85\%$).", bullet_style))

    story.append(Paragraph("<b>B. Theoretical & Technical Terms:</b>", h2_style))
    story.append(Paragraph("<b>Passive Packet Sniffing:</b> Capturing network frames from an adapter without transmitting probe packets or alerting potential adversaries.", term_box))
    story.append(Paragraph("<b>5-Tuple Bidirectional Flow Aggregation:</b> Tracking connection state using canonical keys: $(\min(\text{IP}_s, \text{IP}_d), \max(\text{IP}_s, \text{IP}_d), \min(P_s, P_d), \max(P_s, P_d), \text{Proto})$.", term_box))
    story.append(Paragraph("<b>Inference Latency:</b> Processing time required to classify a single network flow ($0.0512\text{ ms/flow}$, enabling ~19,531 flows/second line-rate throughput).", term_box))

    story.append(Paragraph("<b>C. Underlying Process:</b>", h2_style))
    story.append(Paragraph(
        "1. Clicking 'Start Live Monitoring' invokes `POST /api/live-detection/start`. The server launches `PacketCaptureManager` in a daemon thread via Scapy `sniff()`.<br/>"
        "2. Packets are dispatched to `FlowManager`, which computes forward/backward rates, inter-arrival times (IAT), and TCP flags.<br/>"
        "3. On flow expiration (inactivity timeout or `FIN`/`RST`), `feature_extractor.py` extracts 15 schema attributes.<br/>"
        "4. `live_predictor.py` normalizes features using training parameters ($\mu_{train}, \sigma_{train}$) and calls `model.predict_proba()`.<br/>"
        "5. The flow is persisted to SQLite `live_detections` and polled every 2s via `/api/live-detection/traffic`.",
        body_style
    ))
    story.append(PageBreak())

    # ================= PAGE 13: SCREEN 9 - BEHAVIORAL ANALYTICS =================
    story.append(Paragraph("13. Screen 9: Behavioral Analytics & Identity Threat Profiling (Stage 6)", h1_style))
    story.append(Paragraph(
        "The Behavioral Analytics view implements User and Entity Behavior Analytics (UEBA), correlating authentication events with live endpoint traffic to detect compromised credentials.",
        body_style
    ))
    img_s9 = os.path.join(FIG_DIR, "ui_9_audit_logs.png")
    if os.path.exists(img_s9):
        story.append(RLImage(img_s9, width=440, height=185))
        story.append(Paragraph("Figure 13.1: Zero-Trust Behavioral Analytics and Identity Threat Profiling Console", fig_caption))

    story.append(Paragraph("<b>A. Visual Interface Breakdown:</b>", h2_style))
    story.append(Paragraph("• <b>Temporal Access Heatmap:</b> Visual distribution of user logins across 24 hours (59% morning 06:00–12:00 UTC, 40% afternoon, 1% off-hours).", bullet_style))
    story.append(Paragraph("• <b>Monitored Endpoint Cards:</b> Summarizes activity across 13 network devices, highlighting unusual transmission volumes.", bullet_style))
    story.append(Paragraph("• <b>Behavioral Deviation Feed:</b> Alerts flagging unusual user activity (e.g., unexpected off-hours access, rapid endpoint switching).", bullet_style))

    story.append(Paragraph("<b>B. Theoretical & Technical Terms:</b>", h2_style))
    story.append(Paragraph("<b>User and Entity Behavior Analytics (UEBA):</b> A cybersecurity methodology that tracks normal behavioral baselines for users and devices, detecting anomalies indicative of insider threats or stolen credentials.", term_box))
    story.append(Paragraph("<b>Baseline Anomaly Thresholding:</b> Comparing active operational metrics against established statistical intervals ($\mu \pm 2\sigma$).", term_box))
    story.append(Paragraph("<b>Non-Repudiation:</b> Assurance that an entity cannot deny the authenticity of their signature or action within an audit log.", term_box))

    story.append(Paragraph("<b>C. Underlying Process:</b>", h2_style))
    story.append(Paragraph(
        "Accessing `/behavioral-analytics` calls `GET /api/behavioral-analytics`. The Flask backend aggregates 1,316+ historical events from `audit_logs` and combines them with `live_detections`. "
        "The heuristic engine profiles 3 user principals (`admin`, `analyst`, `testuser`) across active IP addresses, computing anomaly scores based on login hours, failed credential bursts, and unusual privilege access.",
        body_style
    ))
    story.append(PageBreak())

    # ================= PAGE 14: SCREEN 10 - AUDIT TRAIL TABLE =================
    story.append(Paragraph("14. Screen 10: Forensic Audit Trail & Privilege Enforcement (Stage 6)", h1_style))
    story.append(Paragraph(
        "The Forensic Audit Trail maintains a permanent, tamper-evident record of all security-relevant transactions, providing empirical proof of Zero-Trust access control.",
        body_style
    ))
    img_s10 = os.path.join(FIG_DIR, "ui_10_audit_trail_table.png")
    if os.path.exists(img_s10):
        story.append(RLImage(img_s10, width=440, height=185))
        story.append(Paragraph("Figure 14.1: Zero-Trust Forensic Audit Trail Table Displaying Cryptographic Event Records", fig_caption))

    story.append(Paragraph("<b>A. Visual Interface Breakdown:</b>", h2_style))
    story.append(Paragraph("• <b>Filterable Audit Table:</b> Displays Event ID, Timestamp, Username, Action Code, IP Address, Status (`SUCCESS`, `BLOCKED`, `REJECTED`), and Details.", bullet_style))
    story.append(Paragraph("• <b>Severity-Coded Badges:</b> Green for verified authentications; Amber for session expirations; Red for blocked privilege escalation attempts.", bullet_style))
    story.append(Paragraph("• <b>CSV Export Utility:</b> Allows compliance auditors to download raw forensic event logs for compliance reporting.", bullet_style))

    story.append(Paragraph("<b>B. Theoretical & Technical Terms:</b>", h2_style))
    story.append(Paragraph("<b>Tamper-Evident Audit Trail:</b> An append-only persistence schema where log records cannot be altered or deleted by application users.", term_box))
    story.append(Paragraph("<b>Privilege Escalation Defense:</b> Intercepting attempts by unprivileged users to execute administrative routes (`@require_role(['Admin'])`).", term_box))
    story.append(Paragraph("<b>Stateless Session Invalidation:</b> Automatically rejecting expired JWT tokens without maintaining complex server-side session tables.", term_box))

    story.append(Paragraph("<b>C. Underlying Process & Empirical Database Evidence:</b>", h2_style))
    story.append(Paragraph(
        "Every API route in the application wraps execution inside `log_audit_event()`. Empirical queries on `database.db` reveal <b>1,316 total audit entries</b>:",
        body_style
    ))

    t_aud_data = [
        [Paragraph("Audit Action Category", tbl_cell_hdr), Paragraph("Count", tbl_cell_hdr), Paragraph("Security Status", tbl_cell_hdr), Paragraph("Verification Meaning", tbl_cell_hdr)],
        [Paragraph("EXPIRED_OR_INVALID_TOKEN", tbl_cell_bold), Paragraph("522", tbl_cell), Paragraph("BLOCKED (HTTP 401)", tbl_cell), Paragraph("Stateless Zero-Trust token expiry enforced", tbl_cell)],
        [Paragraph("USER_LOGIN [FAILED]", tbl_cell_bold), Paragraph("113", tbl_cell), Paragraph("BLOCKED (HTTP 401)", tbl_cell), Paragraph("Brute-force and bad-credential attempts intercepted", tbl_cell)],
        [Paragraph("MODEL_TRAINING_START", tbl_cell_bold), Paragraph("105", tbl_cell), Paragraph("AUDITED (Admin Only)", tbl_cell), Paragraph("Training runs tracked with seed and row counts", tbl_cell)],
        [Paragraph("USER_LOGIN [SUCCESS]", tbl_cell_bold), Paragraph("72", tbl_cell), Paragraph("SUCCESS (HTTP 200)", tbl_cell), Paragraph("Admin, Analyst, and User logins verified via Bcrypt", tbl_cell)],
        [Paragraph("LIVE_CAPTURE_START / STOP", tbl_cell_bold), Paragraph("124", tbl_cell), Paragraph("SUCCESS", tbl_cell), Paragraph("Packet monitoring sessions initiated and tracked", tbl_cell)],
        [Paragraph("LIVE_REPLAY_TEST", tbl_cell_bold), Paragraph("63", tbl_cell), Paragraph("SUCCESS", tbl_cell), Paragraph("Controlled flow simulations executed by operators", tbl_cell)],
        [Paragraph("RBAC_ACCESS_DENIED", tbl_cell_bold), Paragraph("28", tbl_cell), Paragraph("REJECTED (HTTP 403)", tbl_cell), Paragraph("Non-Admin privilege escalation attempts strictly blocked", tbl_cell)],
        [Paragraph("DATASET_SELECT / UPLOAD", tbl_cell_bold), Paragraph("34", tbl_cell), Paragraph("SUCCESS", tbl_cell), Paragraph("Benchmark switches recorded in forensic log", tbl_cell)]
    ]
    t_aud = Table(t_aud_data, colWidths=[140, 50, 105, 155])
    t_aud.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1E3A8A")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('TOPPADDING', (0,0), (-1,-1), 2), ('BOTTOMPADDING', (0,0), (-1,-1), 2)
    ]))
    story.append(t_aud)
    story.append(PageBreak())

    # ================= PAGE 15: MASTER SCORECARD & VIVA DEFENSE GUIDE =================
    story.append(Paragraph("15. Master Project Scorecard & Faculty Viva Defense Guide", h1_style))
    story.append(Paragraph(
        "This concluding section synthesizes the project accomplishments and arms the candidate with defensible answers to anticipated questions during technical viva evaluations.",
        body_style
    ))

    story.append(Paragraph("<b>Master System Scorecard:</b>", h2_style))
    story.append(Paragraph("• <b>Benchmark Ingestion:</b> 5.66M+ records cataloged across UNSW-NB15, NSL-KDD, and CIC-IDS2017 with zero train-test data leakage.", bullet_style))
    story.append(Paragraph("• <b>Champion Classifier:</b> Support Vector Machine (RBF Kernel) on UNSW-NB15 achieved <b>96.00% Accuracy</b>, <b>96.01% Precision</b>, <b>96.00% Recall</b>, a low <b>2.22% False Positive Rate</b>, and <b>0.9853 ROC-AUC</b>.", bullet_style))
    story.append(Paragraph("• <b>Ensemble Classifier:</b> Random Forest achieved <b>97.42% Accuracy</b> on UNSW-NB15 and <b>99.00% Accuracy</b> on NSL-KDD.", bullet_style))
    story.append(Paragraph("• <b>Live Detection Speed:</b> Per-flow inference latency of <b>0.0512 ms/flow</b> (~19,531 flows/second line-rate capacity) across 1,384+ live Wi-Fi flows.", bullet_style))
    story.append(Paragraph("• <b>Zero-Trust RBAC:</b> Complete separation of duties between Admin and Analyst; 28 unauthorized privilege escalation attempts intercepted with HTTP 403 Forbidden and logged across 1,316 audit entries.", bullet_style))

    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>Defensible Responses to Critical Viva Review Questions:</b>", h2_style))
    story.append(Paragraph(
        "<b>1. Why choose an RBF Kernel SVM over simpler Linear Regression or Decision Trees?</b><br/>"
        "<i>Answer:</i> Network intrusion features exhibit highly non-linear, multi-dimensional correlations (e.g., relationship between flow duration, packet rates, and TCP window sizes). "
        "Linear models achieved only 89.45% accuracy with an unacceptable 5.12% false alarm rate. The RBF Gaussian kernel projects features into infinite-dimensional Hilbert space, "
        "establishing optimal non-linear separation boundaries that achieve 96.00% accuracy and 0.9853 ROC-AUC.",
        body_style
    ))
    story.append(Paragraph(
        "<b>2. Why is keeping False Positive Rate (FPR) below 2.5% more critical than raw Accuracy in production?</b><br/>"
        "<i>Answer:</i> In high-throughput corporate networks evaluating 100,000 flows per hour, a 10% FPR generates 10,000 false alarms every hour, causing severe alert fatigue and blinding analysts to real intrusions. "
        "By restricting FPR to <b>2.22%</b>, our model ensures that alerts represent actionable, statistically validated threats.",
        body_style
    ))
    story.append(Paragraph(
        "<b>3. How does Zero Trust specifically protect the AI pipeline?</b><br/>"
        "<i>Answer:</i> Under Zero Trust, no user or component inside the network is implicitly trusted. Our system enforces Separation of Duties: "
        "Security Analysts can monitor live traffic feeds and view audit logs but are cryptographically blocked by `@require_role(['Admin'])` from retraining models, altering weights, or deleting forensic datasets. "
        "Every unauthorized attempt is rejected with HTTP 403 and committed to an immutable audit trail.",
        body_style
    ))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"SUCCESS: Generated PDF at {PDF_PATH}")

def build_docx():
    doc = docx.Document()

    for section in doc.sections:
        section.top_margin = Inches(0.7)
        section.bottom_margin = Inches(0.7)
        section.left_margin = Inches(0.7)
        section.right_margin = Inches(0.7)

    def add_h1(text):
        h = doc.add_heading(level=1)
        r = h.add_run(text)
        r.font.name = "Arial"
        r.font.size = Pt(14)
        r.font.color.rgb = RGBColor(30, 58, 138)
        r.bold = True

    def add_h2(text):
        h = doc.add_heading(level=2)
        r = h.add_run(text)
        r.font.name = "Arial"
        r.font.size = Pt(11)
        r.font.color.rgb = RGBColor(15, 23, 42)
        r.bold = True

    def add_p(text):
        p = doc.add_paragraph()
        r = p.add_run(text)
        r.font.name = "Times New Roman"
        r.font.size = Pt(10)
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    def add_bullet(text):
        p = doc.add_paragraph(style='List Bullet')
        r = p.add_run(text)
        r.font.name = "Times New Roman"
        r.font.size = Pt(9.5)
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    def add_img(img_name, caption):
        img_p = os.path.join(FIG_DIR, img_name)
        if os.path.exists(img_p):
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            doc.add_picture(img_p, width=Inches(6.0))
            p_cap = doc.add_paragraph()
            r_cap = p_cap.add_run(caption)
            r_cap.font.name = "Arial"
            r_cap.font.size = Pt(8.5)
            r_cap.bold = True
            r_cap.font.color.rgb = RGBColor(51, 65, 85)
            p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # Title
    p_title = doc.add_paragraph()
    r_title = p_title.add_run("ZERO-TRUST AI-POWERED NETWORK INTRUSION DETECTION SYSTEM\n")
    r_title.bold = True
    r_title.font.name = "Arial"
    r_title.font.size = Pt(18)
    r_title.font.color.rgb = RGBColor(15, 23, 42)
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER

    r_sub = p_title.add_run("Operational Dashboard Guide, Sequential Execution Analysis & Technical Telemetry\n")
    r_sub.font.name = "Arial"
    r_sub.font.size = Pt(11)
    r_sub.font.color.rgb = RGBColor(30, 58, 138)

    r_meta = p_title.add_run("Author: Lohith Gopi (Batch 34) | Institution: JNNCE, Shivamogga | Dept: Information Science & Engineering")
    r_meta.font.name = "Arial"
    r_meta.font.size = Pt(9)
    r_meta.font.color.rgb = RGBColor(100, 116, 139)

    doc.add_paragraph("―" * 60)

    # Content
    add_h1("1. Executive Summary & Sequential Execution Framework")
    add_p(
        "This technical document provides an exhaustive, visual, and operational analysis of the Zero-Trust AI-Powered Network Intrusion Detection System (Zero-Trust NIDS). "
        "The platform bridges machine learning classification with a live, modern Security Operations Center (SOC) dashboard. "
        "Unlike monolithic academic scripts, this system enforces the Zero-Trust security paradigm—'Never Trust, Always Verify'—across all interactive web views and background pipelines."
    )
    add_bullet("Stage 0: Portal Entry & Authentication: SPA initialization, identity assertion, 12-round Bcrypt hash verification, and stateless HS256 JWT issuance.")
    add_bullet("Stage 1: Ingestion & Dataset Preparation: Benchmark dataset cataloging, stratified sampling, deduplication, and zero-leakage feature scaling.")
    add_bullet("Stage 2: Offline Model Training & Convergence: Asynchronous multi-algorithm optimization, loss tracking, and weight update Frobenius norm evaluation.")
    add_bullet("Stage 3: Holdout Performance Evaluation: Testing on unseen 15% partitions, computing Confusion Matrices, ROC-AUC curves, and multi-class precision/recall.")
    add_bullet("Stage 4: Model Checkpointing & Hot-Swapping: Serializing optimal weights into .joblib checkpoints and binding the model to the live inference engine.")
    add_bullet("Stage 5: Live Network Sniffing & Real-Time Classification: Capturing live packets via Scapy, assembling bidirectional 5-tuple flows, and assigning threat risk tiers.")
    add_bullet("Stage 6: Zero-Trust Governance & Forensic Auditing: Enforcing RBAC (Admin vs Analyst), intercepting privilege escalation, and recording audit logs.")

    doc.add_page_break()

    # Master Arch
    add_h1("2. Master Architectural Workflow & Role Separation")
    add_p("The system follows a multi-tier decoupled architecture: a React 18 SPA frontend communicates via authenticated REST APIs with a Python Flask backend.")
    add_img("fig3_1_master_architecture.png", "Figure 2.1: Master Architecture Diagram Illustrating End-to-End Data, Control, and Model Flows")
    add_h2("Zero-Trust Role Separation (Admin vs Analyst):")
    add_bullet("Administrator (Admin): Full system authority. Can initiate asynchronous model training runs, activate/hot-swap active detection models, delete existing model checkpoints, and delete cataloged datasets.")
    add_bullet("Security Analyst (Analyst): Restricted monitoring authority. Can view datasets, inspect comparison matrices, initiate live packet sniffing, monitor live threat alerts, evaluate model performance, and examine audit logs.")
    add_bullet("Analyst Live Training HUD: When an Admin triggers background training, logged-in Analysts receive a prominent read-only telemetry banner ('⚡ LIVE ADMIN TRAINING') displaying live epoch progress, loss, and accuracy.")

    doc.add_page_break()

    # Screen 1
    add_h1("3. Screen 1: Academic Landing Page & Public SOC Portal Entry")
    add_p("The landing page serves as the public-facing entry point, establishing institutional attributions, project context, and the identity boundary for Zero-Trust access.")
    add_img("ui_1_landing_page.png", "Figure 3.1: Academic Landing Page of the Proposed Zero-Trust AI-Powered NIDS")
    add_h2("Visual Interface Breakdown:")
    add_bullet("Hero Header & Branding: Identifies the project under the Department of Information Science & Engineering, JNNCE Shivamogga, Batch No. 34.")
    add_bullet("System Status Indicator: Displays real-time operational status (Active Model Version, Database Connection State, Passive Sniffer Readiness).")
    add_bullet("Access Control CTA: 'Launch Security Portal' button directing the user to the Zero-Trust authentication gateway.")
    add_h2("Theoretical & Technical Terms:")
    add_p("• Single-Page Application (SPA): A web architecture that loads a single HTML page and dynamically updates content without full browser reloads.")
    add_p("• Identity Boundary: Demarcation separating unauthenticated public traffic from protected internal system endpoints.")
    add_p("• Client-Side State Hydration: React initializing local user tokens from browser storage upon application startup.")
    add_h2("Underlying Process:")
    add_p("When a user opens the landing page, React mounts App.jsx and verifies if an unexpired JWT token exists in AuthContext.jsx. If found, the user transitions to the SOC Dashboard; otherwise, the public Landing View renders.")

    doc.add_page_break()

    # Screen 2
    add_h1("4. Screen 2: Zero-Trust Security Portal & Role-Based Authentication")
    add_p("The security portal authenticates users and establishes cryptographically verifiable identity claims prior to granting access to any network or model controls.")
    add_img("ui_2_login_portal.png", "Figure 4.1: Zero-Trust Security Portal and Role-Based Authentication Interface")
    add_h2("Visual Interface Breakdown:")
    add_bullet("Role Selector: Visual pills allowing quick credential pre-filling for test roles (Admin, Analyst, User).")
    add_bullet("Credential Input Fields: Username and masked password inputs with client-side format validation.")
    add_bullet("Security Mandate Banner: 'Never Trust, Always Verify. Continuous Authentication & Tamper-Evident Auditing.'")
    add_h2("Theoretical & Technical Terms:")
    add_p("• Bcrypt Hashing (12 Salt Rounds): Adaptive key-derivation function that protects passwords against brute-force and rainbow-table attacks.")
    add_p("• JSON Web Token (JWT): RFC 7519 standard representing claims signed using HMAC-SHA256 (HS256).")
    add_p("• Bearer Token Scheme: Attaching JWT inside Authorization: Bearer <token> on every API call.")
    add_h2("Underlying Process:")
    add_p("Transmits POST /api/auth/login. Flask queries users in database.db, checks password via bcrypt.check_password_hash(). On success, issues 8-hour JWT and records USER_LOGIN [SUCCESS] in audit_logs. On failure, returns HTTP 401 and logs USER_LOGIN [FAILED].")

    doc.add_page_break()

    # Screen 3
    add_h1("5. Screen 3: Administrator SOC Overview & 8-Stage Pipeline Tracker")
    add_p("The SOC Overview serves as centralized mission control, providing high-level telemetry, active model status, and lifecycle stage tracking.")
    add_img("ui_3_admin_dashboard.png", "Figure 5.1: Administrator Security Operations Dashboard and 8-Stage Pipeline Tracker")
    add_h2("Visual Interface Breakdown:")
    add_bullet("Active Model Badge: Displays active model name, version ID (v_c01de4), and training benchmark.")
    add_bullet("Telemetry Counter Cards: 4 KPI cards displaying Captured Flows (1,384+), Datasets (4), Threat Deviations (5), and Audit Records (1,316+).")
    add_bullet("8-Stage Lifecycle Progress Trackers: Step-by-step visual cards tracking Ingestion, Sampling, Normalization, Training, Evaluation, Registry, Sniffing, and Auditing.")
    add_h2("Theoretical & Technical Terms:")
    add_p("• Security Operations Center (SOC): Centralized visual dashboard where enterprise systems are monitored and protected.")
    add_p("• Telemetry: Automated collection and transmission of operational measurements for real-time monitoring.")
    add_p("• Pipeline State Machine: Formal architectural construct tracking deterministic progression from raw packets to evaluated models.")
    add_h2("Underlying Process:")
    add_p("Dispatches parallel GET requests to /api/system/status, /api/model/active, and /api/behavioral-analytics. The backend aggregates SQLite metrics and host hardware statistics.")

    doc.add_page_break()

    # Screen 4
    add_h1("6. Screen 4: Datasets Inventory, Partitioning & Management (Stage 1)")
    add_p("Governs CSV ingestion, pre-ingestion validation, stratified subsampling, and target benchmark selection for model training.")
    add_img("ui_4_datasets_management.png", "Figure 6.1: Zero-Trust Datasets Inventory and Target Selection Interface")
    add_h2("Visual Interface Breakdown:")
    add_bullet("Cataloged Datasets Table: Displays uploaded benchmark CSVs, file sizes, total record counts, and timestamps.")
    add_bullet("Active Selection Indicator: Green badge denoting currently selected dataset (unsw_nb15_raw.csv).")
    add_bullet("RBAC Action Buttons: Upload and Select available to both roles; Delete trash icon rendered strictly for Admin.")
    add_h2("Theoretical & Technical Terms:")
    add_p("• Stratified Sampling: Preserving exact benign and multi-attack class distributions without synthetic rows.")
    add_p("• Data Leakage Prevention: Fitting StandardScaler strictly on training split before transforming test or live flows.")
    add_h2("Underlying Process:")
    add_p("Selecting a dataset triggers POST /api/dataset/select, updating is_selected=1 in dataset_history. The preprocessor drops session identifiers, performs median imputation, and applies stratified 70/15/15 partitioning.")

    doc.add_page_break()

    # Screen 5
    add_h1("7. Screen 5: Multi-Dataset Structural Comparison Matrix")
    add_p("Allows security teams to contrast structural, dimensional, and class distribution differences across standard intrusion benchmarks.")
    add_img("ui_5_dataset_comparison.png", "Figure 7.1: Multi-Dataset Comparison Matrix Interface Contrasting NSL-KDD, CIC-IDS2017, and UNSW-NB15")
    add_h2("Visual Interface Breakdown:")
    add_bullet("Side-by-Side Comparison Cards: Contrasts row volume, file size, target column name, feature counts, and clean hygiene status.")
    add_bullet("Class Distribution Visualizations: Horizontal bar charts indicating class imbalance (e.g., 75.2% BENIGN in CIC-IDS2017 vs 58.8% Normal in UNSW-NB15).")
    add_bullet("Feature Schema Alignment Badges: Highlights live feature count mapped to each benchmark (15 for UNSW, 19 for NSL, 22 for CIC).")
    add_h2("Theoretical & Technical Terms:")
    add_p("• Class Imbalance Ratio: Disparity between majority benign flows and rare attack types.")
    add_p("• Schema Alignment: Deterministic transformation mapping raw CSV headers to live packet sniffing features.")
    add_h2("Underlying Process:")
    add_p("Calls GET /api/datasets/compare. Retrieves cataloged metadata, deserializes class distributions, and dynamically maps raw columns to canonical schemas.")

    doc.add_page_break()

    # Screen 6
    add_h1("8. Screen 6: AI Model Training Console & Convergence Telemetry (Stage 2)")
    add_p("Provides an interactive console for configuring and executing machine learning training runs across multiple algorithmic families.")
    add_img("ui_6_model_training.png", "Figure 8.1: AI Model Training Console Configuring Stratified Sample Size, Seed, and Hyperparameters")
    add_h2("Visual Interface Breakdown:")
    add_bullet("Algorithm Selector: Dropdown enabling selection between SVM RBF, Random Forest, Logistic Regression, and Deep MLP.")
    add_bullet("Hyperparameter Controls: Sliders and inputs for Sample Size (N=25,000), Seed (42), Epochs (10), Batch Size (32), and Learning Rate (0.001).")
    add_bullet("Live Progress Bar: Dynamic indicator showing active epoch progress, loss values, and real-time accuracy.")
    add_bullet("Analyst Read-Only Banner: Replaces controls with read-only HUD when viewed by an Analyst.")
    add_h2("Theoretical & Technical Terms:")
    add_p("• Support Vector Classifier (RBF Kernel): Non-linear kernel method projecting features into infinite-dimensional Hilbert space.")
    add_p("• Cross-Entropy Loss: Objective loss function measuring discrepancy between predicted probabilities and true labels.")
    add_p("• Adam Optimizer: Adaptive learning rate algorithm combining momentum with RMSProp.")
    add_h2("Underlying Process:")
    add_p("Clicking 'Start Training' triggers POST /api/model/train (Admin Only). A background thread executes NIDSTrainer.train(), fits StandardScaler, computes validation loss, serializes model.joblib, and updates model_history.")

    doc.add_page_break()

    # Training curves
    add_h1("9. Empirical Training Curves & Mathematical Weight Stabilization")
    add_p("To verify algorithmic convergence and eliminate overfitting, optimization telemetry was tracked across 10 complete epochs.")
    add_img("fig4_1_training_curves.png", "Figure 9.1: Verified 10-Epoch Learning Curves (Loss, Accuracy, and Frobenius Weight Update Norm) Across Datasets")
    add_h2("Mathematical Proof of Convergence:")
    add_p("Model convergence was verified using the Frobenius Weight Update Norm (||ΔW^(e)||_F), defined as the Euclidean magnitude of weight matrix modifications between successive epochs: ||ΔW||_F = sqrt(sum (W_ij^(e) - W_ij^(e-1))^2). In Epoch 1, updates are large (||ΔW^(1)||_F = 13.4667). By Epoch 2, it drops to 0.9260 and stabilizes below 0.80 by Epoch 10, confirming mathematical convergence without overfitting.")

    doc.add_page_break()

    # Screen 7
    add_h1("10. Screen 7: Model Performance Evaluation & Holdout Analytics (Stage 3)")
    add_p("Renders comprehensive holdout test analytics on unseen partitions (N_test=3,750 for UNSW-NB15), ensuring rigorous assessment without optimistic bias.")
    add_img("ui_7_performance_evaluation.png", "Figure 10.1: AI Model Performance Evaluation Dashboard Displaying Confusion Matrix and Metric Cards")
    add_h2("Visual Interface Breakdown:")
    add_bullet("Top-Level Metric Cards: 6 KPI cards displaying Accuracy (96.00%), Precision (96.01%), Recall (96.00%), F1-Score (96.00%), FPR (2.22%), and ROC-AUC (0.9853).")
    add_bullet("Confusion Matrix Heatmap: Displays cell counts for TP, TN, FP, FN with intensity shading.")
    add_bullet("Classification Report Table: Displays class-wise Precision, Recall, and F1-Scores across all 7 traffic categories.")
    add_bullet("ROC Curve Plotter: Plots True Positive Rate vs False Positive Rate across classification thresholds.")
    add_h2("Theoretical & Technical Terms:")
    add_p("• False Positive Rate (FPR): FP / (FP + TN). Probability of raising false alarms on normal traffic (2.22%).")
    add_p("• Recall / Attack Detection Rate: TP / (TP + FN). Proportion of actual cyberattacks detected (96.69%).")
    add_p("• ROC-AUC: Threshold-independent metric measuring class separability (0.9853).")
    add_h2("Underlying Process:")
    add_p("Calls GET /api/model/evaluation/<id>. Loads the serialized model, transforms unseen holdout test split (X_test) with frozen scaler parameters, and computes confusion matrix, classification report, and ROC curve.")

    doc.add_page_break()

    # CM deep dive
    add_h1("11. Confusion Matrix Analysis & Comparative Benchmarking")
    add_p("Evaluating classification matrices reveals the granular distribution of correct classifications and misclassifications across binary and multi-class boundaries.")
    add_img("fig4_2_unsw_binary_cm_roc.png", "Figure 11.1: Verified Holdout Confusion Matrix and ROC Curve (AUC = 0.9853) for UNSW-NB15 Classification")
    add_h2("Binary & Multi-Class Confusion Matrix Breakdown:")
    add_p("On the 3,750 unseen UNSW-NB15 holdout test flows, the active Support Vector Machine correctly identified 2,158 Normal flows (TN) and 1,492 Attack flows (TP), with only 49 False Alarms (FP, FPR = 2.22%) and 51 Missed Attacks (FN, FNR = 3.31%).")
    add_p("Per-Class Results: Normal (97.74% F1, 2,207 support), Generic (94.44% F1, 611 support), Exploits (92.73% F1, 379 support), Fuzzers (94.14% F1, 240 support), DoS (92.93% F1, 151 support), Reconnaissance (92.99% F1, 80 support), Analysis (90.00% F1, 82 support). Weighted Average: Precision = 96.01%, Recall = 96.00%, F1-Score = 96.00%, Overall FPR = 2.22%, ROC-AUC = 0.9853.")

    doc.add_page_break()

    # Screen 8
    add_h1("12. Screen 8: Real-Time Live Network Detection Console (Stage 5)")
    add_p("Inspects incoming network traffic passively on the host machine, performing real-time flow aggregation, feature extraction, and AI risk scoring.")
    add_img("ui_8_live_detection.png", "Figure 12.1: Real-Time Live Network Detection Console with Interface Sniffer Controls and Threat Stream")
    add_h2("Visual Interface Breakdown:")
    add_bullet("Network Interface Discovery: Dropdown enumerating available network adapters (Wi-Fi Realtek RTL8821CE 172.20.10.8).")
    add_bullet("Capture Controls: 'Start Live Monitoring', 'Stop Monitoring', and 'Replay Test Flow' buttons.")
    add_bullet("Streaming Flow Telemetry Feed: Live scrolling table displaying Timestamp, 5-Tuple endpoints, Protocol (TCP/UDP), Flow Duration, Packet/Byte counts, AI Prediction, Confidence, and Risk Badges.")
    add_bullet("Piecewise Risk Scoring Badges: Green (LOW Risk, <60%), Amber (MEDIUM Risk, 60%-85%), and Red (HIGH Risk, >= 85%).")
    add_h2("Theoretical & Technical Terms:")
    add_p("• Passive Packet Sniffing: Capturing network frames from an adapter without transmitting probe packets.")
    add_p("• 5-Tuple Bidirectional Flow Aggregation: Tracking connection state using canonical keys: (min(IPs, IPd), max(IPs, IPd), min(Ps, Pd), max(Ps, Pd), Protocol).")
    add_p("• Inference Latency: Processing time required to classify a single network flow (0.0512 ms/flow, enabling ~19,531 flows/second line-rate throughput).")
    add_h2("Underlying Process:")
    add_p("Starts packet capture via Scapy sniff() in daemon thread. Packets are aggregated into bidirectional flows. On flow expiration, extracts 15 schema attributes, normalizes with training scaler, scores with active model, and persists to SQLite live_detections.")

    doc.add_page_break()

    # Screen 9
    add_h1("13. Screen 9: Behavioral Analytics & Identity Threat Profiling (Stage 6)")
    add_p("Implements User and Entity Behavior Analytics (UEBA), correlating authentication events with live endpoint traffic to detect compromised credentials.")
    add_img("ui_9_audit_logs.png", "Figure 13.1: Zero-Trust Behavioral Analytics and Identity Threat Profiling Console")
    add_h2("Visual Interface Breakdown:")
    add_bullet("Temporal Access Heatmap: Visual distribution of user logins across 24 hours (59% morning 06:00-12:00 UTC, 40% afternoon, 1% off-hours).")
    add_bullet("Monitored Endpoint Cards: Summarizes activity across 13 network devices, highlighting unusual transmission volumes.")
    add_bullet("Behavioral Deviation Feed: Alerts flagging unusual user activity (e.g., unexpected off-hours access, rapid endpoint switching).")
    add_h2("Theoretical & Technical Terms:")
    add_p("• User and Entity Behavior Analytics (UEBA): Tracking normal behavioral baselines for users and devices to detect insider threats.")
    add_p("• Baseline Anomaly Thresholding: Comparing operational metrics against established statistical intervals.")
    add_p("• Non-Repudiation: Assurance that an entity cannot deny the authenticity of their signature or action within an audit log.")
    add_h2("Underlying Process:")
    add_p("Calls GET /api/behavioral-analytics. The backend aggregates 1,316+ historical audit events and combines them with live_detections, computing anomaly scores across active IP addresses.")

    doc.add_page_break()

    # Screen 10
    add_h1("14. Screen 10: Forensic Audit Trail & Privilege Enforcement (Stage 6)")
    add_p("Maintains a permanent, tamper-evident record of all security-relevant transactions, providing empirical proof of Zero-Trust access control.")
    add_img("ui_10_audit_trail_table.png", "Figure 14.1: Zero-Trust Forensic Audit Trail Table Displaying Cryptographic Event Records")
    add_h2("Visual Interface Breakdown:")
    add_bullet("Filterable Audit Table: Displays Event ID, Timestamp, Username, Action Code, IP Address, Status (SUCCESS, BLOCKED, REJECTED), and Details.")
    add_bullet("Severity-Coded Badges: Green for verified authentications; Amber for session expirations; Red for blocked privilege escalation attempts.")
    add_bullet("CSV Export Utility: Allows compliance auditors to download raw forensic event logs for compliance reporting.")
    add_h2("Theoretical & Technical Terms:")
    add_p("• Tamper-Evident Audit Trail: Append-only persistence schema where log records cannot be altered or deleted.")
    add_p("• Privilege Escalation Defense: Intercepting attempts by unprivileged users to execute administrative routes (@require_role(['Admin'])).")
    add_p("• Stateless Session Invalidation: Automatically rejecting expired JWT tokens without maintaining complex server-side session tables.")
    add_h2("Underlying Process & Empirical Evidence:")
    add_p("Every API route wraps execution inside log_audit_event(). Database queries confirm 1,316 total audit entries: 522 EXPIRED_OR_INVALID_TOKEN (HTTP 401), 113 USER_LOGIN [FAILED] (HTTP 401), 72 USER_LOGIN [SUCCESS] (HTTP 200), 105 MODEL_TRAINING_START, 124 LIVE_CAPTURE_START/STOP, 63 LIVE_REPLAY_TEST, and 28 RBAC_ACCESS_DENIED (HTTP 403 Forbidden).")

    doc.add_page_break()

    # Master Scorecard & Viva Guide
    add_h1("15. Master Project Scorecard & Faculty Viva Defense Guide")
    add_p("This concluding section synthesizes project accomplishments and arms the candidate with defensible answers to anticipated viva review questions.")
    add_h2("Master System Scorecard:")
    add_bullet("Benchmark Ingestion: 5.66M+ records cataloged across UNSW-NB15, NSL-KDD, and CIC-IDS2017 with zero train-test data leakage.")
    add_bullet("Champion Classifier: Support Vector Machine (RBF Kernel) on UNSW-NB15 achieved 96.00% Accuracy, 96.01% Precision, 96.00% Recall, a low 2.22% False Positive Rate, and 0.9853 ROC-AUC.")
    add_bullet("Ensemble Classifier: Random Forest achieved 97.42% Accuracy on UNSW-NB15 and 99.00% Accuracy on NSL-KDD.")
    add_bullet("Live Detection Speed: Per-flow inference latency of 0.0512 ms/flow (~19,531 flows/second line-rate capacity) across 1,384+ live Wi-Fi flows.")
    add_bullet("Zero-Trust RBAC: Complete separation of duties between Admin and Analyst; 28 unauthorized privilege escalation attempts intercepted with HTTP 403 Forbidden and logged across 1,316 audit entries.")
    add_h2("Defensible Responses to Critical Viva Review Questions:")
    add_p("1. Why choose an RBF Kernel SVM over simpler Linear Regression or Decision Trees?\nAnswer: Network intrusion features exhibit highly non-linear, multi-dimensional correlations. Linear models achieved only 89.45% accuracy with an unacceptable 5.12% false alarm rate. The RBF Gaussian kernel projects features into infinite-dimensional Hilbert space, establishing optimal non-linear separation boundaries that achieve 96.00% accuracy and 0.9853 ROC-AUC.")
    add_p("2. Why is keeping False Positive Rate (FPR) below 2.5% more critical than raw Accuracy in production?\nAnswer: In high-throughput corporate networks evaluating 100,000 flows per hour, a 10% FPR generates 10,000 false alarms every hour, causing severe alert fatigue. By restricting FPR to 2.22%, our model ensures that alerts represent actionable, statistically validated threats.")
    add_p("3. How does Zero Trust specifically protect the AI pipeline?\nAnswer: Under Zero Trust, no user or component inside the network is implicitly trusted. Our system enforces Separation of Duties: Security Analysts can monitor live traffic feeds and view audit logs but are cryptographically blocked by @require_role(['Admin']) from retraining models, altering weights, or deleting forensic datasets. Every unauthorized attempt is rejected with HTTP 403 and committed to an immutable audit trail.")

    doc.save(DOCX_PATH)
    print(f"SUCCESS: Generated DOCX at {DOCX_PATH}")

if __name__ == "__main__":
    build_pdf()
    build_docx()

    # Copy to Desktop folder for easy access
    desktop_pdf = os.path.join(DESKTOP_DIR, PDF_FILENAME)
    desktop_docx = os.path.join(DESKTOP_DIR, DOCX_FILENAME)
    shutil.copy2(PDF_PATH, desktop_pdf)
    shutil.copy2(DOCX_PATH, desktop_docx)
    print(f"SUCCESS: Copied PDF to {desktop_pdf}")
    print(f"SUCCESS: Copied DOCX to {desktop_docx}")
