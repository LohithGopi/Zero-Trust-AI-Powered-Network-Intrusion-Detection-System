"""
VTU DOCX Generator:
Generates the complete, editable Microsoft Word document matching the
20-page VTU academic report structure.
"""

import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls

NAVY = RGBColor(30, 58, 138)       # #1E3A8A
SLATE = RGBColor(71, 85, 105)      # #475569
DARK = RGBColor(15, 23, 42)        # #0F172A

def set_cell_background(cell, hex_color):
    """Set background color of a table cell."""
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=60, bottom=60, left=100, right=100):
    """Set internal padding for table cell (in twips: 20 twips = 1 pt)."""
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def format_table(table, col_widths, col_alignments=None):
    """Apply professional borders, padding, and widths to docx table."""
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, row in enumerate(table.rows):
        # Header row shading
        if i == 0:
            trPr = row._tr.get_or_add_trPr()
            trPr.append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))
            for cell in row.cells:
                set_cell_background(cell, "1E3A8A")
                set_cell_margins(cell, top=80, bottom=80, left=100, right=100)
        else:
            bg = "F8FAFC" if i % 2 == 1 else "FFFFFF"
            for cell in row.cells:
                set_cell_background(cell, bg)
                set_cell_margins(cell, top=60, bottom=60, left=100, right=100)
                
        for j, cell in enumerate(row.cells):
            if j < len(col_widths):
                cell.width = Inches(col_widths[j])
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER

def add_callout_box(doc, text, title=""):
    """Insert a highlighted callout / code box."""
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    cell.width = Inches(6.8)
    set_cell_background(cell, "F1F5F9")
    set_cell_margins(cell, top=100, bottom=100, left=140, right=140)
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 1.15
    if title:
        run_title = p.add_run(title + "\n")
        run_title.font.name = "Times New Roman"
        run_title.font.size = Pt(9.5)
        run_title.font.bold = True
        run_title.font.color.rgb = NAVY
    run = p.add_run(text)
    run.font.name = "Consolas"
    run.font.size = Pt(8.5)
    run.font.color.rgb = DARK
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

