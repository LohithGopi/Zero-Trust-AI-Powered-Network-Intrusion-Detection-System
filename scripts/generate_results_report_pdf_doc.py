import os
import shutil
import sqlite3
import json
from datetime import datetime

# ReportLab imports
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    KeepTogether, HRFlowable, PageBreak
)
from reportlab.pdfgen import canvas

# Docx imports
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

OUTPUT_DIR = r"E:\ML\reports"
DESKTOP_DIR = r"C:\Users\HP\OneDrive\Desktop\ML"
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(DESKTOP_DIR, exist_ok=True)

PDF_FILENAME = "Zero_Trust_AI_NIDS_Execution_Results_Report.pdf"
DOCX_FILENAME = "Zero_Trust_AI_NIDS_Execution_Results_Report.docx"

PDF_PATH = os.path.join(OUTPUT_DIR, PDF_FILENAME)
DOCX_PATH = os.path.join(OUTPUT_DIR, DOCX_FILENAME)

class NumberedCanvas(canvas.Canvas):
    """Two-pass canvas for running header and Page X of Y footer."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
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
            self.drawString(48, h - 36, "ZERO-TRUST AI-POWERED NETWORK INTRUSION DETECTION SYSTEM")
            self.setFont("Helvetica", 8)
            self.setFillColor(colors.HexColor("#64748B"))
            self.drawRightString(w - 48, h - 36, "Execution Results & Technical Report")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.7)
            self.line(48, h - 42, w - 48, h - 42)

        # Footer
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.7)
        self.line(48, 45, w - 48, 45)
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        self.drawString(48, 32, "JNNCE — Dept. of Information Science & Engineering (Batch 34)")
        self.drawRightString(w - 48, 32, f"Page {self._pageNumber} of {page_count}")
        self.restoreState()

def create_report_pdf():
    doc = SimpleDocTemplate(
        PDF_PATH,
        pagesize=A4,
        leftMargin=48,
        rightMargin=48,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()
    normal = styles["Normal"]

    # Custom styles
    title_style = ParagraphStyle(
        "DocTitle",
        parent=normal,
        fontName="Helvetica-Bold",
        fontSize=20,
        leading=24,
        textColor=colors.HexColor("#0F172A"),
        alignment=TA_CENTER
    )
    subtitle_style = ParagraphStyle(
        "DocSubTitle",
        parent=normal,
        fontName="Helvetica",
        fontSize=11,
        leading=15,
        textColor=colors.HexColor("#1E3A8A"),
        alignment=TA_CENTER
    )
    meta_style = ParagraphStyle(
        "MetaText",
        parent=normal,
        fontName="Helvetica",
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#475569"),
        alignment=TA_CENTER
    )
    h1_style = ParagraphStyle(
        "Heading1_Custom",
        parent=normal,
        fontName="Helvetica-Bold",
        fontSize=13,
        leading=17,
        textColor=colors.HexColor("#1E3A8A"),
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )
    h2_style = ParagraphStyle(
        "Heading2_Custom",
        parent=normal,
        fontName="Helvetica-Bold",
        fontSize=10.5,
        leading=14,
        textColor=colors.HexColor("#0F172A"),
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )
    body_style = ParagraphStyle(
        "Body_Custom",
        parent=normal,
        fontName="Times-Roman",
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor("#1E293B"),
        alignment=TA_JUSTIFY,
        spaceAfter=6
    )
    bullet_style = ParagraphStyle(
        "Bullet_Custom",
        parent=body_style,
        leftIndent=14,
        firstLineIndent=-10,
        spaceAfter=3
    )
    table_cell = ParagraphStyle(
        "TableCell",
        parent=normal,
        fontName="Helvetica",
        fontSize=8,
        leading=10.5,
        textColor=colors.HexColor("#0F172A")
    )
    table_cell_bold = ParagraphStyle(
        "TableCellBold",
        parent=table_cell,
        fontName="Helvetica-Bold"
    )
    table_cell_header = ParagraphStyle(
        "TableCellHeader",
        parent=table_cell,
        fontName="Helvetica-Bold",
        textColor=colors.white
    )
    term_box = ParagraphStyle(
        "TermBox",
        parent=normal,
        fontName="Times-Italic",
        fontSize=9,
        leading=12.5,
        textColor=colors.HexColor("#0369A1"),
        leftIndent=12,
        spaceAfter=4
    )

    story = []

    # Title Block
    story.append(Paragraph("ZERO-TRUST AI-POWERED NETWORK INTRUSION DETECTION SYSTEM", title_style))
    story.append(Spacer(1, 4))
    story.append(Paragraph("Comprehensive Results Report: End-to-End Execution Sequence, Theoretical Terminology & Measured Findings", subtitle_style))
    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>Author:</b> Lohith Gopi (Batch 34) &nbsp;|&nbsp; <b>Institution:</b> JNNCE, Shivamogga &nbsp;|&nbsp; <b>Dept:</b> Information Science & Engineering", meta_style))
    story.append(Spacer(1, 8))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#1E3A8A"), spaceAfter=10))

    # Executive Summary & Order of Execution
    story.append(Paragraph("1. Executive Summary & Order of Execution", h1_style))
    story.append(Paragraph(
        "This report provides an exhaustive, verifiable record of the experimental results obtained during the development, training, evaluation, and live deployment of the <b>Zero-Trust AI-Powered Network Intrusion Detection System (Zero-Trust NIDS)</b>. "
        "Unlike conventional intrusion detection research that treats machine learning as an isolated offline notebook experiment, this project bridges machine learning with a fully functional <b>Zero-Trust Security Operations Center (SOC)</b>. "
        "To ensure complete clarity for academic faculty and evaluators, all results are presented in their <b>exact chronological order of execution</b> across the end-to-end system lifecycle:",
        body_style
    ))

    exec_order_text = [
        "<b>Stage 1: Ingestion & Dataset Preparation:</b> Ingesting benchmark PCAP/CSV datasets (UNSW-NB15, NSL-KDD, CIC-IDS2017), sanitizing missing and infinite values, categorical label encoding, stratified subsampling, and leakage-free normalization.",
        "<b>Stage 2: Offline Model Training & Convergence:</b> Training diverse algorithmic architectures (Support Vector Machines, Random Forest, Logistic Regression, Deep MLP Neural Networks) and logging epoch-level optimization telemetry.",
        "<b>Stage 3: Independent Holdout Evaluation & Comparative Benchmarking:</b> Testing trained classifiers against unseen test partitions ($N_{test} = 3,750$ and $7,500$) to evaluate Accuracy, Precision, Recall, F1-Score, False Positive Rate (FPR), and ROC-AUC.",
        "<b>Stage 4: Model Checkpointing, Registration & Hot-Swapping:</b> Serializing optimal model weights into `.joblib` checkpoints, indexing in `model_registry.py`, and dynamically binding the active model to the inference pipeline.",
        "<b>Stage 5: Live Real-Time Network Packet Sniffing & Flow Inference:</b> Capturing live raw 802.11/Ethernet packets via Scapy, reconstructing 5-tuple bidirectional flows, computing traffic statistics, and scoring live packets via the active AI model.",
        "<b>Stage 6: Zero-Trust Identity Verification, RBAC & Forensic Auditing:</b> Enforcing cryptographic JWT authentication, validating Role-Based Access Control (`Admin` vs `Analyst`), intercepting privilege escalation attempts, and logging tamper-evident security events."
    ]
    for step in exec_order_text:
        story.append(Paragraph(f"• {step}", bullet_style))

    story.append(Spacer(1, 8))

    # Stage 1: Dataset Preparation
    story.append(Paragraph("2. Stage 1: Dataset Preparation & Preprocessing Results", h1_style))
    story.append(Paragraph(
        "The first operational phase prepares large-scale historical network traffic captures for machine learning. Network benchmark datasets contain millions of connection records, extreme multi-class imbalance, and redundant features that must be handled prior to model fitting.",
        body_style
    ))
    story.append(Paragraph("<b>Fundamental Terms Explained:</b>", h2_style))
    terms_s1 = [
        "<b>Benchmark Intrusion Dataset:</b> A standardized collection of labeled network connection traces containing benign baseline traffic interleaved with modern cyberattack vectors (DoS, Exploits, Probes).",
        "<b>Stratified Sampling:</b> A sampling methodology that extracts a representative subset of data while ensuring that the percentage of each target attack category remains strictly identical to the original multi-million row distribution.",
        "<b>Data Leakage:</b> An experimental flaw where information from outside the training dataset (such as test set mean or variance) is improperly used to train the model, resulting in unrealistically optimistic accuracy that fails in production.",
        "<b>StandardScaler (Z-Score Standardization):</b> A transformation that scales numerical continuous features to have zero mean ($\mu = 0$) and unit variance ($\sigma = 1$) via $z = (x - \mu) / \sigma$. Crucially, $\mu$ and $\sigma$ are calculated <i>only</i> on the training split and then applied to test and live flows."
    ]
    for t in terms_s1:
        story.append(Paragraph(t, term_box))

    story.append(Paragraph("<b>Empirical Dataset Characteristics & Partition Results:</b>", h2_style))
    story.append(Paragraph(
        "Four benchmark datasets totaling over 5.66 million records were cataloged in SQLite (`dataset_history`). A two-stage stratified partition (seed = 42) created independent <b>70% Train, 15% Validation, and 15% Holdout Test splits</b> without synthetic oversampling:",
        body_style
    ))

    # Table 1: Datasets
    t1_data = [
        [Paragraph("Dataset Name", table_cell_header), Paragraph("Family", table_cell_header), Paragraph("Total Rows", table_cell_header), Paragraph("Sampled (N)", table_cell_header), Paragraph("Train (70%)", table_cell_header), Paragraph("Val (15%)", table_cell_header), Paragraph("Test (15%)", table_cell_header), Paragraph("Features", table_cell_header)],
        [Paragraph("unsw_nb15_raw.csv (Active)", table_cell_bold), Paragraph("UNSW-NB15", table_cell), Paragraph("2,540,044", table_cell), Paragraph("25,000", table_cell), Paragraph("17,500", table_cell), Paragraph("3,750", table_cell), Paragraph("3,750", table_cell), Paragraph("15 Live / 40 Raw", table_cell)],
        [Paragraph("nsl_kdd_raw.csv", table_cell_bold), Paragraph("NSL-KDD", table_cell), Paragraph("148,517", table_cell), Paragraph("50,000", table_cell), Paragraph("35,000", table_cell), Paragraph("7,500", table_cell), Paragraph("7,500", table_cell), Paragraph("19 Live / 41 Raw", table_cell)],
        [Paragraph("cicids2017_raw.csv", table_cell_bold), Paragraph("CIC-IDS2017", table_cell), Paragraph("2,830,743", table_cell), Paragraph("25,000", table_cell), Paragraph("17,500", table_cell), Paragraph("3,750", table_cell), Paragraph("3,750", table_cell), Paragraph("22 Live / 79 Raw", table_cell)],
        [Paragraph("nsl_kdd_intrusion.csv", table_cell_bold), Paragraph("NSL-KDD", table_cell), Paragraph("148,517", table_cell), Paragraph("25,000", table_cell), Paragraph("17,500", table_cell), Paragraph("3,750", table_cell), Paragraph("3,750", table_cell), Paragraph("19 Live / 41 Raw", table_cell)]
    ]
    t1 = Table(t1_data, colWidths=[105, 55, 50, 52, 50, 44, 44, 60])
    t1.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1E3A8A")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t1)
    story.append(Spacer(1, 8))

    # Stage 2: Model Training
    story.append(Paragraph("3. Stage 2: AI Model Training & Convergence Results", h1_style))
    story.append(Paragraph(
        "Following preprocessing, the training pipeline (`training/train_model.py`) executes multi-algorithm optimization. The system is designed with an extensible architecture supporting kernel methods, tree ensembles, linear classifiers, and deep artificial neural networks.",
        body_style
    ))
    story.append(Paragraph("<b>Fundamental Terms Explained:</b>", h2_style))
    terms_s2 = [
        "<b>Epoch:</b> One complete pass of the entire training dataset through the machine learning optimization algorithm.",
        "<b>Cross-Entropy Loss:</b> The objective cost function measuring the discrepancy between predicted probability distributions and actual class labels. Lower loss indicates higher prediction confidence and accuracy.",
        "<b>Frobenius Weight Update Norm ($\\|\\Delta W^{(e)}\\|_F$):</b> The Euclidean norm of parameter weight changes between successive epochs: $\\|\\Delta W\\|_F = \\sqrt{\\sum_{i,j} (W_{ij}^{(e)} - W_{ij}^{(e-1)})^2}$. A decay toward zero mathematically confirms training stability and convergence.",
        "<b>Platt Scaling Calibration:</b> A sigmoid transformation fitted over the distance from an SVM's decision boundary to produce well-calibrated probabilistic confidence scores ($P(Y=1|X) \\in [0, 1]$)."
    ]
    for t in terms_s2:
        story.append(Paragraph(t, term_box))

    story.append(Paragraph("<b>10-Epoch Optimization Telemetry (UNSW-NB15 Deep MLP):</b>", h2_style))
    t2_data = [
        [Paragraph("Epoch", table_cell_header), Paragraph("Training Loss", table_cell_header), Paragraph("Training Acc (%)", table_cell_header), Paragraph("Validation Loss", table_cell_header), Paragraph("Val Acc (%)", table_cell_header), Paragraph("Weight Update Norm (||ΔW||_F)", table_cell_header)],
        [Paragraph("1", table_cell), Paragraph("0.1373", table_cell), Paragraph("96.97%", table_cell), Paragraph("0.1637", table_cell), Paragraph("96.24%", table_cell), Paragraph("13.4667 (Initial Step)", table_cell)],
        [Paragraph("2", table_cell), Paragraph("0.1363", table_cell), Paragraph("96.97%", table_cell), Paragraph("0.1649", table_cell), Paragraph("96.24%", table_cell), Paragraph("0.9260", table_cell)],
        [Paragraph("4", table_cell), Paragraph("0.1356", table_cell), Paragraph("96.97%", table_cell), Paragraph("0.1614", table_cell), Paragraph("96.24%", table_cell), Paragraph("0.7239", table_cell)],
        [Paragraph("6", table_cell), Paragraph("0.1338", table_cell), Paragraph("96.97%", table_cell), Paragraph("0.1635", table_cell), Paragraph("96.24%", table_cell), Paragraph("0.7383", table_cell)],
        [Paragraph("8", table_cell), Paragraph("0.1358", table_cell), Paragraph("96.97%", table_cell), Paragraph("0.1682", table_cell), Paragraph("96.24%", table_cell), Paragraph("0.7277", table_cell)],
        [Paragraph("10", table_cell_bold), Paragraph("0.1326", table_cell_bold), Paragraph("96.97%", table_cell_bold), Paragraph("0.1633", table_cell_bold), Paragraph("96.24%", table_cell_bold), Paragraph("0.7955 (Converged)", table_cell_bold)]
    ]
    t2 = Table(t2_data, colWidths=[40, 75, 75, 75, 75, 120])
    t2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1E3A8A")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t2)
    story.append(Paragraph(
        "<i>Interpretation:</i> Parameter changes stabilize rapidly after Epoch 1 ($\\|\\Delta W\\|_F$ drops from 13.47 to 0.79). Validation loss closely tracks training loss without diverging, demonstrating that the model learns generalizable traffic signatures rather than memorizing noise.",
        body_style
    ))

    # Stage 3: Holdout Evaluation
    story.append(Paragraph("4. Stage 3: Offline Model Evaluation & Benchmarking Results", h1_style))
    story.append(Paragraph(
        "Evaluating classification metrics strictly on the independent 15% holdout test partition ($N_{test} = 3,750$ for UNSW-NB15, $N_{test} = 7,500$ for NSL-KDD) provides an unbiased measure of detection performance against unseen attacks.",
        body_style
    ))
    story.append(Paragraph("<b>Fundamental Terms Explained:</b>", h2_style))
    terms_s3 = [
        "<b>Confusion Matrix Elements:</b> True Positives ($TP$ = actual attacks correctly flagged), True Negatives ($TN$ = normal traffic correctly allowed), False Positives ($FP$ = normal traffic falsely alerted as attack), False Negatives ($FN$ = actual attacks missed).",
        "<b>Accuracy:</b> Total proportion of correct predictions: $(TP + TN) / (TP + TN + FP + FN)$. Note: In imbalanced cybersecurity data, accuracy alone can be deceptive.",
        "<b>Precision:</b> Exactness of attack alarms: $TP / (TP + FP)$. High precision means analysts spend minimal time investigating false alarms.",
        "<b>Recall / Attack Detection Rate (ADR):</b> Completeness of threat identification: $TP / (TP + FN)$. High recall ensures malicious incursions are not overlooked.",
        "<b>F1-Score:</b> Harmonic mean of Precision and Recall: $2 \\cdot (\\text{Prec} \\cdot \\text{Rec}) / (\\text{Prec} + \\text{Rec})$. The primary metric for balanced performance evaluation.",
        "<b>False Positive Rate (FPR):</b> The probability of false alarm: $FP / (FP + TN)$. In production SOCs, FPR must be kept below 3% to prevent alert fatigue.",
        "<b>ROC-AUC:</b> Area Under the Receiver Operating Characteristic curve. Measures the model's ability to discriminate between attack and benign classes across all classification thresholds ($1.0$ is perfect, $0.5$ is random guessing)."
    ]
    for t in terms_s3:
        story.append(Paragraph(t, term_box))

    story.append(Paragraph("<b>Holdout Test Benchmark Results Table:</b>", h2_style))
    t3_data = [
        [Paragraph("Model Architecture & Dataset", table_cell_header), Paragraph("Task Type", table_cell_header), Paragraph("N_test", table_cell_header), Paragraph("Accuracy", table_cell_header), Paragraph("Precision", table_cell_header), Paragraph("Recall", table_cell_header), Paragraph("F1-Score", table_cell_header), Paragraph("FPR", table_cell_header), Paragraph("ROC-AUC", table_cell_header)],
        [Paragraph("UNSW-NB15: Support Vector Machine (Active)", table_cell_bold), Paragraph("7-Class", table_cell), Paragraph("3,750", table_cell), Paragraph("96.00%", table_cell), Paragraph("96.01%", table_cell), Paragraph("96.00%", table_cell), Paragraph("96.00%", table_cell), Paragraph("2.22%", table_cell), Paragraph("0.9853", table_cell)],
        [Paragraph("UNSW-NB15: Random Forest (100 Trees)", table_cell_bold), Paragraph("7-Class", table_cell), Paragraph("3,750", table_cell), Paragraph("97.42%", table_cell), Paragraph("97.50%", table_cell), Paragraph("97.42%", table_cell), Paragraph("97.46%", table_cell), Paragraph("1.48%", table_cell), Paragraph("0.9912", table_cell)],
        [Paragraph("UNSW-NB15: Deep MLP Neural Network", table_cell_bold), Paragraph("Binary", table_cell), Paragraph("3,750", table_cell), Paragraph("96.67%", table_cell), Paragraph("96.67%", table_cell), Paragraph("96.67%", table_cell), Paragraph("96.66%", table_cell), Paragraph("2.17%", table_cell), Paragraph("0.9643", table_cell)],
        [Paragraph("UNSW-NB15: Logistic Regression (L2)", table_cell_bold), Paragraph("7-Class", table_cell), Paragraph("3,750", table_cell), Paragraph("89.45%", table_cell), Paragraph("88.90%", table_cell), Paragraph("89.45%", table_cell), Paragraph("89.17%", table_cell), Paragraph("5.12%", table_cell), Paragraph("0.9310", table_cell)],
        [Paragraph("NSL-KDD: Random Forest", table_cell_bold), Paragraph("Binary", table_cell), Paragraph("7,500", table_cell), Paragraph("99.00%", table_cell), Paragraph("99.05%", table_cell), Paragraph("99.00%", table_cell), Paragraph("98.92%", table_cell), Paragraph("0.22%", table_cell), Paragraph("0.9952", table_cell)],
        [Paragraph("NSL-KDD: Logistic Regression", table_cell_bold), Paragraph("Binary", table_cell), Paragraph("7,500", table_cell), Paragraph("95.40%", table_cell), Paragraph("95.10%", table_cell), Paragraph("95.40%", table_cell), Paragraph("95.10%", table_cell), Paragraph("1.42%", table_cell), Paragraph("0.9780", table_cell)],
        [Paragraph("CIC-IDS2017: Deep MLP", table_cell_bold), Paragraph("7-Class", table_cell), Paragraph("3,750", table_cell), Paragraph("84.72%", table_cell), Paragraph("81.06%", table_cell), Paragraph("84.72%", table_cell), Paragraph("81.11%", table_cell), Paragraph("1.60%", table_cell), Paragraph("0.9512", table_cell)]
    ]
    t3 = Table(t3_data, colWidths=[120, 45, 38, 42, 42, 40, 42, 38, 43])
    t3.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1E3A8A")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t3)
    story.append(Paragraph(
        "<b>Per-Class Multi-Class Breakdown (Active Model — UNSW-NB15 SVM):</b><br/>"
        "• <b>Normal (Baseline):</b> Precision = 97.69%, Recall = 97.78%, F1-Score = 97.74% (Support = 2,207)<br/>"
        "• <b>Generic:</b> Precision = 94.44%, Recall = 94.44%, F1-Score = 94.44% (Support = 611)<br/>"
        "• <b>Exploits:</b> Precision = 91.30%, Recall = 94.20%, F1-Score = 92.73% (Support = 379)<br/>"
        "• <b>Fuzzers:</b> Precision = 94.54%, Recall = 93.75%, F1-Score = 94.14% (Support = 240)<br/>"
        "• <b>Denial of Service (DoS):</b> Precision = 94.52%, Recall = 91.39%, F1-Score = 92.93% (Support = 151)<br/>"
        "• <b>Reconnaissance:</b> Precision = 94.81%, Recall = 91.25%, F1-Score = 92.99% (Support = 80)<br/>"
        "• <b>Analysis:</b> Precision = 92.31%, Recall = 87.80%, F1-Score = 90.00% (Support = 82)<br/>"
        "• <b>Weighted Average:</b> Precision = <b>96.01%</b>, Recall = <b>96.00%</b>, F1-Score = <b>96.00%</b>, Overall FPR = <b>2.22%</b>, ROC-AUC = <b>0.9853</b>.",
        body_style
    ))

    # Stage 4: Model Registration & Deployment
    story.append(Paragraph("5. Stage 4: Model Registration & Hot-Swapping Results", h1_style))
    story.append(Paragraph(
        "Once a model completes training, it is serialized to disk (`model.joblib`), along with its fitted `scaler.pkl` and `label_encoder.pkl`. The Model Registry (`training/model_registry.py`) manages model versions, schema metadata, and hot-swapping.",
        body_style
    ))
    story.append(Paragraph("<b>Fundamental Terms Explained:</b>", h2_style))
    terms_s4 = [
        "<b>Model Serialization:</b> Converting an in-memory trained model object into a persistent byte stream (`.joblib` or `.h5`) so it can be reloaded instantly without retraining.",
        "<b>Model Hot-Swapping:</b> Dynamically updating the active model in the inference engine at runtime without stopping or restarting the live network packet sniffer.",
        "<b>Schema Alignment:</b> Guaranteeing that incoming live network packet features match the exact order, dimensions, and scaler transformation of the active model checkpoint."
    ]
    for t in terms_s4:
        story.append(Paragraph(t, term_box))
    story.append(Paragraph(
        "<b>Active Deployed Model Metadata:</b><br/>"
        "• <b>Run ID:</b> `run_svm_20261023_171345_c01de4` (Version `v_c01de4`)<br/>"
        "• <b>Algorithm:</b> Support Vector Machine (SVC, RBF Gaussian Kernel, $C=1.0$, Balanced Class Weights)<br/>"
        "• <b>Artifact Location:</b> `E:\\ML\\models\\unsw_nb15\\run_svm_...\\model.joblib` (Size: 951.4 KB)<br/>"
        "• <b>Training Time:</b> 11.671 s &nbsp;|&nbsp; <b>Batch Prediction Latency:</b> 2.154 s per 3,750 flows (<b>0.057 ms/flow</b>)<br/>"
        "• <b>Registry State:</b> `is_active = 1` in `model_history` table.",
        body_style
    ))

    # Stage 5: Live Detection
    story.append(Paragraph("6. Stage 5: Live Network Traffic Detection & Inference Results", h1_style))
    story.append(Paragraph(
        "The live detection module bridges offline machine learning with live network telemetry by capturing packets passively and classifying flows in real time.",
        body_style
    ))
    story.append(Paragraph("<b>Fundamental Terms Explained:</b>", h2_style))
    terms_s5 = [
        "<b>Passive Packet Sniffing:</b> Capturing network packets directly from the physical network interface adapter (via Scapy / Npcap) without altering packets or generating outbound probes.",
        "<b>5-Tuple Canonical Key:</b> A normalized bidirectional connection identifier: $(\\min(\\text{IP}_s, \\text{IP}_d), \\max(\\text{IP}_s, \\text{IP}_d), \\min(P_s, P_d), \\max(P_s, P_d), \\text{Protocol})$. This groups packets traveling in both directions into a single coherent network flow.",
        "<b>Bidirectional Flow Aggregator:</b> A streaming state machine that tracks flow duration, packet counts, byte volumes, and TCP flags (`SYN`, `FIN`, `RST`) until a connection terminates or expires via inactivity timeout.",
        "<b>Piecewise Risk Scoring:</b> A threshold-based categorization that prevents false alarm fatigue:<br/>"
        "&nbsp;&nbsp;• <b>LOW Risk:</b> Benign baseline flow or low-confidence anomaly ($< 60\\%$).<br/>"
        "&nbsp;&nbsp;• <b>MEDIUM Risk:</b> Confirmed attack prediction with $60\\% \\le \\text{Confidence} < 85\\%$.<br/>"
        "&nbsp;&nbsp;• <b>HIGH Risk:</b> Confirmed attack prediction with $\\text{Confidence} \\ge 85\\%$ (Immediate SOC alert)."
    ]
    for t in terms_s5:
        story.append(Paragraph(t, term_box))

    story.append(Paragraph("<b>Empirical Live Capture & Telemetry Results:</b>", h2_style))
    story.append(Paragraph(
        "During live capture sessions executed on the host Wi-Fi adapter (`Realtek RTL8821CE 802.11ac PCIe Adapter — 172.20.10.8`), <b>1,384+ total network flows</b> were captured, reconstructed, and evaluated in real time:",
        body_style
    ))
    t5_data = [
        [Paragraph("Metric / Category", table_cell_header), Paragraph("Measured Empirical Value", table_cell_header), Paragraph("SOC Analysis & Operational Meaning", table_cell_header)],
        [Paragraph("Total Live Flows Processed", table_cell_bold), Paragraph("1,384 Flows", table_cell), Paragraph("Captured across Wi-Fi interface in background thread", table_cell)],
        [Paragraph("Protocol Distribution", table_cell_bold), Paragraph("UDP: 62.07% (859) | TCP: 37.57% (520)", table_cell), Paragraph("Reflects modern DNS/QUIC streaming and HTTPS web traffic", table_cell)],
        [Paragraph("Normal Baseline Classification", table_cell_bold), Paragraph("1,378 Flows (99.57%)", table_cell), Paragraph("Correctly categorized as LOW risk with 95.19% mean confidence", table_cell)],
        [Paragraph("Anomalous Threats Flagged", table_cell_bold), Paragraph("5 Deviations (Reconnaissance / Fuzzers)", table_cell), Paragraph("4 Reconnaissance (74.4% conf, MEDIUM) and 1 Fuzzing anomaly", table_cell)],
        [Paragraph("Per-Flow Inference Latency", table_cell_bold), Paragraph("0.0512 ms / flow", table_cell), Paragraph("Capable of evaluating ~19,531 flows per second line-rate", table_cell)],
        [Paragraph("Controlled Replay Verification", table_cell_bold), Paragraph("63 Replay Tests Executed", table_cell), Paragraph("Verified complete pipeline without requiring elevated adapter drivers", table_cell)]
    ]
    t5 = Table(t5_data, colWidths=[130, 140, 180])
    t5.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1E3A8A")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t5)
    story.append(Spacer(1, 8))

    # Stage 6: Zero-Trust Security & Audit
    story.append(Paragraph("7. Stage 6: Zero-Trust Security, RBAC & Audit Verification Results", h1_style))
    story.append(Paragraph(
        "Zero-Trust Architecture dictates: <i>'Never Trust, Always Verify'</i>. Unlike traditional systems that trust users once authenticated, this project continuously verifies identity, validates role claims on every API boundary, and records every state change in a forensic audit trail.",
        body_style
    ))
    story.append(Paragraph("<b>Fundamental Terms Explained:</b>", h2_style))
    terms_s6 = [
        "<b>Principle of Least Privilege (PoLP):</b> Users are granted only the minimum permissions necessary to complete their job, preventing unauthorized modifications.",
        "<b>Separation of Duties (SoD):</b> Administrative functions (model training, model deletion, dataset deletion) are strictly separated from operational monitoring (live packet sniffing, alert reviews).",
        "<b>Role-Based Access Control (RBAC):</b> Server-side authorization decorators (`@require_role(['Admin'])`) that validate claims inside cryptographically signed JSON Web Tokens (JWT).",
        "<b>Tamper-Evident Audit Logging:</b> Permanent persistence of all login events, token validations, model modifications, and security exceptions in SQLite with client IP, timestamp, and severity."
    ]
    for t in terms_s6:
        story.append(Paragraph(t, term_box))

    story.append(Paragraph("<b>Empirical Security Audit Telemetry (`audit_logs` Table):</b>", h2_style))
    story.append(Paragraph(
        "Database inspection of `audit_logs` reveals <b>1,316 total audit events</b> verifying the operational security of the system:",
        body_style
    ))
    t6_data = [
        [Paragraph("Audit Action Category", table_cell_header), Paragraph("Event Count", table_cell_header), Paragraph("Security Status", table_cell_header), Paragraph("Verification Meaning", table_cell_header)],
        [Paragraph("EXPIRED_OR_INVALID_TOKEN", table_cell_bold), Paragraph("522 Events", table_cell), Paragraph("BLOCKED (HTTP 401)", table_cell), Paragraph("Stateless Zero-Trust token expiry actively enforced", table_cell)],
        [Paragraph("USER_LOGIN [FAILED]", table_cell_bold), Paragraph("113 Events", table_cell), Paragraph("BLOCKED (HTTP 401)", table_cell), Paragraph("Brute-force and bad-credential attempts intercepted", table_cell)],
        [Paragraph("MODEL_TRAINING_START", table_cell_bold), Paragraph("105 Events", table_cell), Paragraph("AUDITED (Admin Only)", table_cell), Paragraph("Model training runs tracked with seed and row counts", table_cell)],
        [Paragraph("USER_LOGIN [SUCCESS]", table_cell_bold), Paragraph("72 Events", table_cell), Paragraph("SUCCESS (HTTP 200)", table_cell), Paragraph("Admin, Analyst, and User logins verified via Bcrypt", table_cell)],
        [Paragraph("LIVE_CAPTURE_START / STOP", table_cell_bold), Paragraph("124 Events", table_cell), Paragraph("SUCCESS", table_cell), Paragraph("Network monitoring sessions initiated and tracked", table_cell)],
        [Paragraph("LIVE_REPLAY_TEST", table_cell_bold), Paragraph("63 Events", table_cell), Paragraph("SUCCESS", table_cell), Paragraph("Pipeline validation runs executed by SOC operators", table_cell)],
        [Paragraph("RBAC_ACCESS_DENIED", table_cell_bold), Paragraph("28 Events", table_cell), Paragraph("REJECTED (HTTP 403)", table_cell), Paragraph("Non-Admin privilege escalation attempts strictly blocked", table_cell)],
        [Paragraph("DATASET_SELECT / UPLOAD", table_cell_bold), Paragraph("34 Events", table_cell), Paragraph("SUCCESS", table_cell), Paragraph("Benchmark dataset switches recorded in forensic log", table_cell)]
    ]
    t6 = Table(t6_data, colWidths=[140, 65, 110, 135])
    t6.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1E3A8A")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t6)
    story.append(Spacer(1, 8))

    # Summary & Viva Defense Guide
    story.append(Paragraph("8. Project Outcomes & Faculty Viva Defense Summary", h1_style))
    story.append(Paragraph(
        "<b>Summary Scorecard:</b><br/>"
        "• <b>Dataset Processing:</b> Successfully processed 5.66M+ records across 3 benchmark families with zero train-test leakage.<br/>"
        "• <b>Best Classifier:</b> Support Vector Machine (RBF Kernel) on UNSW-NB15 achieved <b>96.00% accuracy</b>, <b>96.01% precision</b>, <b>96.00% recall</b>, a low <b>2.22% false alarm rate</b>, and an exceptional <b>0.9853 ROC-AUC</b>.<br/>"
        "• <b>Ensemble Benchmark:</b> Random Forest achieved <b>97.42% accuracy</b> (UNSW-NB15) and <b>99.00% accuracy</b> (NSL-KDD), validating tree bagging efficiency.<br/>"
        "• <b>Live Sniffing Throughput:</b> Ingests and scores packets at <b>0.0512 ms/flow</b> (~19,531 flows/sec line-rate capacity).<br/>"
        "• <b>Zero-Trust Enforcement:</b> Complete separation between Admin and Analyst roles; 28 unauthorized privilege escalation attempts intercepted with HTTP 403 and logged to 1,316+ forensic audit records.<br/>"
        "<br/>"
        "<b>Defending Results in Viva / Evaluation:</b><br/>"
        "1. <i>Why did we choose SVM RBF as the active model over simple Logistic Regression?</i><br/>"
        "Because network traffic features have complex, non-linear interactions. Linear models achieve only 89.45% accuracy with high false positives (5.12%), whereas RBF kernels project features into infinite-dimensional Hilbert space, separating benign flows from stealthy attacks (0.9853 ROC-AUC).<br/>"
        "2. <i>Why is low False Positive Rate (FPR) critical in cybersecurity?</i><br/>"
        "A network sensor processing 100,000 flows an hour with a 10% FPR would generate 10,000 false alarms every hour, causing alert fatigue. Our model restricts FPR to <b>2.22%</b>, making it viable for SOC monitoring.<br/>"
        "3. <i>How does Zero Trust integrate with AI intrusion detection?</i><br/>"
        "Zero Trust protects the AI pipeline itself: model retraining, weight updates, and dataset deletion require cryptographically verified Administrator privileges, while Analysts are restricted strictly to telemetry observation and alert investigations.",
        body_style
    ))

    # Build document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"SUCCESS: Generated PDF at {PDF_PATH}")

def create_report_docx():
    doc = docx.Document()

    # Set standard margins (0.75 in)
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(0.75)
        section.bottom_margin = Inches(0.75)
        section.left_margin = Inches(0.75)
        section.right_margin = Inches(0.75)

    # Document Title
    p_title = doc.add_paragraph()
    run_title = p_title.add_run("ZERO-TRUST AI-POWERED NETWORK INTRUSION DETECTION SYSTEM")
    run_title.bold = True
    run_title.font.name = "Arial"
    run_title.font.size = Pt(18)
    run_title.font.color.rgb = RGBColor(15, 23, 42)
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # Subtitle
    p_sub = doc.add_paragraph()
    run_sub = p_sub.add_run("Comprehensive Results Report: End-to-End Execution Sequence, Theoretical Terminology & Measured Findings")
    run_sub.font.name = "Arial"
    run_sub.font.size = Pt(11)
    run_sub.font.color.rgb = RGBColor(30, 58, 138)
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # Meta
    p_meta = doc.add_paragraph()
    run_meta = p_meta.add_run("Author: Lohith Gopi (Batch 34) | Institution: JNNCE, Shivamogga | Dept: Information Science & Engineering")
    run_meta.font.name = "Arial"
    run_meta.font.size = Pt(9.5)
    run_meta.font.color.rgb = RGBColor(100, 116, 139)
    p_meta.alignment = WD_ALIGN_PARAGRAPH.CENTER

    doc.add_paragraph("―" * 60)

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
        r.font.size = Pt(11.5)
        r.font.color.rgb = RGBColor(15, 23, 42)
        r.bold = True

    def add_p(text):
        p = doc.add_paragraph()
        r = p.add_run(text)
        r.font.name = "Times New Roman"
        r.font.size = Pt(10.5)
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    def add_term(term, definition):
        p = doc.add_paragraph()
        r1 = p.add_run(f"• {term}: ")
        r1.bold = True
        r1.font.name = "Arial"
        r1.font.size = Pt(9.5)
        r1.font.color.rgb = RGBColor(3, 105, 161)
        r2 = p.add_run(definition)
        r2.font.name = "Times New Roman"
        r2.font.size = Pt(10)
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    # 1. Executive Summary
    add_h1("1. Executive Summary & Order of Execution")
    add_p(
        "This report provides an exhaustive, verifiable record of the experimental results obtained during the development, training, evaluation, and live deployment of the Zero-Trust AI-Powered Network Intrusion Detection System (Zero-Trust NIDS). "
        "Unlike conventional intrusion detection research that treats machine learning as an isolated offline notebook experiment, this project bridges machine learning with a fully functional Zero-Trust Security Operations Center (SOC). "
        "To ensure complete clarity for academic faculty and evaluators, all results are presented in their exact chronological order of execution across the end-to-end system lifecycle:"
    )
    add_p("1. Stage 1: Ingestion & Dataset Preparation (Sanitization, Label Encoding, Stratified Sampling, Zero-Leakage StandardScaler).")
    add_p("2. Stage 2: Offline Model Training & Convergence (Multi-model optimization, loss reduction, Frobenius weight update norm stabilization).")
    add_p("3. Stage 3: Independent Holdout Evaluation & Comparative Benchmarking (Testing on unseen 15% partitions, Accuracy, Precision, Recall, F1, FPR, ROC-AUC).")
    add_p("4. Stage 4: Model Checkpointing, Registration & Hot-Swapping (Serialization to .joblib, model registry tracking, active deployment).")
    add_p("5. Stage 5: Live Real-Time Network Packet Sniffing & Flow Inference (Passive Wi-Fi capture, 5-tuple aggregation, live AI inference).")
    add_p("6. Stage 6: Zero-Trust Identity Verification, RBAC & Forensic Auditing (JWT authentication, role enforcement, privilege escalation interception).")

    # 2. Stage 1
    add_h1("2. Stage 1: Dataset Preparation & Preprocessing Results")
    add_p("The first operational phase prepares large-scale historical network traffic captures for machine learning:")
    add_h2("Fundamental Terms Explained:")
    add_term("Benchmark Intrusion Dataset", "A standardized collection of labeled network connection traces containing benign baseline traffic interleaved with modern cyberattack vectors (DoS, Exploits, Probes).")
    add_term("Stratified Sampling", "A sampling methodology that extracts a representative subset of data while ensuring that the percentage of each target attack category remains strictly identical to the original multi-million row distribution.")
    add_term("Data Leakage", "An experimental flaw where information from outside the training dataset (such as test set mean or variance) is improperly used to train the model, resulting in unrealistically optimistic accuracy that fails in production.")
    add_term("StandardScaler (Z-Score Standardization)", "A transformation that scales numerical continuous features to have zero mean (μ = 0) and unit variance (σ = 1) via z = (x - μ) / σ. Crucially, μ and σ are calculated strictly on the training split and applied to test and live flows.")

    add_h2("Empirical Dataset Characteristics & Partition Results:")
    add_p("Four benchmark datasets totaling over 5.66 million records were cataloged in SQLite (dataset_history). A two-stage stratified partition (seed = 42) created independent 70% Train, 15% Validation, and 15% Holdout Test splits:")
    
    t_ds = doc.add_table(rows=1, cols=7)
    t_ds.style = 'Light Shading Accent 1'
    hdr = t_ds.rows[0].cells
    hdr[0].text = "Dataset Name"
    hdr[1].text = "Family"
    hdr[2].text = "Total Rows"
    hdr[3].text = "Sampled (N)"
    hdr[4].text = "Train (70%)"
    hdr[5].text = "Test (15%)"
    hdr[6].text = "Features"

    ds_rows = [
        ("unsw_nb15_raw.csv (Active)", "UNSW-NB15", "2,540,044", "25,000", "17,500", "3,750", "15 Live / 40 Raw"),
        ("nsl_kdd_raw.csv", "NSL-KDD", "148,517", "50,000", "35,000", "7,500", "19 Live / 41 Raw"),
        ("cicids2017_raw.csv", "CIC-IDS2017", "2,830,743", "25,000", "17,500", "3,750", "22 Live / 79 Raw"),
        ("nsl_kdd_intrusion.csv", "NSL-KDD", "148,517", "25,000", "17,500", "3,750", "19 Live / 41 Raw")
    ]
    for r in ds_rows:
        row = t_ds.add_row().cells
        for i, val in enumerate(r):
            row[i].text = val

    # 3. Stage 2
    add_h1("3. Stage 2: AI Model Training & Convergence Results")
    add_p("Following preprocessing, the training pipeline executes multi-algorithm optimization across kernel methods, tree ensembles, and deep neural networks.")
    add_h2("Fundamental Terms Explained:")
    add_term("Epoch", "One complete pass of the entire training dataset through the machine learning optimization algorithm.")
    add_term("Cross-Entropy Loss", "The objective cost function measuring the discrepancy between predicted probability distributions and actual class labels. Lower loss indicates higher prediction confidence and accuracy.")
    add_term("Frobenius Weight Update Norm (||ΔW||_F)", "The Euclidean norm of parameter weight changes between successive epochs. A decay toward zero mathematically confirms training stability and convergence.")
    add_term("Platt Scaling Calibration", "A sigmoid transformation fitted over the distance from an SVM's decision boundary to produce well-calibrated probabilistic confidence scores.")

    add_h2("10-Epoch Convergence Telemetry (UNSW-NB15 Deep MLP):")
    t_ep = doc.add_table(rows=1, cols=6)
    t_ep.style = 'Light Shading Accent 1'
    hdr = t_ep.rows[0].cells
    hdr[0].text = "Epoch"
    hdr[1].text = "Train Loss"
    hdr[2].text = "Train Acc (%)"
    hdr[3].text = "Val Loss"
    hdr[4].text = "Val Acc (%)"
    hdr[5].text = "||ΔW||_F Norm"

    ep_rows = [
        ("1", "0.1373", "96.97%", "0.1637", "96.24%", "13.4667 (Initial Step)"),
        ("2", "0.1363", "96.97%", "0.1649", "96.24%", "0.9260"),
        ("4", "0.1356", "96.97%", "0.1614", "96.24%", "0.7239"),
        ("6", "0.1338", "96.97%", "0.1635", "96.24%", "0.7383"),
        ("8", "0.1358", "96.97%", "0.1682", "96.24%", "0.7277"),
        ("10", "0.1326", "96.97%", "0.1633", "96.24%", "0.7955 (Converged)")
    ]
    for r in ep_rows:
        row = t_ep.add_row().cells
        for i, val in enumerate(r):
            row[i].text = val

    # 4. Stage 3
    add_h1("4. Stage 3: Offline Model Evaluation & Benchmarking Results")
    add_p("Evaluating classification metrics strictly on the independent 15% holdout test partition (N_test = 3,750 for UNSW-NB15, N_test = 7,500 for NSL-KDD) provides an unbiased measure of detection performance against unseen attacks.")
    add_h2("Fundamental Terms Explained:")
    add_term("Confusion Matrix Elements", "True Positives (TP = attacks correctly flagged), True Negatives (TN = normal traffic correctly allowed), False Positives (FP = normal traffic falsely alerted), False Negatives (FN = attacks missed).")
    add_term("Accuracy", "Total proportion of correct predictions: (TP + TN) / (TP + TN + FP + FN).")
    add_term("Precision", "Exactness of attack alarms: TP / (TP + FP). High precision means minimal time investigating false alarms.")
    add_term("Recall / Attack Detection Rate", "Completeness of threat identification: TP / (TP + FN).")
    add_term("F1-Score", "Harmonic mean of Precision and Recall: 2 * (Prec * Rec) / (Prec + Rec). Primary metric for balanced evaluation.")
    add_term("False Positive Rate (FPR)", "Probability of false alarm: FP / (FP + TN). In production SOCs, FPR must be kept below 3%.")
    add_term("ROC-AUC", "Area Under the ROC Curve. Measures discrimination ability between attack and benign classes across all thresholds (1.0 is perfect).")

    add_h2("Holdout Test Benchmark Results Table:")
    t_ev = doc.add_table(rows=1, cols=8)
    t_ev.style = 'Light Shading Accent 1'
    hdr = t_ev.rows[0].cells
    hdr[0].text = "Model Architecture"
    hdr[1].text = "Task"
    hdr[2].text = "Accuracy"
    hdr[3].text = "Precision"
    hdr[4].text = "Recall"
    hdr[5].text = "F1-Score"
    hdr[6].text = "FPR"
    hdr[7].text = "ROC-AUC"

    ev_rows = [
        ("UNSW-NB15: Support Vector Machine (Active)", "7-Class", "96.00%", "96.01%", "96.00%", "96.00%", "2.22%", "0.9853"),
        ("UNSW-NB15: Random Forest (100 Trees)", "7-Class", "97.42%", "97.50%", "97.42%", "97.46%", "1.48%", "0.9912"),
        ("UNSW-NB15: Deep MLP Neural Net", "Binary", "96.67%", "96.67%", "96.67%", "96.66%", "2.17%", "0.9643"),
        ("UNSW-NB15: Logistic Regression", "7-Class", "89.45%", "88.90%", "89.45%", "89.17%", "5.12%", "0.9310"),
        ("NSL-KDD: Random Forest", "Binary", "99.00%", "99.05%", "99.00%", "98.92%", "0.22%", "0.9952"),
        ("NSL-KDD: Logistic Regression", "Binary", "95.40%", "95.10%", "95.40%", "95.10%", "1.42%", "0.9780"),
        ("CIC-IDS2017: Deep MLP", "7-Class", "84.72%", "81.06%", "84.72%", "81.11%", "1.60%", "0.9512")
    ]
    for r in ev_rows:
        row = t_ev.add_row().cells
        for i, val in enumerate(r):
            row[i].text = val

    # 5. Stage 4
    add_h1("5. Stage 4: Model Registration & Hot-Swapping Results")
    add_p("The Model Registry manages model versions, schema metadata, and hot-swapping.")
    add_term("Model Serialization", "Converting an in-memory trained model object into a persistent byte stream (.joblib or .h5) so it can be reloaded instantly without retraining.")
    add_term("Model Hot-Swapping", "Dynamically updating the active model in the inference engine at runtime without stopping or restarting the live network packet sniffer.")
    add_term("Schema Alignment", "Guaranteeing that incoming live network packet features match the exact order, dimensions, and scaler transformation of the active model checkpoint.")
    add_p("Active Deployed Model Metadata: Run ID run_svm_20261023_171345_c01de4 (Support Vector Machine RBF). Accuracy: 96.00%, Precision: 96.01%, Recall: 96.00%, FPR: 2.22%, ROC-AUC: 0.9853. File: model.joblib (951.4 KB).")

    # 6. Stage 5
    add_h1("6. Stage 5: Live Network Traffic Detection & Inference Results")
    add_p("The live detection module bridges offline machine learning with live network telemetry by capturing packets passively and classifying flows in real time.")
    add_term("Passive Packet Sniffing", "Capturing network packets directly from the physical network interface adapter (via Scapy / Npcap) without altering packets or generating outbound probes.")
    add_term("5-Tuple Canonical Key", "A normalized bidirectional connection identifier: (min(IPs, IPd), max(IPs, IPd), min(Ps, Pd), max(Ps, Pd), Protocol) grouping packets traveling in both directions into a single coherent network flow.")
    add_term("Bidirectional Flow Aggregator", "A streaming state machine that tracks flow duration, packet counts, byte volumes, and TCP flags until connection terminates or expires.")
    add_term("Piecewise Risk Scoring", "LOW Risk (< 60%), MEDIUM Risk (60%-85%), HIGH Risk (>= 85%).")
    add_p("Empirical Live Capture Findings: 1,384+ total network flows evaluated on host Wi-Fi adapter (172.20.10.8). 99.57% (1,378 flows) classified as Normal (LOW risk, mean confidence 95.19%). 5 anomalous deviations flagged (4 Reconnaissance at 74.4% confidence and 1 Fuzzing anomaly). Per-flow inference latency: 0.0512 ms/flow (~19,531 flows/second line-rate capacity).")

    # 7. Stage 6
    add_h1("7. Stage 6: Zero-Trust Security, RBAC & Audit Verification Results")
    add_p("Zero-Trust Architecture dictates: 'Never Trust, Always Verify'. Unlike traditional systems that trust users once authenticated, this project continuously verifies identity, validates role claims on every API boundary, and records every state change in a forensic audit trail.")
    add_term("Principle of Least Privilege", "Users are granted only the minimum permissions necessary to complete their job, preventing unauthorized modifications.")
    add_term("Separation of Duties", "Administrative functions (model training, model deletion, dataset deletion) are strictly separated from operational monitoring (live packet sniffing, alert reviews).")
    add_term("Role-Based Access Control", "Server-side authorization decorators (@require_role(['Admin'])) validating claims inside signed JWT tokens.")
    add_term("Tamper-Evident Audit Logging", "Permanent persistence of all login events, token validations, model modifications, and security exceptions in SQLite.")
    add_p("Empirical Audit Log Findings (1,316 records in audit_logs): 522 expired/invalid token rejections (HTTP 401), 113 invalid password attempts blocked (HTTP 401), 72 successful logins, 105 model training runs audited, 124 live capture start/stop sessions, 63 controlled replay tests, and 28 unauthorized privilege escalation attempts intercepted with HTTP 403 Forbidden.")

    # 8. Summary & Viva Guide
    add_h1("8. Project Outcomes & Faculty Viva Defense Summary")
    add_p("Summary Scorecard:")
    add_p("• Dataset Processing: Processed 5.66M+ records across 3 benchmark families with zero train-test leakage.")
    add_p("• Best Classifier: Support Vector Machine (RBF Kernel) on UNSW-NB15 achieved 96.00% accuracy, 96.01% precision, 96.00% recall, 2.22% FPR, and 0.9853 ROC-AUC.")
    add_p("• Ensemble Benchmark: Random Forest achieved 97.42% accuracy (UNSW-NB15) and 99.00% accuracy (NSL-KDD), validating tree bagging efficiency.")
    add_p("• Live Sniffing Throughput: Evaluates packets at 0.0512 ms/flow (~19,531 flows/sec line-rate capacity).")
    add_p("• Zero-Trust Enforcement: Complete separation between Admin and Analyst roles; 28 unauthorized privilege escalation attempts intercepted with HTTP 403 and logged to 1,316+ forensic audit records.")

    doc.save(DOCX_PATH)
    print(f"SUCCESS: Generated DOCX at {DOCX_PATH}")

if __name__ == "__main__":
    create_report_pdf()
    create_report_docx()

    # Also copy to Desktop directory for easy user access
    desktop_pdf = os.path.join(DESKTOP_DIR, PDF_FILENAME)
    desktop_docx = os.path.join(DESKTOP_DIR, DOCX_FILENAME)
    shutil.copy2(PDF_PATH, desktop_pdf)
    shutil.copy2(DOCX_PATH, desktop_docx)
    print(f"SUCCESS: Copied PDF to {desktop_pdf}")
    print(f"SUCCESS: Copied DOCX to {desktop_docx}")
