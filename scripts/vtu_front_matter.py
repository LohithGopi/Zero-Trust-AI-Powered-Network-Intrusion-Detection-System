"""
VTU Front Matter Builder (Pages i to viii)
Contains:
  Page i:    Official VTU & JNNCE Title Page
  Page ii:   Certificate of Evaluation
  Page iii:  Student Declaration
  Page iv:   Acknowledgements
  Page v:    Abstract
  Page vi:   Table of Contents
  Page vii:  List of Figures
  Page viii: List of Tables
"""

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle, PageBreak, Image, HRFlowable

def build_front_matter_story(styles, logo_path: str):
    story = []
    
    # -------------------------------------------------------------
    # PAGE i: TITLE PAGE
    # -------------------------------------------------------------
    story.append(Spacer(1, 10))
    story.append(Paragraph("VISVESVARAYA TECHNOLOGICAL UNIVERSITY", styles['VTUChapter']))
    story.append(Paragraph("“Jnana Sangama”, Belagavi – 590018, Karnataka, India", styles['VTUSubtitle']))
    story.append(Spacer(1, 12))
    
    if os.path.exists(logo_path):
        story.append(Image(logo_path, width=82, height=82))
    else:
        story.append(Spacer(1, 82))
        
    story.append(Spacer(1, 12))
    story.append(Paragraph("A PROJECT REPORT ON", styles['VTUSubtitle']))
    story.append(Spacer(1, 4))
    story.append(Paragraph("“SYSTEM DESIGN AND IMPLEMENTATION OF ZERO TRUST AI-POWERED NETWORK INTRUSION DETECTION SYSTEM”", styles['VTUTitle']))
    story.append(Spacer(1, 10))
    story.append(Paragraph("<i>Submitted in partial fulfillment of the requirements for the award of degree of</i>", styles['VTUSubtitle']))
    story.append(Paragraph("<b>BACHELOR OF ENGINEERING</b><br/>IN<br/><b>INFORMATION SCIENCE AND ENGINEERING</b>", styles['VTUChapter']))
    story.append(Spacer(1, 10))
    
    # Student and Guide Table
    team_data = [
        [Paragraph("<b>Submitted by:</b>", styles['VTUBodyBold']), Paragraph("<b>Under the Guidance of:</b>", styles['VTUBodyBold'])],
        [
            Paragraph("<b>ANVITH B K</b> (4JN23IS015)<br/>"
                      "<b>AYUSH K N</b> (4JN23IS021)<br/>"
                      "<b>KIRAN KUMAR R</b> (4JN23IS045)<br/>"
                      "<b>LOHITH GOPI S</b> (4JN23IS052)", styles['VTUBody']),
            Paragraph("<b>Mr. VISHWAS C G M</b><br/>"
                      "Assistant Professor<br/>"
                      "Dept. of Information Science & Engg.<br/>"
                      "JNNCE, Shivamogga", styles['VTUBody'])
        ]
    ]
    team_table = Table(team_data, colWidths=[240, 240])
    team_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(team_table)
    story.append(Spacer(1, 14))
    
    # Department / College Footer
    story.append(Paragraph("DEPARTMENT OF INFORMATION SCIENCE AND ENGINEERING", styles['VTUChapter']))
    story.append(Paragraph("<b>JAWAHARLAL NEHRU NATIONAL COLLEGE OF ENGINEERING</b>", styles['VTUBodyBold']))
    story.append(Paragraph("(Approved by AICTE, Affiliated to VTU Belagavi, Accredited by NBA & NAAC)", styles['VTUSubtitle']))
    story.append(Paragraph("Navule, Shivamogga – 577204, Karnataka, India<br/><b>Academic Year: 2026–2027 | Project Batch No. 34</b>", styles['VTUSubtitle']))
    story.append(PageBreak())

    # -------------------------------------------------------------
    # PAGE ii: CERTIFICATE OF EVALUATION
    # -------------------------------------------------------------
    story.append(Spacer(1, 10))
    story.append(Paragraph("JAWAHARLAL NEHRU NATIONAL COLLEGE OF ENGINEERING", styles['VTUChapter']))
    story.append(Paragraph("Navule, Shivamogga – 577204, Karnataka, India<br/>Department of Information Science and Engineering", styles['VTUSubtitle']))
    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#1E3A8A"), spaceBefore=4, spaceAfter=14))
    story.append(Paragraph("CERTIFICATE", styles['VTUTitle']))
    story.append(Spacer(1, 14))
    
    cert_text = (
        "This is to certify that the project work titled <b>“SYSTEM DESIGN AND IMPLEMENTATION OF ZERO TRUST "
        "AI-POWERED NETWORK INTRUSION DETECTION SYSTEM”</b> is a bonafide work carried out by <b>ANVITH B K (4JN23IS015), "
        "AYUSH K N (4JN23IS021), KIRAN KUMAR R (4JN23IS045), and LOHITH GOPI S (4JN23IS052)</b>, students of "
        "Bachelor of Engineering in Information Science and Engineering at Jawaharlal Nehru National College of Engineering, "
        "Shivamogga, in partial fulfillment of the requirements for the award of degree of <b>Bachelor of Engineering "
        "in Information Science and Engineering</b> of <b>Visvesvaraya Technological University (VTU), Belagavi</b>, during the "
        "academic year 2026–2027. It is certified that all suggestions indicated for Internal Assessment have been incorporated "
        "in this report deposited in the departmental library. The project report has been approved as it satisfies the academic "
        "requirements in respect of project work prescribed for the said degree."
    )
    story.append(Paragraph(cert_text, styles['VTUBody']))
    story.append(Spacer(1, 40))
    
    # Signature Table
    sig_data = [
        [
            Paragraph("<b>Mr. Vishwas C G M</b><br/>Guide, Assistant Professor<br/>Dept. of ISE, JNNCE", styles['VTUBody']),
            Paragraph("<b>Dr. Chethan K R</b><br/>Head of Department, Associate Professor<br/>Dept. of ISE, JNNCE", styles['VTUBody']),
            Paragraph("<b>Dr. P. Manjunatha</b><br/>Principal<br/>JNNCE, Shivamogga", styles['VTUBody'])
        ]
    ]
    sig_table = Table(sig_data, colWidths=[160, 160, 160])
    sig_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(sig_table)
    story.append(Spacer(1, 35))
    
    viva_data = [
        [Paragraph("<b>Name of Examiners</b>", styles['VTUBodyBold']), Paragraph("<b>Signature with Date</b>", styles['VTUBodyBold'])],
        [Paragraph("1. ............................................................................", styles['VTUBody']), Paragraph(".....................................................", styles['VTUBody'])],
        [Paragraph("2. ............................................................................", styles['VTUBody']), Paragraph(".....................................................", styles['VTUBody'])]
    ]
    viva_table = Table(viva_data, colWidths=[280, 200])
    viva_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(viva_table)
    story.append(PageBreak())

    # -------------------------------------------------------------
    # PAGE iii: DECLARATION
    # -------------------------------------------------------------
    story.append(Spacer(1, 15))
    story.append(Paragraph("DECLARATION", styles['VTUTitle']))
    story.append(Spacer(1, 18))
    
    decl_text = (
        "We, the undersigned students of the Department of Information Science and Engineering, Jawaharlal Nehru National College "
        "of Engineering, Shivamogga, hereby declare that the project work entitled <b>“SYSTEM DESIGN AND IMPLEMENTATION OF "
        "ZERO TRUST AI-POWERED NETWORK INTRUSION DETECTION SYSTEM”</b> has been independently executed by us under the "
        "guidance of <b>Mr. Vishwas C G M</b>, Assistant Professor, Department of Information Science and Engineering, JNNCE, "
        "Shivamogga, for the award of the degree of <b>Bachelor of Engineering in Information Science and Engineering</b> from "
        "<b>Visvesvaraya Technological University, Belagavi</b> during the academic batch 2023–2027 (Academic Year 2026–2027).<br/><br/>"
        "We further declare that this report has not previously formed the basis for the award of any degree, diploma, associateship, "
        "fellowship, or any other similar title to any university or institution. All materials, source codes, datasets, and intellectual "
        "contributions referenced in this work have been fully attributed in compliance with standard academic integrity guidelines."
    )
    story.append(Paragraph(decl_text, styles['VTUBody']))
    story.append(Spacer(1, 50))
    
    decl_table_data = [
        [Paragraph("<b>Place:</b> Shivamogga<br/><b>Date:</b> 28-10-2026", styles['VTUBodyBold']),
         Paragraph("<b>ANVITH B K</b> (USN: 4JN23IS015)<br/>"
                   "<b>AYUSH K N</b> (USN: 4JN23IS021)<br/>"
                   "<b>KIRAN KUMAR R</b> (USN: 4JN23IS045)<br/>"
                   "<b>LOHITH GOPI S</b> (USN: 4JN23IS052)", styles['VTUBody'])]
    ]
    decl_table = Table(decl_table_data, colWidths=[200, 280])
    decl_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(decl_table)
    story.append(PageBreak())

    # -------------------------------------------------------------
    # PAGE iv: ACKNOWLEDGEMENTS
    # -------------------------------------------------------------
    story.append(Spacer(1, 15))
    story.append(Paragraph("ACKNOWLEDGEMENTS", styles['VTUTitle']))
    story.append(Spacer(1, 14))
    
    ack_text = (
        "The satisfaction and euphoria that accompany the successful completion of any task would be incomplete without "
        "mentioning the individuals whose constant cooperation, guidance, and encouragement made it possible.<br/><br/>"
        "We express our deep sense of gratitude to our respected Principal, <b>Dr. P. Manjunatha</b>, for providing an "
        "inspiring academic atmosphere and granting the necessary computational infrastructure to carry out this project.<br/><br/>"
        "We are profoundly indebted to <b>Dr. Chethan K R</b>, Associate Professor and Head of the Department of Information Science "
        "and Engineering, for his invaluable encouragement, constructive feedback, and continuous support throughout the duration "
        "of our academic program.<br/><br/>"
        "We take immense pride and privilege in expressing our heartfelt gratitude to our esteemed Project Guide, "
        "<b>Mr. Vishwas C G M</b>, Assistant Professor, Department of Information Science and Engineering, for his exemplary guidance, "
        "scholarly insights, continuous technical supervision, and patience during every stage of design, implementation, and empirical "
        "validation.<br/><br/>"
        "We also extend our sincere thanks to the Project Coordinators and all the teaching and technical non-teaching staff members "
        "of the Department of Information Science and Engineering for their direct and indirect assistance.<br/><br/>"
        "Finally, we express our warmest affection and gratitude to our parents and friends for their constant moral encouragement, "
        "unconditional support, and belief in our abilities throughout our engineering tenure."
    )
    story.append(Paragraph(ack_text, styles['VTUBody']))
    story.append(Spacer(1, 30))
    story.append(Paragraph("<b>Project Batch No. 34:</b><br/>"
                           "Anvith B K, Ayush K N, Kiran kumar R, Lohith gopi S", styles['VTUBodyBold']))
    story.append(PageBreak())

    # -------------------------------------------------------------
    # PAGE v: ABSTRACT
    # -------------------------------------------------------------
    story.append(Spacer(1, 15))
    story.append(Paragraph("ABSTRACT", styles['VTUTitle']))
    story.append(Spacer(1, 14))
    
    abstract_text = (
        "Traditional perimeter-based network security models operate under the implicit assumption that internal network entities "
        "are inherently trustworthy. In contemporary enterprise infrastructures characterized by cloud-native microservices, "
        "hybrid remote endpoints, and advanced persistent threats (APTs), this legacy 'castle-and-moat' paradigm fails to prevent "
        "lateral movement, credential harvesting, and zero-day vulnerabilities. This project presents the comprehensive system design, "
        "architectural specification, and full-stack software implementation of an <b>AI-Powered Zero Trust Network Intrusion "
        "Detection System (ZT-NIDS)</b> adhering to National Institute of Standards and Technology (NIST) SP 800-207 guidelines.<br/><br/>"
        "The system enforces a rigorous 'never trust, always verify' paradigm by unifying cryptographic JSON Web Token (JWT) authentication, "
        "12-round salted Bcrypt password hashing, and strict Role-Based Access Control (RBAC) with dual-role Separation of Duties (SoD) "
        "between Administrators and Security Analysts. An automated, data leakage-free engineering pipeline ingests, cleans, imputes, and "
        "normalizes three benchmark intrusion datasets: <b>UNSW-NB15 (2.54M records)</b>, <b>CIC-IDS2017 (2.83M records)</b>, and "
        "<b>NSL-KDD (148.5K records)</b>. A pluggable machine learning registry implements Support Vector Machines (SVM with Gaussian RBF "
        "kernel), Random Forests (100 ensemble estimators), Multinomial Logistic Regression, Deep Multilayer Perceptrons (MLP), and "
        "Long Short-Term Memory (LSTM) recurrent neural networks.<br/><br/>"
        "To enable production security operations, a passive packet capture driver utilizing Scapy and Windows Npcap reassembles network "
        "packets into canonical bidirectional 5-tuple flows, extracting connection duration, byte volumes, packet counts, TCP flag ratios, "
        "and time-to-live metrics. Rigorous empirical validation proves that the active deployed classifier (UNSW-NB15 SVM) attains "
        "<b>96.00% classification accuracy, 96.01% precision, 96.00% recall, 96.00% F1-score, a 2.22% false alarm rate, and 0.9853 ROC-AUC</b> "
        "across a 7-class attack taxonomy on unseen holdout test data ($N_{test}=3,750$). Random Forest benchmarks achieve <b>97.42% accuracy</b> "
        "on UNSW-NB15 and <b>99.00% accuracy</b> on NSL-KDD. Streaming live inference operates at a sub-millisecond line-rate latency of "
        "<b>0.0512 ms per flow</b> (~19,531 flows/sec) across 1,384+ live Wi-Fi network flows. An immutable SQLite audit trail of 1,316+ "
        "forensic events verifies that 100% of unprivileged privilege escalation attempts (HTTP 403) and expired session tokens (HTTP 401) "
        "are intercepted, confirming that AI telemetry can be successfully synthesized with continuous Zero Trust access governance."
    )
    story.append(Paragraph(abstract_text, styles['VTUBody']))
    story.append(Spacer(1, 10))
    story.append(Paragraph("<b>Keywords:</b> Network Intrusion Detection System (NIDS), Zero Trust Architecture (ZTA), NIST SP 800-207, "
                           "Role-Based Access Control (RBAC), Support Vector Machine (SVM), Random Forest, UNSW-NB15, Live Packet Sniffing, Line-Rate Inference.", styles['VTUBodyBold']))
    story.append(PageBreak())

    # -------------------------------------------------------------
    # PAGE vi: TABLE OF CONTENTS
    # -------------------------------------------------------------
    story.append(Spacer(1, 10))
    story.append(Paragraph("TABLE OF CONTENTS", styles['VTUTitle']))
    story.append(Spacer(1, 10))
    
    toc_data = [
        [Paragraph("<b>Chapter / Section</b>", styles['VTUTableHeader']), Paragraph("<b>Title</b>", styles['VTUTableHeader']), Paragraph("<b>Page No.</b>", styles['VTUTableHeader'])],
        [Paragraph("", styles['VTUTableCellBold']), Paragraph("<b>Preliminary Pages (Certificate, Declaration, Abstract)</b>", styles['VTUTableCellBold']), Paragraph("i – viii", styles['VTUTableCellCenter'])],
        [Paragraph("<b>Chapter 1</b>", styles['VTUTableCellBold']), Paragraph("<b>Introduction & Project Objectives</b>", styles['VTUTableCellBold']), Paragraph("<b>1</b>", styles['VTUTableCellCenter'])],
        [Paragraph("<b>Chapter 2</b>", styles['VTUTableCellBold']), Paragraph("<b>Problem Statement and Requirement Analysis</b>", styles['VTUTableCellBold']), Paragraph("<b>2</b>", styles['VTUTableCellCenter'])],
        [Paragraph("<b>Chapter 3</b>", styles['VTUTableCellBold']), Paragraph("<b>Literature Review and Technology Study</b>", styles['VTUTableCellBold']), Paragraph("<b>3</b>", styles['VTUTableCellCenter'])],
        [Paragraph("<b>Chapter 4</b>", styles['VTUTableCellBold']), Paragraph("<b>System Design Overview & Master Architecture</b>", styles['VTUTableCellBold']), Paragraph("<b>4</b>", styles['VTUTableCellCenter'])],
        [Paragraph("<b>Chapter 5</b>", styles['VTUTableCellBold']), Paragraph("<b>Zero Trust Security Architecture & Access Control</b>", styles['VTUTableCellBold']), Paragraph("<b>5</b>", styles['VTUTableCellCenter'])],
        [Paragraph("<b>Chapter 6</b>", styles['VTUTableCellBold']), Paragraph("<b>Use Case and Module Subsystem Design</b>", styles['VTUTableCellBold']), Paragraph("<b>6</b>", styles['VTUTableCellCenter'])],
        [Paragraph("<b>Chapter 7</b>", styles['VTUTableCellBold']), Paragraph("<b>Dataset Design, Preprocessing & Anti-Leakage Pipeline</b>", styles['VTUTableCellBold']), Paragraph("<b>7</b>", styles['VTUTableCellCenter'])],
        [Paragraph("<b>Chapter 8</b>", styles['VTUTableCellBold']), Paragraph("<b>Machine Learning Model Design & Hyperparameters</b>", styles['VTUTableCellBold']), Paragraph("<b>8</b>", styles['VTUTableCellCenter'])],
        [Paragraph("<b>Chapter 9</b>", styles['VTUTableCellBold']), Paragraph("<b>Model Mathematics, Loss Formulations & Algorithms</b>", styles['VTUTableCellBold']), Paragraph("<b>9</b>", styles['VTUTableCellCenter'])],
        [Paragraph("<b>Chapter 10</b>", styles['VTUTableCellBold']), Paragraph("<b>Database Schema and REST API Design</b>", styles['VTUTableCellBold']), Paragraph("<b>10</b>", styles['VTUTableCellCenter'])],
        [Paragraph("<b>Chapter 11</b>", styles['VTUTableCellBold']), Paragraph("<b>Frontend Implementation & SOC Dashboard</b>", styles['VTUTableCellBold']), Paragraph("<b>11</b>", styles['VTUTableCellCenter'])],
        [Paragraph("<b>Chapter 12</b>", styles['VTUTableCellBold']), Paragraph("<b>Backend Implementation & Flask Route Handlers</b>", styles['VTUTableCellBold']), Paragraph("<b>12</b>", styles['VTUTableCellCenter'])],
        [Paragraph("<b>Chapter 13</b>", styles['VTUTableCellBold']), Paragraph("<b>Authentication, JWT & Access Control Implementation</b>", styles['VTUTableCellBold']), Paragraph("<b>13</b>", styles['VTUTableCellCenter'])],
        [Paragraph("<b>Chapter 14</b>", styles['VTUTableCellBold']), Paragraph("<b>Dataset Management & Model Training Implementation</b>", styles['VTUTableCellBold']), Paragraph("<b>14</b>", styles['VTUTableCellCenter'])],
        [Paragraph("<b>Chapter 15</b>", styles['VTUTableCellBold']), Paragraph("<b>Live and Simulated Network Traffic Detection</b>", styles['VTUTableCellBold']), Paragraph("<b>15</b>", styles['VTUTableCellCenter'])],
        [Paragraph("<b>Chapter 16</b>", styles['VTUTableCellBold']), Paragraph("<b>Implementation Workflow & System Integration</b>", styles['VTUTableCellBold']), Paragraph("<b>16</b>", styles['VTUTableCellCenter'])],
        [Paragraph("<b>Chapter 17</b>", styles['VTUTableCellBold']), Paragraph("<b>Testing, Verification & Boundary Case Validation</b>", styles['VTUTableCellBold']), Paragraph("<b>17</b>", styles['VTUTableCellCenter'])],
        [Paragraph("<b>Chapter 18</b>", styles['VTUTableCellBold']), Paragraph("<b>Performance Evaluation & Experimental Results</b>", styles['VTUTableCellBold']), Paragraph("<b>18</b>", styles['VTUTableCellCenter'])],
        [Paragraph("<b>Chapter 19</b>", styles['VTUTableCellBold']), Paragraph("<b>Security Analysis, Limitations & Future Enhancements</b>", styles['VTUTableCellBold']), Paragraph("<b>19</b>", styles['VTUTableCellCenter'])],
        [Paragraph("<b>Chapter 20</b>", styles['VTUTableCellBold']), Paragraph("<b>Conclusion & Primary Numbered References</b>", styles['VTUTableCellBold']), Paragraph("<b>20</b>", styles['VTUTableCellCenter'])],
        [Paragraph("", styles['VTUTableCellBold']), Paragraph("<b>Comprehensive IEEE Bibliography ([1] – [26])</b>", styles['VTUTableCellBold']), Paragraph("21 – 22", styles['VTUTableCellCenter'])],
        [Paragraph("", styles['VTUTableCellBold']), Paragraph("<b>Appendix A: Complete REST API Specification & Schemas</b>", styles['VTUTableCellBold']), Paragraph("23", styles['VTUTableCellCenter'])],
        [Paragraph("", styles['VTUTableCellBold']), Paragraph("<b>Appendix B: Codebase Directory & File Structure</b>", styles['VTUTableCellBold']), Paragraph("24", styles['VTUTableCellCenter'])]
    ]
    toc_table = Table(toc_data, colWidths=[80, 340, 60])
    toc_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1E3A8A")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(toc_table)
    story.append(PageBreak())

    # -------------------------------------------------------------
    # PAGE vii: LIST OF FIGURES
    # -------------------------------------------------------------
    story.append(Spacer(1, 10))
    story.append(Paragraph("LIST OF FIGURES", styles['VTUTitle']))
    story.append(Spacer(1, 10))
    
    lof_data = [
        [Paragraph("<b>Fig. No.</b>", styles['VTUTableHeader']), Paragraph("<b>Figure Title</b>", styles['VTUTableHeader']), Paragraph("<b>Page No.</b>", styles['VTUTableHeader'])],
        [Paragraph("Figure 4.1", styles['VTUTableCellBold']), Paragraph("Master 5-Tier Zero Trust AI-NIDS System Architecture Topology", styles['VTUTableCell']), Paragraph("4", styles['VTUTableCellCenter'])],
        [Paragraph("Figure 5.1", styles['VTUTableCellBold']), Paragraph("Zero Trust Continuous Request Verification and RBAC Authorization Flow", styles['VTUTableCell']), Paragraph("5", styles['VTUTableCellCenter'])],
        [Paragraph("Figure 6.1", styles['VTUTableCellBold']), Paragraph("Zero Trust AI-NIDS Actor and Role Separation Use-Case Diagram", styles['VTUTableCell']), Paragraph("6", styles['VTUTableCellCenter'])],
        [Paragraph("Figure 6.2", styles['VTUTableCellBold']), Paragraph("Preprocessing, Model Registry and Training Component Subsystem Diagram", styles['VTUTableCell']), Paragraph("6", styles['VTUTableCellCenter'])],
        [Paragraph("Figure 7.1", styles['VTUTableCellBold']), Paragraph("Multi-Dataset Ingestion, Cleaning, and Anti-Leakage Preprocessing Flowchart", styles['VTUTableCell']), Paragraph("7", styles['VTUTableCellCenter'])],
        [Paragraph("Figure 8.1", styles['VTUTableCellBold']), Paragraph("Machine Learning Model Training, Hot-Swapping, and Inference Pipeline", styles['VTUTableCell']), Paragraph("8", styles['VTUTableCellCenter'])],
        [Paragraph("Figure 10.1", styles['VTUTableCellBold']), Paragraph("Relational SQLite Database Entity-Relationship (ER) Schema Diagram", styles['VTUTableCell']), Paragraph("10", styles['VTUTableCellCenter'])],
        [Paragraph("Figure 10.2", styles['VTUTableCellBold']), Paragraph("REST API Request-Response Lifecycle and Security Middleware Pipeline", styles['VTUTableCell']), Paragraph("10", styles['VTUTableCellCenter'])],
        [Paragraph("Figure 11.1", styles['VTUTableCellBold']), Paragraph("React 18 SOC Dashboard Telemetry View (`ui_3_admin_dashboard.png`)", styles['VTUTableCell']), Paragraph("11", styles['VTUTableCellCenter'])],
        [Paragraph("Figure 11.2", styles['VTUTableCellBold']), Paragraph("AI Model Training and Convergence Monitoring View (`ui_6_model_training.png`)", styles['VTUTableCell']), Paragraph("11", styles['VTUTableCellCenter'])],
        [Paragraph("Figure 11.3", styles['VTUTableCellBold']), Paragraph("Live Passive Packet Sniffer Interface View (`ui_8_live_detection.png`)", styles['VTUTableCell']), Paragraph("11", styles['VTUTableCellCenter'])],
        [Paragraph("Figure 11.4", styles['VTUTableCellBold']), Paragraph("Immutable Forensic Audit Trail Table View (`ui_10_audit_trail_table.png`)", styles['VTUTableCell']), Paragraph("11", styles['VTUTableCellCenter'])],
        [Paragraph("Figure 13.1", styles['VTUTableCellBold']), Paragraph("Zero Trust Authentication, Token Validation, and Authorization Flowchart", styles['VTUTableCell']), Paragraph("13", styles['VTUTableCellCenter'])],
        [Paragraph("Figure 14.1", styles['VTUTableCellBold']), Paragraph("Dataset Upload, Validation, Training Execution, and Model Serialization Flow", styles['VTUTableCell']), Paragraph("14", styles['VTUTableCellCenter'])],
        [Paragraph("Figure 15.1", styles['VTUTableCellBold']), Paragraph("Real-Time Packet Sniffing, 5-Tuple Aggregation, and Inference Architecture", styles['VTUTableCell']), Paragraph("15", styles['VTUTableCellCenter'])],
        [Paragraph("Figure 16.1", styles['VTUTableCellBold']), Paragraph("Complete End-to-End System Operational Workflow and Decision Diagram", styles['VTUTableCell']), Paragraph("16", styles['VTUTableCellCenter'])],
        [Paragraph("Figure 18.1", styles['VTUTableCellBold']), Paragraph("Empirical Holdout Performance Comparison Bar Chart across Implemented Models", styles['VTUTableCell']), Paragraph("18", styles['VTUTableCellCenter'])],
        [Paragraph("Figure 18.2", styles['VTUTableCellBold']), Paragraph("Normalized Confusion Matrix and ROC Curve for UNSW-NB15 Benchmark", styles['VTUTableCell']), Paragraph("18", styles['VTUTableCellCenter'])]
    ]
    lof_table = Table(lof_data, colWidths=[70, 350, 60])
    lof_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1E3A8A")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
    ]))
    story.append(lof_table)
    story.append(PageBreak())

    # -------------------------------------------------------------
    # PAGE viii: LIST OF TABLES
    # -------------------------------------------------------------
    story.append(Spacer(1, 10))
    story.append(Paragraph("LIST OF TABLES", styles['VTUTitle']))
    story.append(Spacer(1, 10))
    
    lot_data = [
        [Paragraph("<b>Table No.</b>", styles['VTUTableHeader']), Paragraph("<b>Table Description</b>", styles['VTUTableHeader']), Paragraph("<b>Page No.</b>", styles['VTUTableHeader'])],
        [Paragraph("Table 2.1", styles['VTUTableCellBold']), Paragraph("Hardware, Software, Library, and Operational Environment Specifications", styles['VTUTableCell']), Paragraph("2", styles['VTUTableCellCenter'])],
        [Paragraph("Table 3.1", styles['VTUTableCellBold']), Paragraph("Comparative Synthesis of Existing NIDS Approaches vs Implemented System", styles['VTUTableCell']), Paragraph("3", styles['VTUTableCellCenter'])],
        [Paragraph("Table 7.1", styles['VTUTableCellBold']), Paragraph("Benchmark Intrusion Datasets Characteristics and Stratified Partition Statistics", styles['VTUTableCell']), Paragraph("7", styles['VTUTableCellCenter'])],
        [Paragraph("Table 8.1", styles['VTUTableCellBold']), Paragraph("Machine Learning Model Configurations, Kernel Functions, and Hyperparameters", styles['VTUTableCell']), Paragraph("8", styles['VTUTableCellCenter'])],
        [Paragraph("Table 10.1", styles['VTUTableCellBold']), Paragraph("Relational SQLite Database Schema Specification and Field Definitions", styles['VTUTableCell']), Paragraph("10", styles['VTUTableCellCenter'])],
        [Paragraph("Table 13.1", styles['VTUTableCellBold']), Paragraph("Zero Trust Role-Based Access Control (RBAC) Permission Enforcement Matrix", styles['VTUTableCell']), Paragraph("13", styles['VTUTableCellCenter'])],
        [Paragraph("Table 17.1", styles['VTUTableCellBold']), Paragraph("Formal System Verification, Integration, and Security Test-Case Results Matrix", styles['VTUTableCell']), Paragraph("17", styles['VTUTableCellCenter'])],
        [Paragraph("Table 18.1", styles['VTUTableCellBold']), Paragraph("Empirical Benchmark Holdout Test Performance Metrics Across All Models", styles['VTUTableCell']), Paragraph("18", styles['VTUTableCellCenter'])],
        [Paragraph("Table 19.1", styles['VTUTableCellBold']), Paragraph("STRIDE Threat Model Security Analysis, Vulnerabilities, and Mitigations", styles['VTUTableCell']), Paragraph("19", styles['VTUTableCellCenter'])],
        [Paragraph("Table 20.1", styles['VTUTableCellBold']), Paragraph("Formal Project Objectives Realization and Deliverable Verification Scorecard", styles['VTUTableCell']), Paragraph("20", styles['VTUTableCellCenter'])]
    ]
    lot_table = Table(lot_data, colWidths=[70, 350, 60])
    lot_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1E3A8A")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(lot_table)
    story.append(PageBreak())

    return story

print("vtu_front_matter.py written.")