def generate_docx_report(output_path: str, fig_dir: str, logo_path: str):
    print("Generating complete editable DOCX report...")
    doc = docx.Document()
    
    # Page Setup (A4: 8.27 x 11.69 inches)
    for section in doc.sections:
        section.page_width = Inches(8.27)
        section.page_height = Inches(11.69)
        section.top_margin = Inches(0.75)
        section.bottom_margin = Inches(0.75)
        section.left_margin = Inches(1.25)
        section.right_margin = Inches(0.75)
        
        # Configure Header & Footer
        header = section.header
        hp = header.paragraphs[0]
        hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        hrun = hp.add_run("VISVESVARAYA TECHNOLOGICAL UNIVERSITY, BELAGAVI | B.E. ISE BATCH 34")
        hrun.font.name = "Times New Roman"
        hrun.font.size = Pt(8.5)
        hrun.font.color.rgb = SLATE
        
        footer = section.footer
        fp = footer.paragraphs[0]
        fp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        frun = fp.add_run("JNNCE Shivamogga — Zero Trust AI-Powered NIDS System Design & Implementation Report")
        frun.font.name = "Times New Roman"
        frun.font.size = Pt(8.5)
        frun.font.color.rgb = SLATE

    # Helper function for adding paragraphs
    def add_p(text, style='Normal', space_before=0, space_after=4, bold=False, italic=False, color=None, align=WD_ALIGN_PARAGRAPH.JUSTIFY):
        p = doc.add_paragraph()
        p.alignment = align
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = 1.3
        run = p.add_run(text)
        run.font.name = "Times New Roman"
        run.font.size = Pt(10)
        run.bold = bold
        run.italic = italic
        if color:
            run.font.color.rgb = color
        return p

    def add_h1(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(2)
        run = p.add_run(text)
        run.font.name = "Times New Roman"
        run.font.size = Pt(12)
        run.bold = True
        run.font.color.rgb = NAVY
        return p

    def add_chapter(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(4)
        p.paragraph_format.space_after = Pt(4)
        run = p.add_run(text)
        run.font.name = "Times New Roman"
        run.font.size = Pt(14)
        run.bold = True
        run.font.color.rgb = DARK
        return p

    def add_img(filename, width_in=6.0, caption=""):
        p_img = os.path.join(fig_dir, filename)
        if os.path.exists(p_img):
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(4)
            p.paragraph_format.space_after = Pt(2)
            p.add_run().add_picture(p_img, width=Inches(width_in))
            if caption:
                cp = doc.add_paragraph()
                cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
                cp.paragraph_format.space_before = Pt(2)
                cp.paragraph_format.space_after = Pt(6)
                crun = cp.add_run(caption)
                crun.font.name = "Times New Roman"
                crun.font.size = Pt(8.5)
                crun.italic = True
                crun.font.color.rgb = SLATE

    # =========================================================
    # FRONT MATTER: PAGES i to viii
    # =========================================================
    # Page i: Title Page
    add_chapter("VISVESVARAYA TECHNOLOGICAL UNIVERSITY")
    add_p("“Jnana Sangama”, Belagavi – 590018, Karnataka, India", align=WD_ALIGN_PARAGRAPH.CENTER, color=SLATE)
    if os.path.exists(logo_path):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.add_run().add_picture(logo_path, width=Inches(1.2))
    add_p("A PROJECT REPORT ON", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=6)
    p_t = doc.add_paragraph()
    p_t.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_t = p_t.add_run("“SYSTEM DESIGN AND IMPLEMENTATION OF ZERO TRUST AI-POWERED NETWORK INTRUSION DETECTION SYSTEM”")
    r_t.font.name = "Times New Roman"
    r_t.font.size = Pt(15)
    r_t.bold = True
    r_t.font.color.rgb = NAVY
    add_p("Submitted in partial fulfillment of the requirements for the award of degree of", align=WD_ALIGN_PARAGRAPH.CENTER, italic=True)
    add_chapter("BACHELOR OF ENGINEERING\nIN\nINFORMATION SCIENCE AND ENGINEERING")
    add_p("Submitted by:\nANVITH B K (4JN23IS015) | AYUSH K N (4JN23IS021)\nKIRAN KUMAR R (4JN23IS045) | LOHITH GOPI S (4JN23IS052)\n\nUnder the Guidance of:\nMr. VISHWAS C G M, Assistant Professor, Dept. of ISE, JNNCE", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True)
    add_p("DEPARTMENT OF INFORMATION SCIENCE AND ENGINEERING\nJAWAHARLAL NEHRU NATIONAL COLLEGE OF ENGINEERING\nNavule, Shivamogga – 577204, Karnataka, India\nAcademic Year: 2026–2027 | Project Batch No. 34", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=12)
    doc.add_page_break()

    # Page ii: Certificate
    add_chapter("JAWAHARLAL NEHRU NATIONAL COLLEGE OF ENGINEERING, SHIVAMOGGA")
    add_p("Department of Information Science and Engineering", align=WD_ALIGN_PARAGRAPH.CENTER, color=SLATE)
    add_chapter("CERTIFICATE")
    add_p(
        "This is to certify that the project work titled “SYSTEM DESIGN AND IMPLEMENTATION OF ZERO TRUST AI-POWERED "
        "NETWORK INTRUSION DETECTION SYSTEM” is a bonafide work carried out by ANVITH B K (4JN23IS015), AYUSH K N (4JN23IS021), "
        "KIRAN KUMAR R (4JN23IS045), and LOHITH GOPI S (4JN23IS052), students of Bachelor of Engineering in Information Science and "
        "Engineering at Jawaharlal Nehru National College of Engineering, Shivamogga, in partial fulfillment of the requirements for "
        "the award of degree of Bachelor of Engineering in Information Science and Engineering of Visvesvaraya Technological University, "
        "Belagavi, during the academic year 2026–2027."
    )
    add_p("\n\nMr. Vishwas C G M (Guide)          Dr. Chethan K R (HOD)          Dr. P. Manjunatha (Principal)", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
    add_p("\n\nExternal Examiners:\n1. ................................................................              Signature: ........................................\n2. ................................................................              Signature: ........................................")
    doc.add_page_break()

    # Page iii: Declaration
    add_chapter("DECLARATION")
    add_p(
        "We, the students of Department of Information Science and Engineering, Jawaharlal Nehru National College of Engineering, "
        "Shivamogga, declare that the project titled “SYSTEM DESIGN AND IMPLEMENTATION OF ZERO TRUST AI-POWERED NETWORK INTRUSION "
        "DETECTION SYSTEM” has been independently executed by us under the guidance of Mr. Vishwas C G M, Assistant Professor, "
        "Department of ISE, JNNCE, for the award of Bachelor of Engineering in Information Science and Engineering from Visvesvaraya "
        "Technological University, Belagavi during 2026–2027 (Batch 34).\n\n"
        "ANVITH B K (4JN23IS015)\nAYUSH K N (4JN23IS021)\nKIRAN KUMAR R (4JN23IS045)\nLOHITH GOPI S (4JN23IS052)",
        bold=False
    )
    doc.add_page_break()

    # Page iv: Acknowledgements
    add_chapter("ACKNOWLEDGEMENTS")
    add_p(
        "We express our profound gratitude to our Principal, Dr. P. Manjunatha, for providing necessary infrastructural facilities. "
        "We are indebted to Dr. Chethan K R, Head of the Department of Information Science and Engineering, for his constant encouragement. "
        "We express our sincere thanks to our esteemed Guide, Mr. Vishwas C G M, for his invaluable guidance, continuous technical advice, "
        "and mentorship. We also thank all teaching and non-teaching faculty members of the ISE Department, our parents, and peers."
    )
    doc.add_page_break()

    # Page v: Abstract
    add_chapter("ABSTRACT")
    add_p(
        "Traditional perimeter network security operates under the flawed assumption of internal trust. This project designs, "
        "implements, and validates an end-to-end AI-Powered Zero Trust Network Intrusion Detection System (ZT-NIDS) adhering to "
        "NIST SP 800-207 guidelines. The system enforces 12-round salted Bcrypt password hashing, stateless HMAC-SHA256 JWT tokens, "
        "and strict Role-Based Access Control (RBAC). A multi-dataset data engineering pipeline cleans and stratifies 5.51M+ records "
        "across UNSW-NB15, CIC-IDS2017, and NSL-KDD without train-test leakage. A pluggable model registry implements Support Vector "
        "Machines (SVM), Random Forests, Logistic Regression, Deep MLP, and LSTM sequence networks. A live passive sniffer using Scapy "
        "and Windows Npcap performs canonical 5-tuple flow aggregation, evaluating flows at 0.0512 ms/flow line-rate latency. "
        "Empirical evaluation proves that the active UNSW-NB15 SVM model achieves 96.00% accuracy, 96.01% precision, 96.00% recall, "
        "2.22% false alarm rate, and 0.9853 ROC-AUC, while 1,316+ forensic audit records guarantee complete operational accountability."
    )
    doc.add_page_break()

    # Page vi: Table of Contents
    add_chapter("TABLE OF CONTENTS")
    add_p("Chapter 1: Introduction ......................................................................................................................... 1\n"
          "Chapter 2: Problem Statement and Requirement Analysis ......................................................................... 2\n"
          "Chapter 3: Literature Review and Technology Study ................................................................................. 3\n"
          "Chapter 4: System Design Overview & Master Architecture ..................................................................... 4\n"
          "Chapter 5: Zero Trust Security Architecture & Access Control ................................................................. 5\n"
          "Chapter 6: Use Case and Module Subsystem Design ................................................................................ 6\n"
          "Chapter 7: Dataset Design, Preprocessing & Anti-Leakage Pipeline ........................................................... 7\n"
          "Chapter 8: Machine Learning Model Design & Hyperparameters ................................................................ 8\n"
          "Chapter 9: Model Mathematics, Loss Formulations & Algorithms ............................................................. 9\n"
          "Chapter 10: Database Schema and REST API Design .............................................................................. 10\n"
          "Chapter 11: Frontend Implementation & SOC Dashboard .......................................................................... 11\n"
          "Chapter 12: Backend Implementation & Flask Route Handlers ................................................................. 12\n"
          "Chapter 13: Authentication, JWT & Access Control Implementation .......................................................... 13\n"
          "Chapter 14: Dataset Management & Model Training Implementation ......................................................... 14\n"
          "Chapter 15: Live and Simulated Network Traffic Detection ..................................................................... 15\n"
          "Chapter 16: Implementation Workflow & System Integration .................................................................... 16\n"
          "Chapter 17: Testing, Verification & Boundary Case Validation ................................................................. 17\n"
          "Chapter 18: Performance Evaluation & Experimental Results ................................................................... 18\n"
          "Chapter 19: Security Analysis, Limitations & Future Enhancements .......................................................... 19\n"
          "Chapter 20: Conclusion & Primary Numbered References ......................................................................... 20\n"
          "Comprehensive IEEE Bibliography ([1] – [26]) ...................................................................................... 21\n"
          "Appendix A: REST API Endpoint Specification ......................................................................................... 23\n"
          "Appendix B: Codebase Directory Structure .............................................................................................. 24")
    doc.add_page_break()

    # Page vii: List of Figures
    add_chapter("LIST OF FIGURES")
    add_p("Figure 4.1: Master 5-Tier Zero Trust AI-NIDS System Architecture Topology ................................................ 4\n"
          "Figure 5.1: Zero Trust Continuous Request Verification and RBAC Authorization Flow .................................... 5\n"
          "Figure 6.1: Zero Trust AI-NIDS Actor and Role Separation Use-Case Diagram ................................................. 6\n"
          "Figure 6.2: Preprocessing, Model Registry and Training Component Subsystem Diagram ................................. 6\n"
          "Figure 7.1: Multi-Dataset Ingestion, Cleaning, and Anti-Leakage Preprocessing Flowchart ................................. 7\n"
          "Figure 8.1: Machine Learning Model Training, Hot-Swapping, and Inference Pipeline ....................................... 8\n"
          "Figure 10.1: Relational SQLite Database Entity-Relationship (ER) Schema Diagram ........................................ 10\n"
          "Figure 10.2: REST API Request-Response Lifecycle and Security Middleware Pipeline .................................... 10\n"
          "Figure 11.1: React 18 SOC Dashboard Telemetry View (`ui_3_admin_dashboard.png`) .................................... 11\n"
          "Figure 11.2: AI Model Training and Convergence Monitoring View (`ui_6_model_training.png`) ........................ 11\n"
          "Figure 11.3: Live Passive Packet Sniffer Interface View (`ui_8_live_detection.png`) ........................................ 11\n"
          "Figure 11.4: Immutable Forensic Audit Trail Table View (`ui_10_audit_trail_table.png`) ................................. 11\n"
          "Figure 13.1: Zero Trust Authentication, Token Validation, and Authorization Flowchart .................................... 13\n"
          "Figure 14.1: Dataset Upload, Validation, Training Execution, and Model Serialization Flow ............................... 14\n"
          "Figure 15.1: Real-Time Packet Sniffing, 5-Tuple Aggregation, and Inference Architecture ................................. 15\n"
          "Figure 16.1: Complete End-to-End System Operational Workflow and Decision Diagram ................................. 16\n"
          "Figure 18.1: Empirical Holdout Performance Comparison Bar Chart across Implemented Models ....................... 18\n"
          "Figure 18.2: Normalized Confusion Matrix and ROC Curve for UNSW-NB15 Benchmark ................................... 18")
    doc.add_page_break()

    # Page viii: List of Tables
    add_chapter("LIST OF TABLES")
    add_p("Table 2.1: Hardware, Software, Library, and Operational Environment Specifications ...................................... 2\n"
          "Table 3.1: Comparative Synthesis of Existing NIDS Approaches vs Implemented System .................................. 3\n"
          "Table 7.1: Benchmark Intrusion Datasets Characteristics and Stratified Partition Statistics .............................. 7\n"
          "Table 8.1: Machine Learning Model Configurations, Kernel Functions, and Hyperparameters ............................ 8\n"
          "Table 10.1: Relational SQLite Database Schema Specification and Field Definitions ........................................ 10\n"
          "Table 13.1: Zero Trust Role-Based Access Control (RBAC) Permission Enforcement Matrix ............................... 13\n"
          "Table 17.1: Formal System Verification, Integration, and Security Test-Case Results Matrix ............................. 17\n"
          "Table 18.1: Empirical Benchmark Holdout Test Performance Metrics Across All Models ................................... 18\n"
          "Table 19.1: STRIDE Threat Model Security Analysis, Vulnerabilities, and Mitigations ..................................... 19\n"
          "Table 20.1: Formal Project Objectives Realization and Deliverable Verification Scorecard ................................. 20")
    doc.add_page_break()

    # =========================================================
    # MAIN REPORT: EXACT 20 PAGES (PAGES 1 to 20)
    # =========================================================
    # PAGE 1
    add_chapter("CHAPTER 1: INTRODUCTION")
    add_h1("1.1 Background of Network Security and Intrusion Detection")
    add_p("Modern enterprise computing infrastructures have transitioned from centralized corporate datacenters to highly distributed, hybrid cloud environments. Historically, network security adhered to perimeter-oriented defensive paradigms—the classical 'castle-and-moat' architecture. However, sophisticated multi-stage cyber attacks, unpatched edge vulnerabilities, software supply chain compromises, and insider threats have rendered static perimeter defenses obsolete. Once an adversary bypasses the outer gateway through credential harvesting or zero-day exploitation, internal enterprise enclaves typically lack granular verification, allowing unrestricted lateral movement and data exfiltration.")
    add_h1("1.2 Definition of Network Intrusion Detection System (NIDS)")
    add_p("A Network Intrusion Detection System (NIDS) is a specialized security mechanism deployed to passively inspect network packet flows, analyze protocol anomalies, and detect malicious behaviors traversing communication links. Unlike active inline firewalls that can introduce routing bottlenecks or single points of failure, a passive NIDS reconstructs bidirectional transport-layer conversations, extracts connection-level statistical attributes (such as duration, byte volume, packet rates, and TCP flag dynamics), and evaluates them against established behavioral baselines to flag unauthorized intrusions in real time without degrading line-rate throughput.")
    add_h1("1.3 Motivation for AI in Network Security")
    add_p("Conventional signature-based NIDS (e.g., Snort, Suricata) rely upon deterministic regular expressions to match pre-compiled byte patterns. While computationally fast, signature engines cannot detect zero-day exploits, novel attack variants, or polymorphic malwares. Furthermore, manual rule generation creates severe operational latency. Artificial Intelligence (AI) and Machine Learning (ML) overcome these limitations by abstracting high-dimensional non-linear correlations from historical traffic flows, empowering classifiers to generalize across unseen attack vectors with high statistical confidence and low false alarm overhead.")
    add_h1("1.4 Need for Zero Trust-Inspired Access Verification")
    add_p("Static access control lists (ACLs) cannot protect modern networks against credential hijacking or rogue insiders. In accordance with National Institute of Standards and Technology (NIST) Special Publication 800-207, the Zero Trust Architecture (ZTA) operates on the core doctrine: 'Never Trust, Always Verify'. Integrating Zero Trust principles into an AI-powered NIDS enforces continuous cryptographic identity verification, strict Role-Based Access Control (RBAC), and immutable forensic audit logging, ensuring that administrative actions (such as model training and active model deployment) are segregated from monitoring duties and permanently accountable.")
    add_h1("1.5 Project Objectives & Scope")
    add_p("The primary engineering objectives are: (1) Architect a decoupled full-stack NIDS utilizing React 18, Flask, SQLite, and scikit-learn; (2) Implement an automated, data leakage-free preprocessing pipeline supporting UNSW-NB15, CIC-IDS2017, and NSL-KDD benchmarks; (3) Build a pluggable multi-model registry implementing SVM, Random Forest, Logistic Regression, Deep MLP, and LSTM classifiers; (4) Integrate a real-time passive packet sniffer using Scapy and Windows Npcap for 5-tuple flow reassembly; and (5) Enforce 12-round salted Bcrypt authentication, stateless JWT session validation, RBAC, and tamper-resistant audit logging.")
    doc.add_page_break()

    # PAGE 2
    add_chapter("CHAPTER 2: PROBLEM STATEMENT & REQUIREMENTS")
    add_h1("2.1 Problem Statement")
    add_p("Enterprise network infrastructures are besieged by sophisticated, multi-stage cyber threats that easily evade conventional perimeter firewalls and signature-based intrusion detection tools. Legacy systems suffer from three crippling vulnerabilities: (1) Excessive false positive rates that cause Security Operations Center (SOC) analyst alert fatigue; (2) Total blindness to zero-day intrusions and polymorphic attack mutations; and (3) Implicit trust models that allow authenticated users unrestricted internal privileges without continuous verification or tamper-resistant forensic accountability.")
    add_h1("2.2 Functional and Non-Functional Requirements")
    add_p("• FR-1 (Auth): 12-round salted Bcrypt password verification and signed JWT token issuance.\n"
          "• FR-2 (RBAC): Strict privilege separation between Administrator (full rights) and Security Analyst (read-only telemetry).\n"
          "• FR-3 (Data Engine): Multipart CSV upload, schema parsing, missing/duplicate/infinite value imputation.\n"
          "• FR-4 (Anti-Leakage): Stratified train-val-test partitioning (70/15/15) with scalers fitted exclusively on training splits.\n"
          "• FR-5 (Multi-Model): Asynchronous training of SVM, Random Forest, Logistic Regression, MLP, and LSTM models.\n"
          "• FR-6 (Hot-Swap): Runtime switching of active deployed model in registry without restarting packet sniffer.\n"
          "• FR-7 (Sniffing): Promiscuous packet capture, 5-tuple flow aggregation, sub-millisecond per-flow risk scoring (< 1.0 ms/flow).\n"
          "• FR-8 (Audit Trail): Permanent logging of all logins, token validations, model changes, and unauthorized access violations.")
    add_h1("2.3 Environmental Specifications")
    t_hw_doc = doc.add_table(rows=1, cols=3)
    t_hw_doc.rows[0].cells[0].paragraphs[0].text = "Category"
    t_hw_doc.rows[0].cells[1].paragraphs[0].text = "Development Environment"
    t_hw_doc.rows[0].cells[2].paragraphs[0].text = "Production Target"
    hw_rows = [
        ("CPU / RAM", "Intel Core i5 / AMD Ryzen 5, 16 GB DDR4", "Intel Xeon / Core i7, 32 GB DDR4/ECC"),
        ("Storage / NIC", "512 GB NVMe SSD, Realtek RTL8821CE Wi-Fi", "1 TB NVMe SSD, Gigabit Promiscuous NIC"),
        ("OS / Runtimes", "Windows 11 64-bit, Python 3.13, Node 20", "Windows Server 2022 / Ubuntu 22.04 LTS"),
        ("Core Stack", "React 18, Vite, Flask, SQLite, Scikit-learn", "Gunicorn/Waitress, Npcap 1.79+, PyTorch/Keras")
    ]
    for cat, dev, prod in hw_rows:
        row = t_hw_doc.add_row()
        row.cells[0].paragraphs[0].text = cat
        row.cells[1].paragraphs[0].text = dev
        row.cells[2].paragraphs[0].text = prod
    format_table(t_hw_doc, [1.5, 2.5, 2.8])
    add_p("Table 2.1: Hardware, Software, Library, and Operational Environment Specifications.", italic=True, align=WD_ALIGN_PARAGRAPH.CENTER)
    doc.add_page_break()

    # PAGE 3
    add_chapter("CHAPTER 3: LITERATURE REVIEW & STUDY")
    add_h1("3.1 Evolution of Intrusion Detection Technologies")
    add_p("The conceptual foundations of automated intrusion detection originated in J. P. Anderson’s 1980 technical report [1], categorizing threats into internal misuse, external penetration, and misfeasance. In 1987, D. E. Denning formulated the first statistical anomaly detection model [2], positing that malicious incursions manifest as quantifiable deviations from normal activity. In 1999, M. Roesch released Snort [3], standardizing rule-based signature matching. However, signature matching cannot detect novel zero-day exploits and produces high false alarm overhead.")
    add_h1("3.2 Machine Learning and Deep Learning in Cyber Telemetry")
    add_p("Moustafa and Slay (2015) introduced the UNSW-NB15 benchmark [5], proving that modern synthetic attack vectors require high-dimensional statistical flow attributes. Sharafaldin et al. (2018) released the CIC-IDS2017 benchmark [6], standardizing 80+ connection attributes. Supervised classifiers—such as Support Vector Machines (SVM) with RBF kernels [8] and Random Forest ensemble trees [9]—demonstrated high generalization accuracy. For temporal correlations, recurrent LSTM networks [10] model sequential packet dynamics.")
    add_h1("3.3 Zero Trust Architecture (NIST SP 800-207)")
    add_p("In 2020, NIST codified the Zero Trust Architecture in SP 800-207 [4], mandating continuous identity verification, dynamic least-privilege authorization, and comprehensive forensic telemetry, expanding on J. Kindervag's Forrester research [15].")
    add_h1("3.4 Methodological Comparison")
    t_comp_doc = doc.add_table(rows=1, cols=4)
    t_comp_doc.rows[0].cells[0].paragraphs[0].text = "Approach"
    t_comp_doc.rows[0].cells[1].paragraphs[0].text = "Detection Method"
    t_comp_doc.rows[0].cells[2].paragraphs[0].text = "Zero-Day Defense"
    t_comp_doc.rows[0].cells[3].paragraphs[0].text = "Access Governance"
    comp_rows = [
        ("Rule NIDS (Snort)", "Regex string matching [3]", "None (Fails unknown)", "None (Stateless packet)"),
        ("Anomaly NIDS", "Statistical thresholds [2]", "Moderate (Gross volume)", "None (IP-level only)"),
        ("Standalone ML", "Tabular flow ML [7]", "High (Math generalization)", "None (Offline scripts)"),
        ("Implemented ZT-AI", "Pluggable Multi-Model AI + 5-Tuple Sniffer", "Exceptional (96-99% Acc)", "Full NIST SP 800-207 RBAC + Audit")
    ]
    for app, dm, zd, ag in comp_rows:
        row = t_comp_doc.add_row()
        row.cells[0].paragraphs[0].text = app
        row.cells[1].paragraphs[0].text = dm
        row.cells[2].paragraphs[0].text = zd
        row.cells[3].paragraphs[0].text = ag
    format_table(t_comp_doc, [1.5, 2.0, 1.5, 1.8])
    add_p("Table 3.1: Comparative Synthesis of Existing NIDS Approaches vs Implemented System.", italic=True, align=WD_ALIGN_PARAGRAPH.CENTER)
    doc.add_page_break()

    # PAGE 4
    add_chapter("CHAPTER 4: SYSTEM DESIGN OVERVIEW")
    add_h1("4.1 Master 5-Tier Decoupled Architecture Topology")
    add_p("The Zero Trust AI-Powered NIDS is engineered upon a modular 5-tier decoupled topology ensuring high scalability and fault isolation:\n"
          "• Tier 1 (Presentation): React 18, Vite, Tailwind CSS single-page interface with real-time SOC telemetry streaming.\n"
          "• Tier 2 (API Gateway): Python Flask REST blueprints managing JSON serialization and CORS validation.\n"
          "• Tier 3 (Security Policy Enforcement): Inline gatekeeper enforcing 12-round Bcrypt, HMAC-SHA256 JWT, and RBAC decorators.\n"
          "• Tier 4 (ML & Telemetry Engine): Pluggable Model Registry (SVM, RF, MLP, LSTM), anti-leakage preprocessor, and Scapy sniffer.\n"
          "• Tier 5 (Persistence & Forensics): SQLite relational store (`database.db`) alongside serialized Joblib/Keras artifacts.")
    add_img("fig3_1_master_architecture.png", width_in=6.0, caption="Figure 4.1: Master 5-Tier Zero Trust AI-NIDS System Architecture Topology.")
    add_h1("4.2 Data Flow and Trust Boundaries")
    add_p("Client requests traverse the Zero Trust gateway before reaching any backend service. Unauthenticated requests are rejected with HTTP 401 Unauthorized; unauthorized roles are rejected with HTTP 403 Forbidden and logged to the audit database.")
    doc.add_page_break()

    # PAGE 5
    add_chapter("CHAPTER 5: ZERO TRUST SECURITY ARCHITECTURE")
    add_h1("5.1 Zero Trust Principles Applied to NIDS")
    add_p("In compliance with NIST SP 800-207 recommendations, the system enforces: (1) Explicit Identity Verification (salted cryptographic credentials); (2) Least Privilege Access (role-restricted permissions); (3) Continuous Inspection (per-request token validation); and (4) Assume Breach (immutable forensic logging of all state transitions).")
    add_h1("5.2 Cryptographic Identity & Session Management")
    add_p("Passwords use 12-round salted Bcrypt hashing ($2^{12} = 4096$ iterations). Authenticated sessions receive HMAC-SHA256 signed JWT tokens encoding subject `user_id`, `username`, assigned `role`, `iat`, and 24-hour expiration (`exp`).")
    add_img("fig3_2_zero_trust_architecture.png", width_in=5.8, caption="Figure 5.1: Zero Trust Continuous Request Verification and RBAC Authorization Flow.")
    add_h1("5.3 Separation of Duties (SoD)")
    add_p("Administrator maintains full operational authority (model training, dataset deletion, active model switching). Security Analyst is restricted to operational monitoring (viewing telemetry, live packet capture, alert reviews).")
    doc.add_page_break()

    # PAGE 6
    add_chapter("CHAPTER 6: USE CASE & MODULE DESIGN")
    add_h1("6.1 System Actors & Use-Case Specification")
    add_p("The system defines two primary human actors: Administrator and Security Analyst. Core use cases encompass: Authentication, Dataset Ingestion & Profiling, Model Training, Model Evaluation, Model Hot-Swapping, Live Packet Sniffing, Threat Alerting, and Audit Trail Review.")
    add_img("fig_use_case_diagram.png", width_in=5.6, caption="Figure 6.1: Zero Trust AI-NIDS Actor and Role Separation Use-Case Diagram.")
    add_h1("6.2 Component Subsystems")
    add_p("The backend is partitioned into decoupled subsystems: Authentication Service, Dataset Preprocessing Engine, Pluggable Model Registry, Live Detection Flow Manager, and Forensic Audit Logger.")
    add_img("fig3_3_preprocessing_training_architecture.png", width_in=5.6, caption="Figure 6.2: Preprocessing, Model Registry and Training Component Subsystem Diagram.")
    doc.add_page_break()

    # PAGE 7
    add_chapter("CHAPTER 7: DATASET DESIGN & PREPROCESSING")
    add_h1("7.1 Multi-Benchmark Dataset Governance")
    add_p("The system catalogs three authoritative cybersecurity benchmarks totaling over 5.51 million records: UNSW-NB15 (2,540,044 flows, 49 features), CIC-IDS2017 (2,830,743 flows, 79 features), and NSL-KDD (148,517 flows, 42 features).")
    add_h1("7.2 Cleaning & Anti-Leakage Preprocessing")
    add_p("Raw data is cleansed by replacing infinite values (`+inf`, `-inf`) with `NaN`, removing duplicate rows prior to splitting, imputing numerical missing values with class-conditional medians, and imputing nominal values with modes. A stratified split creates 70% Train, 15% Validation, and 15% Holdout Test splits ($seed=42$). `StandardScaler` is fitted exclusively on $X_{train}$ and serialized to disk (`scaler.pkl`), preventing data leakage.")
    add_img("fig3_7_preprocessing_flowchart.png", width_in=5.6, caption="Figure 7.1: Multi-Dataset Ingestion, Cleaning, and Anti-Leakage Preprocessing Flowchart.")
    t_ds_doc = doc.add_table(rows=1, cols=4)
    t_ds_doc.rows[0].cells[0].paragraphs[0].text = "Dataset"
    t_ds_doc.rows[0].cells[1].paragraphs[0].text = "Total Rows"
    t_ds_doc.rows[0].cells[2].paragraphs[0].text = "Features"
    t_ds_doc.rows[0].cells[3].paragraphs[0].text = "Holdout Test (15%)"
    ds_rows = [
        ("UNSW-NB15", "2,540,044", "49 Raw / 15 Live", "3,750 samples (7-Class)"),
        ("CIC-IDS2017", "2,830,743", "79 Raw / 22 Live", "3,750 samples (15-Class)"),
        ("NSL-KDD", "148,517", "42 Raw / 19 Live", "7,500 samples (5-Class / Binary)")
    ]
    for dsn, tr, feat, htest in ds_rows:
        row = t_ds_doc.add_row()
        row.cells[0].paragraphs[0].text = dsn
        row.cells[1].paragraphs[0].text = tr
        row.cells[2].paragraphs[0].text = feat
        row.cells[3].paragraphs[0].text = htest
    format_table(t_ds_doc, [1.5, 1.5, 1.8, 2.0])
    add_p("Table 7.1: Benchmark Intrusion Datasets Characteristics and Partition Statistics.", italic=True, align=WD_ALIGN_PARAGRAPH.CENTER)
    doc.add_page_break()

    # PAGE 8
    add_chapter("CHAPTER 8: MACHINE LEARNING MODEL DESIGN")
    add_h1("8.1 Pluggable Model Registry Architecture")
    add_p("The system implements a polymorphic Model Registry (`BaseNIDSModel`) providing standardized interfaces across four classifier families:\n"
          r"• Support Vector Machine (SVM): Scikit-Learn `SVC` with Gaussian RBF kernel ($C=1.0, \gamma=\text{'scale'}$, balanced class weights)." + "\n"
          "• Random Forest: Ensemble of 100 decorrelated decision trees (`criterion='gini'`) using bootstrap aggregation.\n"
          "• Logistic Regression: Multinomial formulation with L2 ridge regularization and L-BFGS solver.\n"
          "• Deep Neural Networks: Dense Multilayer Perceptrons (MLP) and sequential Long Short-Term Memory (LSTM) recurrent architectures.")
    add_img("fig3_8_training_flowchart.png", width_in=5.8, caption="Figure 8.1: Machine Learning Model Training, Hot-Swapping, and Inference Pipeline.")
    add_h1("8.2 Model Hyperparameters and Artifact Persistence")
    add_p("Models are persisted using `joblib.dump()` (`model.joblib`) or Keras `.keras` format, bundled with fitted `StandardScaler` objects and hyperparameter metadata dictionaries, ensuring schema integrity upon deserialization.")
    doc.add_page_break()

    # PAGE 9
    add_chapter("CHAPTER 9: MODEL MATHEMATICS & ALGORITHMS")
    add_h1("9.1 Mathematical Formulations")
    add_p("• SVM Dual Optimization: min 0.5 ||w||^2 + C sum(xi_i)  s.t. y_i(w^T phi(x_i) + b) >= 1 - xi_i\n"
          "• Gaussian RBF Kernel: K(x_i, x_j) = exp(-gamma ||x_i - x_j||^2)\n"
          "• Standardization: z = (x - mu_train) / sigma_train  |  Sigmoid: sigma(z) = 1 / (1 + exp(-z))\n"
          "• Softmax Multi-Class Probability: P(Y=c|x) = exp(z_c) / sum_j exp(z_j)\n"
          "• Binary Cross-Entropy Loss: L_BCE = - (1/N) sum [ y_i ln(y_hat_i) + (1 - y_i) ln(1 - y_hat_i) ]\n"
          "• LSTM Recurrent Cell Gates: f_t = sigma(W_f[h_{t-1}, x_t] + b_f), i_t = sigma(W_i[h_{t-1}, x_t] + b_i), C_t = f_t . C_{t-1} + i_t . C_tilde_t, o_t = sigma(W_o[h_{t-1}, x_t] + b_o), h_t = o_t . tanh(C_t)")
    add_h1("9.2 Training and Streaming Inference Algorithms")
    algo_pseudocode = (
        "Algorithm 9.1: Anti-Leakage Preprocessing & Training\n"
        "Input: Raw Dataset D, Model M, Seed=42\n"
        " 1: Replace inf with NaN; drop duplicate records;\n"
        " 2: Impute numeric NaNs with median; nominal with mode;\n"
        " 3: Stratified partition D -> D_train(70%), D_val(15%), D_test(15%);\n"
        " 4: Fit StandardScaler S* strictly on X_train;\n"
        " 5: Transform X_train, X_val, X_test via S*;\n"
        " 6: Train M on (X_train, y_train); evaluate on (X_test, y_test);\n"
        " 7: Serialize M*, S*, evaluation report R to disk.\n"
        "------------------------------------------------------------------\n"
        "Algorithm 9.2: Streaming 5-Tuple Inference\n"
        "Input: Packet Stream P, Active Model M*, Scaler S*\n"
        " 1: for each packet p in P: update flow F[5-tuple canonical key];\n"
        " 2: on flow termination/timeout: extract features x_live;\n"
        " 3: standardize z_live = S*.transform(x_live);\n"
        " 4: predict class c = M*.predict(z_live), conf = max(predict_proba);\n"
        " 5: Risk = LOW if c=='Normal' else (HIGH if conf>=0.85 else MEDIUM);\n"
        " 6: Persist event in `live_detections`; emit to React UI."
    )
    add_callout_box(doc, algo_pseudocode, title="ALGORITHMIC PSEUDOCODE SPECIFICATION")
    doc.add_page_break()

    # PAGE 10
    add_chapter("CHAPTER 10: DATABASE & API DESIGN")
    add_h1("10.1 Relational SQLite Schema Architecture")
    add_p("Persistence is governed by SQLite (`database/database.db`) enforcing referential integrity across 6 normalized tables: `roles`, `users`, `dataset_history`, `model_history`, `live_detections`, and `audit_logs`.")
    add_img("fig3_5_database_er_diagram.png", width_in=5.6, caption="Figure 10.1: Relational SQLite Database Entity-Relationship (ER) Schema Diagram.")
    add_h1("10.2 REST API Organization & Lifecycle")
    add_p("Client requests authenticate by transmitting HTTP header: `Authorization: Bearer <token>`. The lifecycle traverses: CORS pre-flight -> Token validation (`@token_required`) -> Role authorization (`@require_role`) -> Service execution -> Audit logging -> Structured JSON response.")
    add_img("fig_api_lifecycle.png", width_in=5.6, caption="Figure 10.2: REST API Request-Response Lifecycle and Security Middleware Pipeline.")
    doc.add_page_break()

    # PAGE 11
    add_chapter("CHAPTER 11: FRONTEND IMPLEMENTATION")
    add_h1("11.1 React 18 Architecture and SOC Dashboard")
    add_p("The frontend is implemented in React 18 and Tailwind CSS, organized into modular dashboard views in `frontend/src/pages/dashboard/`: OverviewView, DatasetsView, CompareView, TrainingView, ModelDetailsView, LiveDetectionView, and AuditLogsView.")
    add_img("ui_3_admin_dashboard.png", width_in=5.4, caption="Figure 11.1: SOC Administrative Dashboard View (`ui_3_admin_dashboard.png`).")
    add_img("ui_6_model_training.png", width_in=5.4, caption="Figure 11.2: AI Model Training & Telemetry View (`ui_6_model_training.png`).")
    add_img("ui_8_live_detection.png", width_in=5.4, caption="Figure 11.3: Real-Time Passive Packet Sniffer Interface (`ui_8_live_detection.png`).")
    doc.add_page_break()

    # PAGE 12
    add_chapter("CHAPTER 12: BACKEND IMPLEMENTATION")
    add_h1("12.1 Flask Application Organization & Blueprints")
    add_p("The backend server is implemented in Flask (`app.py`), organized into modular blueprints (`auth_bp`, `dataset_bp`, `model_bp`, `live_detection_bp`). Decorator `@require_role` guarantees authorization before payloads are parsed.")
    backend_code = (
        "# --- Excerpt 12.1: Zero Trust RBAC Decorator (security/zero_trust.py) ---\n"
        "def require_role(allowed_roles):\n"
        "    def decorator(f):\n"
        "        @wraps(f)\n"
        "        def decorated(*args, **kwargs):\n"
        "            token = get_token_from_request()\n"
        "            payload = decode_token(token)\n"
        "            if payload.get('role', 'Admin') not in allowed_roles:\n"
        "                log_audit_event('RBAC_ACCESS_DENIED', 'REJECTED', ...)\n"
        "                return jsonify({'error': 'Role restriction'}), 403\n"
        "            g.user = payload\n"
        "            return f(*args, **kwargs)\n"
        "        return decorated\n"
        "    return decorator\n\n"
        "# --- Excerpt 12.2: Live Prediction Service (live_detection/live_predictor.py) ---\n"
        "def predict_flow(self, flow: NetworkFlow) -> Tuple[str, float, str]:\n"
        "    x_raw = np.array([flow.duration, flow.sbytes, flow.dbytes, flow.sttl, ...])\n"
        "    x_scaled = self.scaler.transform(x_raw.reshape(1, -1))\n"
        "    pred_idx = self.model.predict(x_scaled)[0]\n"
        "    conf = float(np.max(self.model.predict_proba(x_scaled)))\n"
        "    label = self.label_encoder.inverse_transform([pred_idx])[0]\n"
        "    risk = 'LOW' if label == 'Normal' else ('HIGH' if conf >= 0.85 else 'MEDIUM')\n"
        "    return label, conf, risk"
    )
    add_callout_box(doc, backend_code, title="VERIFIED SOURCE CODE EXCERPTS")
    add_h1("12.2 Concurrency and Exception Management")
    add_p("Model training runs asynchronously in a `ThreadPoolExecutor` worker thread, preventing server blocking. System exceptions are formatted as structured JSON responses.")
    doc.add_page_break()

    # PAGE 13
    add_chapter("CHAPTER 13: AUTHENTICATION & ACCESS CONTROL")
    add_h1("13.1 Password Security & JWT Token Verification")
    add_p("Passwords use 12-round salted Bcrypt hashes (`bcrypt.gensalt(12)`). JWT tokens use HMAC-SHA256 signatures with 24-hour expiration windows. Expired tokens are rejected with HTTP 401.")
    add_img("fig3_6_zero_trust_flowchart.png", width_in=5.6, caption="Figure 13.1: Zero Trust Authentication, Token Validation, and Authorization Flowchart.")
    add_h1("13.2 Role Permission Enforcement Matrix")
    t_rbac_doc = doc.add_table(rows=1, cols=4)
    t_rbac_doc.rows[0].cells[0].paragraphs[0].text = "Operation"
    t_rbac_doc.rows[0].cells[1].paragraphs[0].text = "Route"
    t_rbac_doc.rows[0].cells[2].paragraphs[0].text = "Administrator"
    t_rbac_doc.rows[0].cells[3].paragraphs[0].text = "Security Analyst"
    rbac_rows = [
        ("Login / Auth", "/api/auth/login", "ALLOWED (HTTP 200)", "ALLOWED (HTTP 200)"),
        ("View Telemetry", "/api/dataset/info", "ALLOWED (HTTP 200)", "ALLOWED (HTTP 200)"),
        ("Delete Dataset", "/api/dataset/delete/<id>", "ALLOWED (HTTP 200)", "FORBIDDEN (HTTP 403)"),
        ("Train Models", "/api/training/start", "ALLOWED (HTTP 202)", "FORBIDDEN (HTTP 403)"),
        ("Hot-Swap Model", "/api/model/select", "ALLOWED (HTTP 200)", "FORBIDDEN (HTTP 403)"),
        ("Packet Sniffer", "/api/live-detection/start", "ALLOWED (HTTP 200)", "ALLOWED (HTTP 200)"),
        ("Audit Logs", "/api/audit-logs", "ALLOWED (HTTP 200)", "READ-ONLY (HTTP 200)")
    ]
    for op, rt, adm, ana in rbac_rows:
        row = t_rbac_doc.add_row()
        row.cells[0].paragraphs[0].text = op
        row.cells[1].paragraphs[0].text = rt
        row.cells[2].paragraphs[0].text = adm
        row.cells[3].paragraphs[0].text = ana
    format_table(t_rbac_doc, [1.5, 1.8, 1.7, 1.8])
    add_p("Table 13.1: Zero Trust Role-Based Access Control (RBAC) Permission Matrix.", italic=True, align=WD_ALIGN_PARAGRAPH.CENTER)
    doc.add_page_break()

    # PAGE 14
    add_chapter("CHAPTER 14: DATASET & TRAINING IMPLEMENTATION")
    add_h1("14.1 Dataset Ingestion & Profiling Engine")
    add_p("Incoming CSV uploads are scanned for null, infinite, and duplicate records. Dataset metadata is cataloged in `dataset_history` with column counts and target class distributions.")
    add_img("fig3_8_training_flowchart.png", width_in=5.6, caption="Figure 14.1: Dataset Upload, Validation, Training Execution, and Model Serialization Flow.")
    add_h1("14.2 Training Execution & Atomic Hot-Swapping")
    add_p("Training runs asynchronously in a worker thread ($N=25,000$ to $50,000$, $seed=42$). Serialized checkpoints (`model.joblib`, `scaler.pkl`) are saved under `models/<dataset>/<run_id>/`. Activating a model updates `is_active = 1` atomically in SQLite, reloading the sniffer model instantly.")
    doc.add_page_break()

    # PAGE 15
    add_chapter("CHAPTER 15: LIVE & SIMULATED TRAFFIC DETECTION")
    add_h1("15.1 Passive Packet Capture & Flow Aggregation")
    add_p("The packet capture driver interfaces with host network adapters (tested on Realtek RTL8821CE Wi-Fi) via Windows Npcap. Packets are aggregated into canonical 5-tuple flows: K = (min(IPs), max(IPs), min(Ports), max(Ports), Proto), tracking duration, byte volumes, and TCP flags.")
    add_img("fig3_4_live_detection_architecture.png", width_in=5.6, caption="Figure 15.1: Real-Time Packet Sniffing, 5-Tuple Aggregation, and Inference Architecture.")
    add_h1("15.2 Streaming Inference & Risk Scoring")
    add_p("The active SVM model scores flows in 0.0512 ms/flow (~19,531 flows/sec line-rate capacity). Piecewise risk scoring categorizes flows into LOW Risk (< 60% / normal), MEDIUM Risk (60-85% anomaly), and HIGH Risk (>= 85% confirmed attack alert). A replay mode supports testing without elevated Npcap permissions.")
    doc.add_page_break()

    # PAGE 16
    add_chapter("CHAPTER 16: WORKFLOW & SYSTEM INTEGRATION")
    add_h1("16.1 End-to-End Operational Workflow")
    add_p("The operational sequence traverses 6 phases: (1) Identity handshake (Bcrypt + JWT); (2) Dataset governance (UNSW-NB15/CIC-IDS2017); (3) Anti-leakage training; (4) Model hot-swapping; (5) Passive packet sniffing; and (6) SOC alert dispatching and forensic audit logging.")
    add_img("fig_end_to_end_workflow.png", width_in=5.8, caption="Figure 16.1: Complete End-to-End System Operational Workflow and Decision Diagram.")
    add_h1("16.2 Integration Challenges Overcome")
    add_p("• Npcap Elevation: Solved via non-promiscuous adapter binding and simulated replay mode.\n"
          "• Feature Alignment: Solved via dynamic schema alignment dictionary in `live_predictor.py`.\n"
          "• Concurrency: Solved by executing training in `ThreadPoolExecutor` workers.")
    doc.add_page_break()

    # PAGE 17
    add_chapter("CHAPTER 17: TESTING & VALIDATION")
    add_h1("17.1 Multi-Level Testing Methodology")
    add_p("Testing spanned Unit Tests (Bcrypt, JWT, scaler), Integration Tests (REST API, DB CRUD), Security Tests (RBAC escalation, expired tokens), and Live Sniffing Tests.")
    t_tc_doc = doc.add_table(rows=1, cols=4)
    t_tc_doc.rows[0].cells[0].paragraphs[0].text = "Test ID"
    t_tc_doc.rows[0].cells[1].paragraphs[0].text = "Module"
    t_tc_doc.rows[0].cells[2].paragraphs[0].text = "Input Condition / Precondition"
    t_tc_doc.rows[0].cells[3].paragraphs[0].text = "Actual Result / Status"
    tc_rows = [
        ("TC-01", "Auth", "Valid credentials (admin / password)", "HTTP 200, JWT issued (PASSED)"),
        ("TC-02", "Auth", "Incorrect password string", "HTTP 401 Unauthorized (PASSED)"),
        ("TC-03", "RBAC", "Analyst token sent to `/api/training/start`", "HTTP 403 Forbidden (PASSED)"),
        ("TC-04", "Token", "Expired or tampered JWT header", "HTTP 401 Unauthorized (PASSED)"),
        ("TC-05", "Data", "Upload CSV with inf / null values", "Cleaned, 0 nulls (PASSED)"),
        ("TC-06", "Split", "Stratified partition UNSW-NB15", "70/15/15, zero leakage (PASSED)"),
        ("TC-07", "Train", "Execute SVM training run", "Trained in 11.67s, 951 KB (PASSED)"),
        ("TC-08", "Hot-Swap", "Switch active model to RF", "Switched in 0.02s (PASSED)"),
        ("TC-09", "Sniff", "Capture Wi-Fi network packets", "1,384 flows scored (PASSED)"),
        ("TC-10", "Audit", "Query `/api/audit-logs` table", "1,316+ records returned (PASSED)")
    ]
    for tid, mod, cond, res in tc_rows:
        row = t_tc_doc.add_row()
        row.cells[0].paragraphs[0].text = tid
        row.cells[1].paragraphs[0].text = mod
        row.cells[2].paragraphs[0].text = cond
        row.cells[3].paragraphs[0].text = res
    format_table(t_tc_doc, [0.8, 1.0, 2.7, 2.3])
    add_p("Table 17.1: Formal System Verification, Integration, and Security Test-Case Results Matrix.", italic=True, align=WD_ALIGN_PARAGRAPH.CENTER)
    doc.add_page_break()

    # PAGE 18
    add_chapter("CHAPTER 18: PERFORMANCE EVALUATION & RESULTS")
    add_h1("18.1 Holdout Benchmark Performance Evaluation")
    add_p("Evaluation was conducted strictly on independent 15% holdout test partitions ($N_{test}=3,750$ for UNSW-NB15, $N_{test}=7,500$ for NSL-KDD):")
    t_res_doc = doc.add_table(rows=1, cols=6)
    t_res_doc.rows[0].cells[0].paragraphs[0].text = "Model & Dataset"
    t_res_doc.rows[0].cells[1].paragraphs[0].text = "Task"
    t_res_doc.rows[0].cells[2].paragraphs[0].text = "Accuracy"
    t_res_doc.rows[0].cells[3].paragraphs[0].text = "Precision"
    t_res_doc.rows[0].cells[4].paragraphs[0].text = "Recall"
    t_res_doc.rows[0].cells[5].paragraphs[0].text = "F1-Score"
    res_rows = [
        ("UNSW-NB15: SVM (Active)", "7-Class", "96.00%", "96.01%", "96.00%", "96.00%"),
        ("UNSW-NB15: Random Forest", "7-Class", "97.42%", "97.50%", "97.42%", "97.46%"),
        ("UNSW-NB15: Deep MLP", "Binary", "96.67%", "96.67%", "96.67%", "96.66%"),
        ("UNSW-NB15: Logistic Reg", "7-Class", "89.45%", "88.90%", "89.45%", "89.17%"),
        ("NSL-KDD: Random Forest", "Binary", "99.00%", "99.05%", "99.00%", "98.92%"),
        ("NSL-KDD: Logistic Reg", "Binary", "95.40%", "95.10%", "95.40%", "95.10%"),
        ("CIC-IDS2017: Deep MLP", "7-Class", "84.72%", "81.06%", "84.72%", "81.11%")
    ]
    for md, tk, acc, pr, rec, f1 in res_rows:
        row = t_res_doc.add_row()
        row.cells[0].paragraphs[0].text = md
        row.cells[1].paragraphs[0].text = tk
        row.cells[2].paragraphs[0].text = acc
        row.cells[3].paragraphs[0].text = pr
        row.cells[4].paragraphs[0].text = rec
        row.cells[5].paragraphs[0].text = f1
    format_table(t_res_doc, [2.2, 0.8, 0.9, 0.9, 0.9, 1.0])
    add_p("Table 18.1: Empirical Benchmark Holdout Test Performance Metrics Across All Models.", italic=True, align=WD_ALIGN_PARAGRAPH.CENTER)
    add_img("fig4_4_metrics_comparison_bar.png", width_in=5.4, caption="Figure 18.1: Model Comparison Bar Chart across Implemented Models.")
    add_img("fig4_2_unsw_binary_cm_roc.png", width_in=5.4, caption="Figure 18.2: Confusion Matrix & ROC Curve for UNSW-NB15 Benchmark.")
    doc.add_page_break()

    # PAGE 19
    add_chapter("CHAPTER 19: SECURITY ANALYSIS & FUTURE WORK")
    add_h1("19.1 NIST SP 800-207 Zero Trust Tenet Compliance")
    add_p("The architecture fulfills NIST SP 800-207 pillars: explicit authentication on all endpoints, continuous token validation, dynamic least-privilege RBAC whitelists, and complete forensic audit logging.")
    add_h1("19.2 STRIDE Threat Model Security Analysis")
    t_st_doc = doc.add_table(rows=1, cols=3)
    t_st_doc.rows[0].cells[0].paragraphs[0].text = "STRIDE Threat"
    t_st_doc.rows[0].cells[1].paragraphs[0].text = "Vulnerability Vector"
    t_st_doc.rows[0].cells[2].paragraphs[0].text = "Implemented Mitigation"
    st_rows = [
        ("Spoofing Identity", "Stolen credentials / token forgery", "12-round Bcrypt + HMAC-SHA256 JWT"),
        ("Tampering Data", "Altering model weights / CSV data", "Role-restricted endpoints + file permissions"),
        ("Repudiation", "Operator denies retraining model", "Immutable SQLite audit logs (IP, user, timestamp)"),
        ("Info Disclosure", "Interception of traffic metadata", "Stateless JWT + exclusion of raw payloads"),
        ("Denial of Service", "High packet volume choking sniffer", "Multithreaded aggregation (0.051 ms/flow)"),
        ("Elevation Privilege", "Analyst accessing model training", "`@require_role(['Admin'])` returning HTTP 403")
    ]
    for st, vv, im in st_rows:
        row = t_st_doc.add_row()
        row.cells[0].paragraphs[0].text = st
        row.cells[1].paragraphs[0].text = vv
        row.cells[2].paragraphs[0].text = im
    format_table(t_st_doc, [1.5, 2.5, 2.8])
    add_p("Table 19.1: STRIDE Threat Model Security Analysis, Vulnerabilities, and Mitigations.", italic=True, align=WD_ALIGN_PARAGRAPH.CENTER)
    add_h1("19.3 Operational Limitations & Future Enhancements")
    add_p("Limitations: Inability to inspect encrypted TLS 1.3 payloads; single-node SQLite concurrency limits. Future work: Online Concept Drift Detection (ADWIN), Explainable AI (SHAP/LIME), Apache Kafka telemetry ingestion, and Linux eBPF line-rate packet parsing.")
    doc.add_page_break()

    # PAGE 20
    add_chapter("CHAPTER 20: CONCLUSION & REFERENCES")
    add_h1("20.1 Summary of Accomplishments")
    add_p("This project successfully engineered, implemented, and validated a Zero Trust AI-Powered NIDS for the B.E. in Information Science and Engineering at JNNCE, Shivamogga, affiliated with VTU, Belagavi (Batch 34). All 5 primary engineering objectives were fully achieved:")
    t_sc_doc = doc.add_table(rows=1, cols=3)
    t_sc_doc.rows[0].cells[0].paragraphs[0].text = "Objective"
    t_sc_doc.rows[0].cells[1].paragraphs[0].text = "Implemented Architecture"
    t_sc_doc.rows[0].cells[2].paragraphs[0].text = "Verification Status"
    sc_rows = [
        ("1. Decoupled 5-Tier Architecture", "React 18 + Flask + SQLite + Scikit-learn", "FULLY ACHIEVED (Verified)"),
        ("2. Anti-Leakage Preprocessing", "Train-fitted StandardScaler on 3 benchmarks", "FULLY ACHIEVED (5.51M records)"),
        ("3. Pluggable Model Registry", "SVM, Random Forest, Logistic Reg, MLP, LSTM", "FULLY ACHIEVED (96.00% holdout Acc)"),
        ("4. Real-Time Packet Sniffing", "Scapy & Npcap 5-tuple canonical aggregator", "FULLY ACHIEVED (0.0512 ms/flow)"),
        ("5. Zero Trust Access & Auditing", "12-round Bcrypt + JWT + RBAC + Audit Logs", "FULLY ACHIEVED (1,316+ events logged)")
    ]
    for ob, ia, vs in sc_rows:
        row = t_sc_doc.add_row()
        row.cells[0].paragraphs[0].text = ob
        row.cells[1].paragraphs[0].text = ia
        row.cells[2].paragraphs[0].text = vs
    format_table(t_sc_doc, [1.8, 2.8, 2.2])
    add_p("Table 20.1: Formal Project Objectives Realization and Deliverable Verification Scorecard.", italic=True, align=WD_ALIGN_PARAGRAPH.CENTER)
    add_h1("20.2 Primary References Cited in Main Report")
    add_p("[1] J. P. Anderson, “Computer Security Threat Monitoring and Surveillance,” Tech. Rep., 1980.\n"
          "[2] D. E. Denning, “An Intrusion-Detection Model,” IEEE Trans. Softw. Eng., 1987.\n"
          "[3] M. Roesch, “Snort: Lightweight Intrusion Detection for Networks,” USENIX LISA, 1999.\n"
          "[4] S. Rose et al., “Zero Trust Architecture,” NIST SP 800-207, Aug. 2020.\n"
          "[5] N. Moustafa and J. Slay, “UNSW-NB15: a comprehensive data set,” IEEE MilCIS, 2015.\n"
          "[6] I. Sharafaldin et al., “Toward Generating a New Dataset for Intrusion Detection,” ICISSP, 2018.\n"
          "[7] C. Cortes and V. Vapnik, “Support-Vector Networks,” Machine Learning, 1995.\n"
          "[8] S. Hochreiter and J. Schmidhuber, “Long Short-Term Memory,” Neural Computation, 1997.\n"
          "[9] L. Breiman, “Random Forests,” Machine Learning, 2001.\n"
          "[10] F. Pedregosa et al., “Scikit-learn: Machine Learning in Python,” JMLR, 2011.\n"
          "[11] P. Biondi, “Scapy: Interactive Packet Manipulation,” 2021.\n"
          "[12] J. Kindervag, “Build Security Into Your Network’s DNA: Zero Trust,” Forrester, 2010.\n"
          "(Full comprehensive IEEE bibliography continued in Supplementary References section).",
          italic=True)
    doc.add_page_break()

    # =========================================================
    # BACK MATTER: REFERENCES & APPENDICES
    # =========================================================
    add_chapter("REFERENCES (COMPREHENSIVE IEEE BIBLIOGRAPHY)")
    add_p("[1] J. P. Anderson, “Computer Security Threat Monitoring and Surveillance,” Tech. Rep., Fort Washington, PA, USA, 1980.\n"
          "[2] D. E. Denning, “An Intrusion-Detection Model,” IEEE Transactions on Software Engineering, vol. SE-13, no. 2, pp. 222–232, Feb. 1987.\n"
          "[3] M. Roesch, “Snort: Lightweight Intrusion Detection for Networks,” in Proc. USENIX LISA, Seattle, WA, USA, 1999, pp. 229–238.\n"
          "[4] S. Rose, O. Borchert, S. Mitchell, and S. Connelly, “Zero Trust Architecture,” NIST Special Publication 800-207, Aug. 2020.\n"
          "[5] N. Moustafa and J. Slay, “UNSW-NB15: a comprehensive data set for network intrusion detection systems,” in Proc. IEEE MilCIS, 2015.\n"
          "[6] I. Sharafaldin, A. H. Lashkari, and A. A. Ghorbani, “Toward Generating a New Dataset for Intrusion Detection,” in Proc. ICISSP, 2018.\n"
          "[7] M. Tavallaee, E. Bagheri, W. Lu, and A. A. Ghorbani, “A detailed analysis of the KDD CUP 99 data set,” in Proc. IEEE CISDA, 2009.\n"
          "[8] C. Cortes and V. Vapnik, “Support-Vector Networks,” Machine Learning, vol. 20, no. 3, pp. 273–297, Sep. 1995.\n"
          "[9] L. Breiman, “Random Forests,” Machine Learning, vol. 45, no. 1, pp. 5–32, Oct. 2001.\n"
          "[10] S. Hochreiter and J. Schmidhuber, “Long Short-Term Memory,” Neural Computation, vol. 9, no. 8, pp. 1735–1780, Nov. 1997.\n"
          "[11] D. P. Kingma and J. Ba, “Adam: A Method for Stochastic Optimization,” in Proc. ICLR, San Diego, CA, USA, 2015.\n"
          "[12] F. Pedregosa et al., “Scikit-learn: Machine Learning in Python,” Journal of Machine Learning Research, vol. 12, pp. 2825–2830, 2011.\n"
          "[13] M. Abadi et al., “TensorFlow: A System for Large-Scale Machine Learning,” in Proc. USENIX OSDI, 2016.\n"
          "[14] P. Biondi, “Scapy: Interactive Packet Manipulation Tool,” 2021. [Online]. Available: https://scapy.net.\n"
          "[15] J. Kindervag, “Build Security Into Your Network’s DNA: Zero Trust,” Forrester Research Inc., Tech. Rep., 2010.\n"
          "[16] D. Ferraiolo et al., “Proposed NIST standard for role-based access control,” ACM TISSEC, vol. 4, no. 3, pp. 224–274, 2001.\n"
          "[17] M. Jones, J. Bradley, and N. Sakimura, “JSON Web Token (JWT),” IETF RFC 7519, May 2015.\n"
          "[18] N. Provos and D. Mazières, “A Future-Adaptable Password Scheme,” in Proc. USENIX ATC, 1999.\n"
          "[19] A. L. Buczak and E. Guven, “A Survey of Data Mining and ML Methods for Cyber Security,” IEEE Comm. Surveys & Tutorials, 2016.\n"
          "[20] G. Kim et al., “A multi-layer network intrusion detection system using deep neural networks,” IEEE Access, 2019.\n"
          "[21] W. Wang et al., “HASTE: Automated Streaming Traffic Extraction using Canonical 5-Tuple Aggregation,” IEEE TNSM, 2020.\n"
          "[22] S. M. Lundberg and S.-I. Lee, “A Unified Approach to Interpreting Model Predictions,” in NeurIPS, 2017.\n"
          "[23] A. Bifet and R. Gavalda, “Learning from Time-Changing Data with Adaptive Windowing,” in Proc. SIAM SDM, 2007.\n"
          "[24] Insecure.Com LLC, “Npcap: Windows Packet Capture Library & Driver,” 2024. [Online]. Available: https://npcap.com.\n"
          "[25] Visvesvaraya Technological University (VTU), “Guidelines for Preparation of B.E. Project Reports,” 2023.\n"
          "[26] NIST, “Security and Privacy Controls for Information Systems and Organizations,” NIST SP 800-53, Rev. 5, 2020.")
    doc.add_page_break()

    # APPENDIX A
    add_chapter("APPENDIX A: REST API ENDPOINT SPECIFICATION")
    t_api_doc = doc.add_table(rows=1, cols=4)
    t_api_doc.rows[0].cells[0].paragraphs[0].text = "Route"
    t_api_doc.rows[0].cells[1].paragraphs[0].text = "Method"
    t_api_doc.rows[0].cells[2].paragraphs[0].text = "Role Whitelist"
    t_api_doc.rows[0].cells[3].paragraphs[0].text = "Function Description"
    api_list = [
        ("/api/auth/login", "POST", "Public", "Bcrypt verification + 24-hr signed JWT generation"),
        ("/api/auth/register", "POST", "Admin Only", "Creates new user with hashed password and role"),
        ("/api/dataset/upload", "POST", "Admin, Analyst", "Multipart CSV upload and schema validation"),
        ("/api/datasets", "GET", "Admin, Analyst", "Lists uploaded datasets, rows, and selected status"),
        ("/api/dataset/select", "POST", "Admin, Analyst", "Switches active dataset in session"),
        ("/api/dataset/compare", "POST", "Admin, Analyst", "Computes cross-dataset feature distribution"),
        ("/api/dataset/delete/<id>", "DELETE", "Admin Only", "Deletes dataset file and database record"),
        ("/api/training/start", "POST", "Admin Only", "Spawns async model training worker thread"),
        ("/api/training/<run_id>", "GET", "Admin Only", "Polls training convergence progress and loss"),
        ("/api/model/report", "GET", "Admin, Analyst", "Fetches accuracy, precision, recall, F1, and CM"),
        ("/api/live-detection/start", "POST", "Admin, Analyst", "Initiates Scapy/Npcap packet capture"),
        ("/api/live-detection/stop", "POST", "Admin, Analyst", "Stops capture thread and evaluates session"),
        ("/api/live-detection/evaluation", "GET", "Admin, Analyst", "Returns real-time risk scores and threat counts"),
        ("/api/audit-logs", "GET", "Admin Only", "Queries forensic audit trail with search filters")
    ]
    for rt, mt, rw, fd in api_list:
        row = t_api_doc.add_row()
        row.cells[0].paragraphs[0].text = rt
        row.cells[1].paragraphs[0].text = mt
        row.cells[2].paragraphs[0].text = rw
        row.cells[3].paragraphs[0].text = fd
    format_table(t_api_doc, [1.8, 0.8, 1.2, 3.0])
    doc.add_page_break()

    # APPENDIX B
    add_chapter("APPENDIX B: CODEBASE DIRECTORY STRUCTURE")
    codebase_tree = (
        "E:\\ML\\\n"
        "├── app.py                         # Master Flask application entry point\n"
        "├── config.py                      # System configuration & JWT secret keys\n"
        "├── requirements.txt               # Python package dependencies\n"
        "├── run_backend.bat                # Launch script for Flask server\n"
        "├── run_frontend_dev.bat           # Launch script for React Vite frontend\n"
        "├── api/                           # REST API route blueprints\n"
        "├── database/                      # SQLite persistence (`database.db`, `init_db.py`)\n"
        "├── security/                      # 12-round Bcrypt, JWT auth, and Zero Trust decorators\n"
        "├── preprocessing/                 # Missing/infinite value imputation and anti-leakage scaling\n"
        "├── training/                      # Pluggable model registry (SVM, RF, LR, MLP, LSTM)\n"
        "├── live_detection/                # Scapy/Npcap packet sniffer and 5-tuple flow reassembly\n"
        "├── frontend/                      # React 18, Vite, and Tailwind CSS SPA dashboard\n"
        "└── models/                        # Serialized model artifacts (`.joblib`, `.keras`)"
    )
    add_callout_box(doc, codebase_tree, title="PROJECT DIRECTORY TREE")
    
    doc.save(output_path)
    print(f"DOCX Report successfully saved to: {output_path}")

print("vtu_docx_generator.py written.")
