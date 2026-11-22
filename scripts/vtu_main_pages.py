"""
VTU Main Content Pages Builder (Pages 1 to 20)
Strictly engineered so that Page X occupies exactly physical Main Page X.
Each function returns a list of flowables terminating in PageBreak().
"""

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    Paragraph, Spacer, Table, TableStyle, PageBreak, Image, HRFlowable, Preformatted
)

def build_page_1(styles, fig_dir):
    """PAGE 1 — CHAPTER 1: INTRODUCTION"""
    story = []
    story.append(Paragraph("CHAPTER 1: INTRODUCTION", styles['VTUChapter']))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#1E3A8A"), spaceBefore=2, spaceAfter=8))
    
    story.append(Paragraph("1.1 Background of Network Security and Intrusion Detection", styles['VTUH1']))
    story.append(Paragraph(
        "Modern enterprise computing infrastructures have transitioned from centralized corporate datacenters to highly distributed, "
        "hybrid cloud environments comprising remote workers, microservices, and Internet of Things (IoT) endpoints. Historically, network "
        "security adhered to perimeter-oriented defensive paradigms—the classical 'castle-and-moat' architecture. In this paradigm, perimeter "
        "firewalls and virtual private network (VPN) gateways segregate untrusted public networks from trusted internal local area networks (LANs). "
        "However, sophisticated multi-stage cyber attacks, unpatched edge vulnerabilities, software supply chain compromises, and insider threats "
        "have rendered static perimeter defenses obsolete. Once an adversary bypasses the outer gateway through credential harvesting or zero-day "
        "exploitation, internal enterprise enclaves typically lack granular verification, allowing unrestricted lateral movement and data exfiltration.",
        styles['VTUBody']
    ))
    
    story.append(Paragraph("1.2 Definition of Network Intrusion Detection System (NIDS)", styles['VTUH1']))
    story.append(Paragraph(
        "A Network Intrusion Detection System (NIDS) is a specialized security mechanism deployed to passively inspect network packet flows, "
        "analyze protocol anomalies, and detect malicious behaviors traversing communication links. Unlike active inline firewalls that can "
        "introduce routing bottlenecks or single points of failure, a passive NIDS reconstructs bidirectional transport-layer conversations, "
        "extracts connection-level statistical attributes (such as duration, byte volume, packet rates, and TCP flag dynamics), and evaluates them "
        "against established behavioral baselines to flag unauthorized intrusions in real time without degrading line-rate throughput.",
        styles['VTUBody']
    ))
    
    story.append(Paragraph("1.3 Motivation for AI in Network Security", styles['VTUH1']))
    story.append(Paragraph(
        "Conventional signature-based NIDS (e.g., Snort, Suricata) rely upon deterministic regular expressions to match pre-compiled byte patterns. "
        "While computationally fast, signature engines cannot detect zero-day exploits, novel attack variants, or polymorphic malwares. Furthermore, "
        "manual rule generation creates severe operational latency. Artificial Intelligence (AI) and Machine Learning (ML) overcome these limitations "
        "by abstracting high-dimensional non-linear correlations from historical traffic flows, empowering classifiers to generalize across unseen "
        "attack vectors with high statistical confidence and low false alarm overhead.",
        styles['VTUBody']
    ))
    
    story.append(Paragraph("1.4 Need for Zero Trust-Inspired Access Verification", styles['VTUH1']))
    story.append(Paragraph(
        "Static access control lists (ACLs) cannot protect modern networks against credential hijacking or rogue insiders. In accordance with "
        "National Institute of Standards and Technology (NIST) Special Publication 800-207, the Zero Trust Architecture (ZTA) operates on the core "
        "doctrine: <i>'Never Trust, Always Verify'</i>. Integrating Zero Trust principles into an AI-powered NIDS enforces continuous cryptographic "
        "identity verification, strict Role-Based Access Control (RBAC), and immutable forensic audit logging, ensuring that administrative actions "
        "(such as model training and active model deployment) are segregated from monitoring duties and permanently accountable.",
        styles['VTUBody']
    ))
    
    story.append(Paragraph("1.5 Project Objectives", styles['VTUH1']))
    story.append(Paragraph(
        "The primary engineering objectives of this project are: (1) Architect a decoupled full-stack NIDS utilizing React 18, Flask, SQLite, and "
        "scikit-learn; (2) Implement an automated, data leakage-free preprocessing pipeline supporting UNSW-NB15, CIC-IDS2017, and NSL-KDD benchmarks; "
        "(3) Build a pluggable multi-model registry implementing Support Vector Machine (SVM), Random Forest, Logistic Regression, Deep MLP, and "
        "LSTM classifiers; (4) Integrate a real-time passive packet sniffer using Scapy and Windows Npcap for 5-tuple flow reassembly; and "
        "(5) Enforce 12-round salted Bcrypt authentication, stateless JWT session validation, RBAC, and tamper-resistant audit logging.",
        styles['VTUBody']
    ))
    
    story.append(Paragraph("1.6 Scope and Technical Boundaries", styles['VTUH1']))
    story.append(Paragraph(
        "The implemented system focuses on transport-layer flow telemetry (TCP, UDP, ICMP), offline model benchmarking, model hot-swapping, "
        "and real-time local network packet classification. To respect user privacy and computational line-rate constraints, deep payload content "
        "decryption of TLS 1.3 encrypted streams is out of scope; threat classification relies purely on behavioral flow statistics.",
        styles['VTUBody']
    ))
    story.append(PageBreak())
    return story

def build_page_2(styles, fig_dir):
    """PAGE 2 — PROBLEM STATEMENT AND REQUIREMENT ANALYSIS"""
    story = []
    story.append(Paragraph("CHAPTER 2: PROBLEM STATEMENT & REQUIREMENTS", styles['VTUChapter']))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#1E3A8A"), spaceBefore=2, spaceAfter=8))
    
    story.append(Paragraph("2.1 Problem Statement", styles['VTUH1']))
    story.append(Paragraph(
        "Enterprise network infrastructures are besieged by sophisticated, multi-stage cyber threats that easily evade conventional perimeter "
        "firewalls and signature-based intrusion detection tools. Legacy systems suffer from three crippling vulnerabilities: (1) Excessive false positive "
        "rates that cause Security Operations Center (SOC) analyst alert fatigue; (2) Total blindness to zero-day intrusions and polymorphic attack "
        "mutations; and (3) Implicit trust models that allow authenticated users unrestricted internal privileges without continuous verification or "
        "tamper-resistant forensic accountability. There is a critical necessity for a unified network intrusion detection system that integrates "
        "robust, multi-model AI classifiers with NIST SP 800-207 Zero Trust access governance.",
        styles['VTUBody']
    ))
    
    story.append(Paragraph("2.2 Functional Requirements (FR)", styles['VTUH1']))
    story.append(Paragraph(
        "• <b>FR-1: Cryptographic Authentication:</b> Secure user login with 12-round salted Bcrypt password verification and signed JWT token issuance.<br/>"
        "• <b>FR-2: Role-Based Authorization:</b> Strict privilege separation between Administrator (full rights) and Security Analyst (read-only telemetry).<br/>"
        "• <b>FR-3: Dataset Ingestion & Profiling:</b> Multipart upload, schema validation, missing/duplicate/infinite value cleaning for benchmark datasets.<br/>"
        "• <b>FR-4: Anti-Leakage Preprocessing:</b> Stratified train-val-test partitioning (70/15/15) with scalers fitted exclusively on training splits.<br/>"
        "• <b>FR-5: Multi-Model Training Engine:</b> Asynchronous training of SVM, Random Forest, Logistic Regression, MLP, and LSTM models.<br/>"
        "• <b>FR-6: Active Model Hot-Swapping:</b> Atomic runtime switching of the active deployed model in the registry without restarting the sniffer.<br/>"
        "• <b>FR-7: Live Packet Sniffing & Flow Reconstruction:</b> Promiscuous packet capture, 5-tuple flow aggregation, and real-time risk scoring.<br/>"
        "• <b>FR-8: Forensic Audit Trail:</b> Permanent logging of all login events, token validations, model changes, and unauthorized access violations.",
        styles['VTUBody']
    ))
    
    story.append(Paragraph("2.3 Non-Functional Requirements (NFR)", styles['VTUH1']))
    story.append(Paragraph(
        "• <b>NFR-1 (Inference Latency):</b> Live per-flow feature extraction and AI classification latency must remain sub-millisecond (< 1.0 ms/flow).<br/>"
        "• <b>NFR-2 (Throughput & Scalability):</b> Capable of ingesting benchmark datasets exceeding 2.8 million records without memory exhaustion.<br/>"
        "• <b>NFR-3 (Defensive Security):</b> Complete interception and HTTP 403 rejection of any unauthorized role privilege escalation attempts.<br/>"
        "• <b>NFR-4 (Evaluation Accuracy):</b> Holdout classification accuracy must exceed 95% with false alarm rates constrained below 3.0%.",
        styles['VTUBody']
    ))
    
    story.append(Paragraph("2.4 Hardware and Software Requirements", styles['VTUH1']))
    hw_sw_data = [
        [Paragraph("<b>Category</b>", styles['VTUTableHeader']), Paragraph("<b>Development Environment</b>", styles['VTUTableHeader']), Paragraph("<b>Deployment & Production Target</b>", styles['VTUTableHeader'])],
        [Paragraph("Processor (CPU)", styles['VTUTableCellBold']), Paragraph("Intel Core i5 / AMD Ryzen 5 (4+ Cores, 2.5 GHz+)", styles['VTUTableCell']), Paragraph("Intel Xeon / Core i7 (8+ Cores, 3.2 GHz+)", styles['VTUTableCell'])],
        [Paragraph("System Memory (RAM)", styles['VTUTableCellBold']), Paragraph("16 GB DDR4 Dual-Channel", styles['VTUTableCell']), Paragraph("32 GB DDR4 / ECC RAM", styles['VTUTableCell'])],
        [Paragraph("Storage", styles['VTUTableCellBold']), Paragraph("512 GB NVMe M.2 Solid State Drive", styles['VTUTableCell']), Paragraph("1 TB NVMe SSD (Enterprise endurance)", styles['VTUTableCell'])],
        [Paragraph("Network Interface", styles['VTUTableCellBold']), Paragraph("Realtek RTL8821CE 802.11ac Wi-Fi / GbE LAN", styles['VTUTableCell']), Paragraph("Gigabit Ethernet Adapter with Npcap / Promiscuous Mode", styles['VTUTableCell'])],
        [Paragraph("Operating System", styles['VTUTableCellBold']), Paragraph("Microsoft Windows 11 64-bit (Build 22631+)", styles['VTUTableCell']), Paragraph("Windows Server 2022 / Ubuntu Linux 22.04 LTS", styles['VTUTableCell'])],
        [Paragraph("Runtime & Languages", styles['VTUTableCellBold']), Paragraph("Python 3.13.15, Node.js v20.18.0, npm v10.8.2", styles['VTUTableCell']), Paragraph("Python 3.11 / 3.13, Node.js LTS, Npcap 1.79+", styles['VTUTableCell'])],
        [Paragraph("Frameworks & Tools", styles['VTUTableCellBold']), Paragraph("React 18, Vite, Tailwind CSS, Flask, SQLite3", styles['VTUTableCell']), Paragraph("Gunicorn / Waitress WSGI, SQLite / PostgreSQL", styles['VTUTableCell'])],
        [Paragraph("Core Libraries", styles['VTUTableCellBold']), Paragraph("Scikit-Learn, Scapy, Pandas, NumPy, Bcrypt, PyJWT", styles['VTUTableCell']), Paragraph("Joblib, TensorFlow/Keras, Matplotlib, ReportLab", styles['VTUTableCell'])]
    ]
    t_hw = Table(hw_sw_data, colWidths=[90, 195, 195])
    t_hw.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1E3A8A")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(t_hw)
    story.append(Paragraph("Table 2.1: Hardware, Software, Library, and Operational Environment Specifications.", styles['VTUCaption']))
    
    story.append(Paragraph("2.5 Assumptions and Constraints", styles['VTUH1']))
    story.append(Paragraph(
        "• Network packet capture requires elevated Npcap kernel driver privileges on the host operating system.<br/>"
        "• Datasets are provided in structured CSV format conforming to established cybersecurity research benchmarks (CIC-IDS2017, UNSW-NB15, NSL-KDD).",
        styles['VTUBody']
    ))
    story.append(PageBreak())
    return story

def build_page_3(styles, fig_dir):
    """PAGE 3 — LITERATURE REVIEW AND TECHNOLOGY STUDY"""
    story = []
    story.append(Paragraph("CHAPTER 3: LITERATURE REVIEW & STUDY", styles['VTUChapter']))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#1E3A8A"), spaceBefore=2, spaceAfter=8))
    
    story.append(Paragraph("3.1 Evolution of Intrusion Detection Technologies", styles['VTUH1']))
    story.append(Paragraph(
        "The conceptual foundations of automated intrusion detection originated in J. P. Anderson’s seminal 1980 technical report [1], which categorized "
        "computer security threats into internal misuse, external penetration, and misfeasance. In 1987, D. E. Denning formulated the first formal "
        "anomaly detection model [2], positing that malicious incursions manifest as statistically quantifiable deviations from normal system activity. "
        "During the late 1990s, deterministic signature-based detection systems, exemplified by M. Roesch’s open-source Snort engine [3], became the "
        "de facto standard. However, signature matching exhibits severe structural weaknesses: it cannot detect novel zero-day exploits, requires "
        "continuous manual rule authoring, and produces unsustainable false positive rates in high-throughput enterprise networks.",
        styles['VTUBody']
    ))
    
    story.append(Paragraph("3.2 Machine Learning and Deep Learning in Cyber Telemetry", styles['VTUH1']))
    story.append(Paragraph(
        "To mitigate signature rigidity, researchers applied machine learning classifiers to network telemetry. Moustafa and Slay (2015) introduced "
        "the UNSW-NB15 benchmark [5], demonstrating that modern synthetic attack vectors require high-dimensional statistical flow attributes. Sharafaldin "
        "et al. (2018) released the CIC-IDS2017 benchmark [6], standardizing 80+ connection attributes. Supervised classifiers—such as Support Vector "
        "Machines (SVM) with Radial Basis Function (RBF) kernels and Random Forest ensemble trees—demonstrated high generalization accuracy [7]. "
        "For complex temporal correlations, recurrent architectures like Long Short-Term Memory (LSTM) networks [8] and Deep Multilayer Perceptrons "
        "(MLP) were engineered to model inter-packet arrival times and bidirectional byte exchanges.",
        styles['VTUBody']
    ))
    
    story.append(Paragraph("3.3 Zero Trust Architecture (NIST SP 800-207)", styles['VTUH1']))
    story.append(Paragraph(
        "In 2020, the National Institute of Standards and Technology codified the Zero Trust Architecture in NIST SP 800-207 [4]. Zero Trust discards "
        "the implicit trust granted to internal IP subnets, mandating continuous identity verification, dynamic least-privilege authorization, and "
        "comprehensive forensic telemetry. J. Kindervag (2010) originally formulated the Zero Trust model at Forrester Research, emphasizing that all "
        "traffic must be inspected and logged regardless of physical network location.",
        styles['VTUBody']
    ))
    
    story.append(Paragraph("3.4 Comparison of Relevant Methodologies", styles['VTUH1']))
    comp_data = [
        [Paragraph("<b>Approach / Paradigm</b>", styles['VTUTableHeader']), Paragraph("<b>Primary Detection Mechanism</b>", styles['VTUTableHeader']), Paragraph("<b>Zero-Day Resilience</b>", styles['VTUTableHeader']), Paragraph("<b>Identity & Access Governance</b>", styles['VTUTableHeader']), Paragraph("<b>Line-Rate Overhead</b>", styles['VTUTableHeader'])],
        [Paragraph("Rule / Signature NIDS (Snort, Suricata)", styles['VTUTableCellBold']), Paragraph("Deterministic regex string matching on raw packet payloads [3]", styles['VTUTableCell']), Paragraph("None (Fails against unknown attacks)", styles['VTUTableCellCenter']), Paragraph("None (Stateless packet inspection only)", styles['VTUTableCellCenter']), Paragraph("Low (Regex ASIC/CPU matching)", styles['VTUTableCellCenter'])],
        [Paragraph("Statistical Anomaly NIDS (Denning Model)", styles['VTUTableCellBold']), Paragraph("Parametric Gaussian distribution thresholds on metrics [2]", styles['VTUTableCell']), Paragraph("Moderate (Flags gross volume deviations)", styles['VTUTableCellCenter']), Paragraph("None (IP-level telemetry only)", styles['VTUTableCellCenter']), Paragraph("Very Low (Statistical counters)", styles['VTUTableCellCenter'])],
        [Paragraph("Standalone ML NIDS (SVM / Random Forest)", styles['VTUTableCellBold']), Paragraph("Supervised statistical learning on flow tabular vectors [7]", styles['VTUTableCell']), Paragraph("High (Strong mathematical generalization)", styles['VTUTableCellCenter']), Paragraph("None (Offline scripts without RBAC/JWT)", styles['VTUTableCellCenter']), Paragraph("Sub-millisecond per flow", styles['VTUTableCellCenter'])],
        [Paragraph("Deep Sequence NIDS (LSTM / Deep Neural)", styles['VTUTableCellBold']), Paragraph("Temporal recurrent modeling of packet arrival sequences [8]", styles['VTUTableCell']), Paragraph("Very High (Captures non-linear dynamics)", styles['VTUTableCellCenter']), Paragraph("None (Academic standalone models)", styles['VTUTableCellCenter']), Paragraph("Moderate (Matrix GPU/CPU tensors)", styles['VTUTableCellCenter'])],
        [Paragraph("<b>Implemented Zero Trust AI-NIDS</b>", styles['VTUTableCellBold']), Paragraph("<b>Pluggable Multi-Model AI (SVM, RF, MLP, LSTM) + 5-Tuple Aggregation</b>", styles['VTUTableCell']), Paragraph("<b>Exceptional (96–99% accuracy across 3 benchmarks)</b>", styles['VTUTableCellCenter']), Paragraph("<b>Full NIST SP 800-207 RBAC, 12-round Bcrypt, JWT, 1,316+ Audit Logs</b>", styles['VTUTableCellCenter']), Paragraph("<b>0.0512 ms / flow (~19,531 flows/sec)</b>", styles['VTUTableCellCenter'])]
    ]
    t_comp = Table(comp_data, colWidths=[90, 130, 85, 110, 65])
    t_comp.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1E3A8A")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(t_comp)
    story.append(Paragraph("Table 3.1: Comparative Synthesis of Existing NIDS Approaches vs Implemented System.", styles['VTUCaption']))
    
    story.append(Paragraph("3.5 Research and Implementation Gap Addressed", styles['VTUH1']))
    story.append(Paragraph(
        "A critical survey of existing literature reveals a profound implementation divide: academic research overwhelmingly focuses on isolated "
        "machine learning algorithms evaluated on static offline datasets without considering deployment authentication or access control; conversely, "
        "commercial enterprise security tools deploy rigid perimeter rules without adaptable deep learning inference. This project directly addresses "
        "this gap by engineering an integrated, full-stack Zero Trust AI-NIDS that couples production-grade access governance with live packet telemetry.",
        styles['VTUBody']
    ))
    story.append(PageBreak())
    return story

def build_page_4(styles, fig_dir):
    """PAGE 4 — SYSTEM DESIGN OVERVIEW"""
    story = []
    story.append(Paragraph("CHAPTER 4: SYSTEM DESIGN OVERVIEW", styles['VTUChapter']))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#1E3A8A"), spaceBefore=2, spaceAfter=8))
    
    story.append(Paragraph("4.1 Master 5-Tier Decoupled Architecture Topology", styles['VTUH1']))
    story.append(Paragraph(
        "The Zero Trust AI-Powered Network Intrusion Detection System is engineered upon a robust, modular 5-tier decoupled topology. "
        "This tiered architectural separation ensures high scalability, maintainability, fault isolation, and strict enforcement of security "
        "boundaries across all computational layers. Each tier performs a single, well-defined responsibility and communicates with adjacent "
        "tiers exclusively through standardized, authenticated interfaces:",
        styles['VTUBody']
    ))
    story.append(Paragraph(
        "• <b>Tier 1: Presentation & SOC Dashboard Tier:</b> Built with React 18, Vite, and Tailwind CSS. Provides a responsive single-page "
        "interface featuring real-time telemetry streaming, interactive dataset comparison matrices, model training progress monitors, and audit logs.<br/>"
        "• <b>Tier 2: API Gateway & Application Routing Tier:</b> Implemented via Python Flask REST blueprints (`auth_bp`, `dataset_bp`, `model_bp`, "
        "`live_detection_bp`). Manages HTTP routing, JSON payload serialization, CORS pre-flight validation, and structured error responses.<br/>"
        "• <b>Tier 3: Zero Trust Security Policy Enforcement Tier:</b> Acts as an inline cryptographic gatekeeper. Enforces 12-round salted Bcrypt "
        "hashing, stateless HMAC-SHA256 JWT validation, and Role-Based Access Control (RBAC) method decorators (`@require_role`).<br/>"
        "• <b>Tier 4: Machine Learning & Telemetry Engine Tier:</b> Houses the Pluggable Model Registry (SVM, Random Forest, Logistic Regression, "
        "MLP, LSTM), the anti-leakage preprocessing pipeline, and the Scapy/Npcap passive packet sniffing and 5-tuple flow aggregation engine.<br/>"
        "• <b>Tier 5: Persistence & Forensic Audit Tier:</b> Powered by SQLite (`database.db`), storing users, roles, dataset metadata, model runs, "
        "live threat detections, and immutable audit logs, complemented by joblib/Keras serialized model artifacts on disk.",
        styles['VTUBody']
    ))
    
    # Mandatory Master Architecture Diagram
    img_path = os.path.join(fig_dir, "fig3_1_master_architecture.png")
    if os.path.exists(img_path):
        story.append(Spacer(1, 4))
        story.append(Image(img_path, width=440, height=195))
        story.append(Paragraph("Figure 4.1: Master 5-Tier Zero Trust AI-NIDS System Architecture Topology.", styles['VTUCaption']))
    
    story.append(Paragraph("4.2 Data Flow and Trust Boundaries", styles['VTUH1']))
    story.append(Paragraph(
        "Untrusted HTTP requests from the React frontend must traverse the Zero Trust gateway before reaching any backend service. Requests missing "
        "a valid cryptographic JWT token are immediately terminated with HTTP 401 Unauthorized. If authenticated, the claims are extracted and checked "
        "against the endpoint's RBAC whitelist; unauthorized roles are rejected with HTTP 403 Forbidden and logged to the forensic audit database. "
        "Only fully verified requests proceed to execute model training, dataset curation, or packet sniffing routines.",
        styles['VTUBody']
    ))
    story.append(PageBreak())
    return story

def build_page_5(styles, fig_dir):
    """PAGE 5 — ZERO TRUST SECURITY ARCHITECTURE"""
    story = []
    story.append(Paragraph("CHAPTER 5: ZERO TRUST SECURITY ARCHITECTURE", styles['VTUChapter']))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#1E3A8A"), spaceBefore=2, spaceAfter=8))
    
    story.append(Paragraph("5.1 Zero Trust Principles Applied to NIDS", styles['VTUH1']))
    story.append(Paragraph(
        "In compliance with NIST SP 800-207 recommendations, the system abandons perimeter-based assumptions in favor of four core doctrines: "
        "(1) <i>Explicit Identity Verification:</i> No human operator or API client is granted access without authenticating via salted cryptographic "
        "credentials; (2) <i>Least Privilege Access:</i> Operators receive the minimum permissions necessary to fulfill their specific role; "
        "(3) <i>Continuous Inspection:</i> Every individual API request is independently evaluated for token validity and claim integrity; and "
        "(4) <i>Assume Breach:</i> The system assumes the local network may be hostile; all security-sensitive actions are recorded to an immutable "
        "forensic audit trail to guarantee non-repudiation.",
        styles['VTUBody']
    ))
    
    story.append(Paragraph("5.2 Cryptographic Identity & Session Management", styles['VTUH1']))
    story.append(Paragraph(
        "User passwords are protected using the adaptive Bcrypt algorithm configured with a work factor of 12 rounds ($2^{12} = 4096$ iterations), "
        "providing robust defense against offline dictionary and GPU rainbow table attacks. Upon successful credential validation, the server "
        "issues a compact, cryptographically signed JSON Web Token (JWT) utilizing the HMAC-SHA256 (`HS256`) algorithm. The JWT payload encodes "
        "the subject `user_id`, `username`, assigned `role`, issuance timestamp (`iat`), and strict expiration (`exp`, 24-hour validity window).",
        styles['VTUBody']
    ))
    
    # Mandatory Zero Trust Diagram
    img_path = os.path.join(fig_dir, "fig3_2_zero_trust_architecture.png")
    if os.path.exists(img_path):
        story.append(Spacer(1, 4))
        story.append(Image(img_path, width=440, height=180))
        story.append(Paragraph("Figure 5.1: Zero Trust Continuous Request Verification and RBAC Authorization Flow.", styles['VTUCaption']))
    
    story.append(Paragraph("5.3 Role-Based Access Control (RBAC) & Separation of Duties", styles['VTUH1']))
    story.append(Paragraph(
        "Under NIST SP 800-207 guidelines, operational responsibilities are divided into two mutually exclusive roles: "
        "<b>Administrator</b> (maintains full authority to upload datasets, configure preprocessing, trigger model training runs, hot-swap "
        "active classifiers, and review audit trails) and <b>Security Analyst</b> (granted operational monitoring permissions to view telemetry "
        "dashboards, execute live packet capture, inspect threat classifications, and export evaluation reports, while strictly barred from modifying "
        "underlying datasets or deleting models). Python decorators (`@jwt_required` and `@require_role(['Admin'])`) enforce this separation "
        "deterministically at the backend gateway.",
        styles['VTUBody']
    ))
    story.append(Paragraph("5.4 Security Boundaries and Limitations", styles['VTUH1']))
    story.append(Paragraph(
        "While the system enforces Zero Trust access governance across all REST endpoints and administrative functions, packet-level inspection "
        "operates within established boundaries: transport-layer flows are classified without decrypting TLS session payloads, maintaining user privacy.",
        styles['VTUBody']
    ))
    story.append(PageBreak())
    return story

def build_page_6(styles, fig_dir):
    """PAGE 6 — USE CASE AND MODULE DESIGN"""
    story = []
    story.append(Paragraph("CHAPTER 6: USE CASE & MODULE DESIGN", styles['VTUChapter']))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#1E3A8A"), spaceBefore=2, spaceAfter=8))
    
    story.append(Paragraph("6.1 System Actors & Use-Case Specification", styles['VTUH1']))
    story.append(Paragraph(
        "The system explicitly defines two human actors whose privileges strictly reflect their operational role in the security lifecycle: "
        "<b>Administrator (Admin)</b> and <b>Security Analyst (Analyst)</b>. A generic unauthenticated user possesses no operational access beyond "
        "the public login screen. The core use cases encompass: (UC-1) Authenticate and receive signed JWT session credentials; "
        "(UC-2) Manage benchmark datasets (multipart CSV upload, schema parsing, cross-dataset statistical distribution comparison); "
        "(UC-3) Train AI models across pluggable algorithms with custom hyperparameter controls; (UC-4) Inspect holdout evaluation metrics "
        "and ROC/PR curves; (UC-5) Hot-swap the active deployed model; (UC-6) Start/stop live passive packet sniffing; (UC-7) Monitor real-time "
        "threat alerts and piecewise risk levels; and (UC-8) Review tamper-resistant forensic audit logs.",
        styles['VTUBody']
    ))
    
    # Mandatory Use Case Diagram
    img_uc = os.path.join(fig_dir, "fig_use_case_diagram.png")
    if os.path.exists(img_uc):
        story.append(Spacer(1, 2))
        story.append(Image(img_uc, width=440, height=165))
        story.append(Paragraph("Figure 6.1: Zero Trust AI-NIDS Actor and Role Separation Use-Case Diagram.", styles['VTUCaption']))
    
    story.append(Paragraph("6.2 Module & Component Subsystem Architecture", styles['VTUH1']))
    story.append(Paragraph(
        "The backend is partitioned into self-contained, decoupled subsystems communicating across clean functional boundaries: "
        "(1) <i>Authentication Service</i> (`security/jwt_auth.py`, `security/password.py`); (2) <i>Dataset Preprocessing Engine</i> "
        "(`preprocessing/preprocess.py`, `preprocessing/dataset_loader.py`); (3) <i>Pluggable Model Registry</i> (`training/model_registry.py`, "
        "`training/train_model.py`); (4) <i>Live Detection & Flow Manager</i> (`live_detection/packet_capture.py`, `live_detection/flow_manager.py`); "
        "and (5) <i>Forensic Audit Logger</i> (`utils/logger.py`, `database/init_db.py`).",
        styles['VTUBody']
    ))
    
    # Mandatory Component Subsystem Diagram
    img_comp = os.path.join(fig_dir, "fig3_3_preprocessing_training_architecture.png")
    if os.path.exists(img_comp):
        story.append(Spacer(1, 2))
        story.append(Image(img_comp, width=440, height=160))
        story.append(Paragraph("Figure 6.2: Preprocessing, Model Registry and Training Component Subsystem Diagram.", styles['VTUCaption']))
    story.append(PageBreak())
    return story

def build_page_7(styles, fig_dir):
    """PAGE 7 — DATASET DESIGN AND PREPROCESSING"""
    story = []
    story.append(Paragraph("CHAPTER 7: DATASET DESIGN & PREPROCESSING", styles['VTUChapter']))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#1E3A8A"), spaceBefore=2, spaceAfter=8))
    
    story.append(Paragraph("7.1 Multi-Benchmark Dataset Governance", styles['VTUH1']))
    story.append(Paragraph(
        "To prevent single-dataset evaluation bias and ensure architectural generalization, the system catalogs and supports three authoritative "
        "cybersecurity benchmarks totaling over 5.51 million records: <b>UNSW-NB15</b> (2,540,044 flows, 49 features, modern low-footprint attack categories), "
        "<b>CIC-IDS2017</b> (2,830,743 flows, 79 features, realistic background protocols and volumetric DoS/DDoS vectors), and <b>NSL-KDD</b> (148,517 flows, "
        "42 features, refined non-redundant legacy benchmark). Target columns are resolved dynamically across `attack_cat`, `Label`, and `label`.",
        styles['VTUBody']
    ))
    
    story.append(Paragraph("7.2 Ingestion, Cleaning & Imputation Pipeline", styles['VTUH1']))
    story.append(Paragraph(
        "Raw network telemetry frequently contains computational anomalies that disrupt machine learning optimization. The preprocessing engine "
        "executes a strict multi-stage cleansing sequence: (1) Identifies and replaces infinite values (`+inf`, `-inf`) with null placeholders (`NaN`); "
        "(2) Deduplicates records prior to dataset splitting; (3) Imputes missing continuous numerical attributes using class-conditional median values "
        "(robust against extreme outliers); and (4) Imputes nominal missing attributes using category modes. Categorical text features "
        "(`proto`, `service`, `state`) are encoded via Scikit-Learn `LabelEncoder` objects serialized for inference compatibility.",
        styles['VTUBody']
    ))
    
    # Mandatory Preprocessing Flowchart
    img_prep = os.path.join(fig_dir, "fig3_7_preprocessing_flowchart.png")
    if os.path.exists(img_prep):
        story.append(Spacer(1, 3))
        story.append(Image(img_prep, width=440, height=170))
        story.append(Paragraph("Figure 7.1: Multi-Dataset Ingestion, Cleaning, and Anti-Leakage Preprocessing Flowchart.", styles['VTUCaption']))
    
    story.append(Paragraph("7.3 Strict Data-Leakage Prevention & Stratification", styles['VTUH1']))
    story.append(Paragraph(
        "A critical flaw in many published NIDS models is data leakage caused by normalizing entire datasets before splitting. Our pipeline enforces "
        "strict mathematical isolation: a stratified split partitions clean data into <b>70% Training ($N_{train}$), 15% Validation ($N_{val}$), and "
        r"15% Independent Holdout Test ($N_{test}$)</b> splits using fixed seed 42. Scikit-Learn `StandardScaler` ($\mu=0, \sigma=1$) is fitted "
        r"<b>exclusively on the training partition ($X_{train}$)</b>. The resulting parameters ($\mu_{train}, \sigma_{train}$) are serialized to disk "
        "(`scaler.pkl`) and applied as a pure transformation to validation, holdout test, and live streaming network flows.",
        styles['VTUBody']
    ))
    
    ds_summary_data = [
        [Paragraph("<b>Dataset</b>", styles['VTUTableHeader']), Paragraph("<b>Total Rows</b>", styles['VTUTableHeader']), Paragraph("<b>Features</b>", styles['VTUTableHeader']), Paragraph("<b>Train (70%)</b>", styles['VTUTableHeader']), Paragraph("<b>Val (15%)</b>", styles['VTUTableHeader']), Paragraph("<b>Test (15%)</b>", styles['VTUTableHeader']), Paragraph("<b>Primary Target Taxonomy</b>", styles['VTUTableHeader'])],
        [Paragraph("UNSW-NB15", styles['VTUTableCellBold']), Paragraph("2,540,044", styles['VTUTableCellCenter']), Paragraph("49 Raw / 15 Live", styles['VTUTableCellCenter']), Paragraph("17,500", styles['VTUTableCellCenter']), Paragraph("3,750", styles['VTUTableCellCenter']), Paragraph("3,750", styles['VTUTableCellCenter']), Paragraph("7-Class: Normal, Generic, Exploits, Fuzzers, DoS, Recon, Analysis", styles['VTUTableCell'])],
        [Paragraph("CIC-IDS2017", styles['VTUTableCellBold']), Paragraph("2,830,743", styles['VTUTableCellCenter']), Paragraph("79 Raw / 22 Live", styles['VTUTableCellCenter']), Paragraph("17,500", styles['VTUTableCellCenter']), Paragraph("3,750", styles['VTUTableCellCenter']), Paragraph("3,750", styles['VTUTableCellCenter']), Paragraph("15-Class: Benign, DoS Hulk, PortScan, DDoS, FTP-Patator, etc.", styles['VTUTableCell'])],
        [Paragraph("NSL-KDD", styles['VTUTableCellBold']), Paragraph("148,517", styles['VTUTableCellCenter']), Paragraph("42 Raw / 19 Live", styles['VTUTableCellCenter']), Paragraph("35,000", styles['VTUTableCellCenter']), Paragraph("7,500", styles['VTUTableCellCenter']), Paragraph("7,500", styles['VTUTableCellCenter']), Paragraph("5-Class / Binary: Normal, DoS, Probe, R2L, U2R", styles['VTUTableCell'])]
    ]
    t_ds = Table(ds_summary_data, colWidths=[65, 55, 65, 55, 50, 50, 160])
    t_ds.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1E3A8A")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(t_ds)
    story.append(Paragraph("Table 7.1: Benchmark Intrusion Datasets Characteristics and Stratified Partition Statistics.", styles['VTUCaption']))
    story.append(PageBreak())
    return story

def build_page_8(styles, fig_dir):
    """PAGE 8 — MACHINE LEARNING MODEL DESIGN"""
    story = []
    story.append(Paragraph("CHAPTER 8: MACHINE LEARNING MODEL DESIGN", styles['VTUChapter']))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#1E3A8A"), spaceBefore=2, spaceAfter=8))
    
    story.append(Paragraph("8.1 Pluggable Model Registry Architecture", styles['VTUH1']))
    story.append(Paragraph(
        "To avoid architectural lock-in, the system incorporates a polymorphic Model Registry (`training/model_registry.py`) implementing "
        "an abstract base class `BaseNIDSModel`. Every concrete model implements uniform lifecycle hooks: `build_estimator()`, `train()`, "
        "`predict()`, `predict_proba()`, `save()`, and `load()`. This standardized contract enables seamless comparison and zero-downtime hot-swapping "
        "across four distinct machine learning families:",
        styles['VTUBody']
    ))
    story.append(Paragraph(
        r"• <b>Support Vector Machine (SVM):</b> Utilizes Scikit-Learn `SVC` with a non-linear Radial Basis Function (Gaussian RBF) kernel. "
        r"Optimizes maximum-margin hyperplanes in transformed feature space, configured with regularization parameter $C=1.0$, kernel coefficient "
        r"$\gamma=\text{'scale'}$, and `class_weight='balanced'` to offset threat class disparities.<br/>"
        "• <b>Random Forest Classifier:</b> An ensemble of 100 decorrelated decision trees (`n_estimators=100`, `criterion='gini'`). Employs bootstrap "
        "aggregation (bagging) to achieve superior resilience against feature noise and extreme classification stability.<br/>"
        "• <b>Multinomial Logistic Regression:</b> A generalized linear model utilizing L2 ridge regularization and the L-BFGS quasi-Newton optimization "
        "solver. Serves as a high-speed linear classification baseline.<br/>"
        "• <b>Deep Neural Networks (MLP & LSTM):</b> Multilayer feedforward networks configured with dense layers, Batch Normalization, ReLU "
        "activations, Dropout (0.2), and Adam optimization, alongside sequential Long Short-Term Memory (LSTM) recurrent architectures for connection sequences.",
        styles['VTUBody']
    ))
    
    # Mandatory Training Pipeline Diagram
    img_train = os.path.join(fig_dir, "fig3_8_training_flowchart.png")
    if os.path.exists(img_train):
        story.append(Spacer(1, 4))
        story.append(Image(img_train, width=440, height=180))
        story.append(Paragraph("Figure 8.1: Machine Learning Model Training, Hot-Swapping, and Inference Pipeline.", styles['VTUCaption']))
    
    story.append(Paragraph("8.2 Model Hyperparameters and Serialization", styles['VTUH1']))
    story.append(Paragraph(
        "Trained model artifacts are persisted to disk using `joblib.dump()` for Scikit-Learn pipelines and Keras `.h5`/`.keras` format for deep networks. "
        "Every serialized artifact is packaged with its associated feature names, preprocessing scaler, label encoder, and hyperparameter metadata dictionary, "
        "guaranteeing complete reproducibility and schema integrity upon deserialization.",
        styles['VTUBody']
    ))
    
    hp_data = [
        [Paragraph("<b>Model Name</b>", styles['VTUTableHeader']), Paragraph("<b>Algorithm / Family</b>", styles['VTUTableHeader']), Paragraph("<b>Key Hyperparameters & Optimizers</b>", styles['VTUTableHeader']), Paragraph("<b>Artifact Format</b>", styles['VTUTableHeader'])],
        [Paragraph("Support Vector Machine (Active)", styles['VTUTableCellBold']), Paragraph("Scikit-Learn SVC (RBF Kernel)", styles['VTUTableCell']), Paragraph("C=1.0, gamma='scale', probability=True, class_weight='balanced'", styles['VTUTableCell']), Paragraph("model.joblib (951.4 KB)", styles['VTUTableCellCenter'])],
        [Paragraph("Random Forest", styles['VTUTableCellBold']), Paragraph("Ensemble Bagging Trees", styles['VTUTableCell']), Paragraph("n_estimators=100, criterion='gini', max_depth=None, n_jobs=-1", styles['VTUTableCell']), Paragraph("model.joblib (14.2 MB)", styles['VTUTableCellCenter'])],
        [Paragraph("Logistic Regression", styles['VTUTableCellBold']), Paragraph("Multinomial Linear Classifier", styles['VTUTableCell']), Paragraph("penalty='l2', C=1.0, solver='lbfgs', max_iter=1000", styles['VTUTableCell']), Paragraph("model.joblib (48.1 KB)", styles['VTUTableCellCenter'])],
        [Paragraph("Deep MLP / LSTM", styles['VTUTableCellBold']), Paragraph("Deep Recurrent / Dense Neural", styles['VTUTableCell']), Paragraph("hidden_layers=[128, 64], lr=0.001, optimizer=Adam, dropout=0.2", styles['VTUTableCell']), Paragraph("model.keras (2.4 MB)", styles['VTUTableCellCenter'])]
    ]
    t_hp = Table(hp_data, colWidths=[110, 100, 160, 130])
    t_hp.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1E3A8A")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(t_hp)
    story.append(Paragraph("Table 8.1: Machine Learning Model Configurations, Kernel Functions, and Hyperparameters.", styles['VTUCaption']))
    story.append(PageBreak())
    return story

def build_page_9(styles, fig_dir):
    """PAGE 9 — MODEL MATHEMATICS AND ALGORITHMS"""
    story = []
    story.append(Paragraph("CHAPTER 9: MODEL MATHEMATICS & ALGORITHMS", styles['VTUChapter']))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#1E3A8A"), spaceBefore=2, spaceAfter=8))
    
    story.append(Paragraph("9.1 Mathematical Formulation of Implemented Classifiers", styles['VTUH1']))
    story.append(Paragraph(
        "<b>1. Support Vector Machine Optimization & RBF Kernel:</b> The soft-margin SVM optimizes a separating hyperplane in transformed Hilbert space "
        "by solving the quadratic dual problem with slack penalties $\\xi_i$:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<b>min</b><sub>w, b, &xi;</sub> &nbsp; <sup>1</sup>/<sub>2</sub> ||w||<sup>2</sup> + C &sum;<sub>i=1</sub><sup>N</sup> &xi;<sub>i</sub> "
        "&nbsp;&nbsp;&nbsp;&nbsp;<b>s.t.</b> &nbsp; y<sub>i</sub>(w<sup>T</sup>&phi;(x<sub>i</sub>) + b) &ge; 1 - &xi;<sub>i</sub>, &nbsp; &xi;<sub>i</sub> &ge; 0<br/>"
        "The Gaussian Radial Basis Function (RBF) kernel projects non-linear flows into infinite dimensions: &nbsp; "
        "<b>K(x<sub>i</sub>, x<sub>j</sub>) = exp(-&gamma; ||x<sub>i</sub> - x<sub>j</sub>||<sup>2</sup>)</b>, where &gamma; = <sup>1</sup>/<sub>(2&sigma;<sup>2</sup>)</sub>.",
        styles['VTUBody']
    ))
    story.append(Paragraph(
        "<b>2. Preprocessing Scaling & Activation Functions:</b><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;Feature Standardization: &nbsp; <b>z = (x - &mu;<sub>train</sub>) / &sigma;<sub>train</sub></b> &nbsp;&nbsp;|&nbsp;&nbsp; "
        "Sigmoid Activation: &nbsp; <b>&sigma;(z) = 1 / (1 + e<sup>-z</sup>)</b><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;Softmax Multi-Class Probability: &nbsp; <b>P(Y = c | x) = exp(z<sub>c</sub>) / &sum;<sub>j=1</sub><sup>C</sup> exp(z<sub>j</sub>)</b>",
        styles['VTUBody']
    ))
    story.append(Paragraph(
        "<b>3. Objective Loss Functions:</b> Binary Cross-Entropy Loss for two-class discrimination and Categorical Cross-Entropy for 7-class attack taxonomy:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<b>L<sub>BCE</sub> = - <sup>1</sup>/<sub>N</sub> &sum;<sub>i=1</sub><sup>N</sup> [ y<sub>i</sub> ln(&#375;<sub>i</sub>) + (1 - y<sub>i</sub>) ln(1 - &#375;<sub>i</sub>) ]</b> &nbsp;&nbsp;|&nbsp;&nbsp; "
        "<b>L<sub>CCE</sub> = - <sup>1</sup>/<sub>N</sub> &sum;<sub>i=1</sub><sup>N</sup> &sum;<sub>c=1</sub><sup>C</sup> y<sub>ic</sub> ln(&#375;<sub>ic</sub>)</b>",
        styles['VTUBody']
    ))
    story.append(Paragraph(
        "<b>4. Recurrent LSTM Cell Gates & Tensor Dimensions:</b> Recurrent units maintain an internal memory cell C<sub>t</sub> and hidden state h<sub>t</sub> "
        "governed by input gate i<sub>t</sub>, forget gate f<sub>t</sub>, and output gate o<sub>t</sub>:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;f<sub>t</sub> = &sigma;(W<sub>f</sub> [h<sub>t-1</sub>, x<sub>t</sub>] + b<sub>f</sub>) &nbsp;&nbsp;|&nbsp;&nbsp; "
        "i<sub>t</sub> = &sigma;(W<sub>i</sub> [h<sub>t-1</sub>, x<sub>t</sub>] + b<sub>i</sub>) &nbsp;&nbsp;|&nbsp;&nbsp; "
        "C&#771;<sub>t</sub> = tanh(W<sub>c</sub> [h<sub>t-1</sub>, x<sub>t</sub>] + b<sub>c</sub>)<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;C<sub>t</sub> = f<sub>t</sub> &odot; C<sub>t-1</sub> + i<sub>t</sub> &odot; C&#771;<sub>t</sub> &nbsp;&nbsp;|&nbsp;&nbsp; "
        "o<sub>t</sub> = &sigma;(W<sub>o</sub> [h<sub>t-1</sub>, x<sub>t</sub>] + b<sub>o</sub>) &nbsp;&nbsp;|&nbsp;&nbsp; "
        "h<sub>t</sub> = o<sub>t</sub> &odot; tanh(C<sub>t</sub>)<br/>"
        "Input tensor format is 3-dimensional: <b>[Batch_Size = 64, Timesteps = 10, Feature_Dim = 15]</b>.",
        styles['VTUBody']
    ))
    
    story.append(Paragraph("9.2 Algorithmic Pseudocode", styles['VTUH1']))
    code_text = (
        "Algorithm 9.1: Data Leakage-Free Preprocessing and Model Training\n"
        "Input: Raw Dataset D = {x_i, y_i}, Algorithm A in {SVM, RF, LR, MLP, LSTM}, Seed = 42\n"
        "Output: Serialized Model M*, Scaler S*, Evaluation Report R\n"
        " 1: Replace inf and -inf values in D with NaN; drop duplicate rows;\n"
        " 2: Impute numeric NaNs with column median; impute categorical NaNs with mode;\n"
        " 3: Stratified partition D into D_train (70%), D_val (15%), D_test (15%) using Seed 42;\n"
        " 4: Fit StandardScaler S* strictly on X_train: mu = mean(X_train), sigma = std(X_train);\n"
        " 5: Transform X_train, X_val, X_test using S*;\n"
        " 6: Initialize model estimator M with hyperparameters from registry;\n"
        " 7: Train M on (X_train, y_train); validate convergence on (X_val, y_val);\n"
        " 8: Compute holdout metrics R on (X_test, y_test): Accuracy, Precision, Recall, F1, ROC-AUC, CM;\n"
        " 9: Serialize M*, S*, and R to disk; return M*, R.\n"
        "-----------------------------------------------------------------------------------------\n"
        "Algorithm 9.2: Real-Time Flow Reassembly and Streaming Risk Inference\n"
        "Input: Live packet stream P from Scapy/Npcap, Active Model M*, Scaler S*\n"
        " 1: for each packet p in P do:\n"
        " 2:    Extract canonical 5-tuple key: K = (min(IP_s, IP_d), max(IP_s, IP_d), min(P_s, P_d), max(P_s, P_d), Proto)\n"
        " 3:    Update bidirectional flow F[K]: packet count, byte volume, TCP flags, duration\n"
        " 4:    if flow terminates (FIN/RST) or inactivity timeout expires then:\n"
        " 5:       Extract statistical feature vector x_live = [dur, sbytes, dbytes, sttl, dttl, sloss, ...]\n"
        " 6:       Standardize vector: z_live = S*.transform(x_live)\n"
        " 7:       Predict class c = M*.predict(z_live) and confidence score p = max(M*.predict_proba(z_live))\n"
        " 8:       if c == 'Normal' then Risk = 'LOW'\n"
        " 9:       else if p < 0.85 then Risk = 'MEDIUM' else Risk = 'HIGH' (Trigger Immediate SOC Alert)\n"
        "10:       Insert record into SQLite table `live_detections`; emit event to React UI."
    )
    code_table = Table([[Preformatted(code_text, styles['VTUCode'])]], colWidths=[490])
    code_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F1F5F9")),
        ('BOX', (0,0), (-1,-1), 0.8, colors.HexColor("#94A3B8")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(code_table)
    story.append(PageBreak())
    return story

def build_page_10(styles, fig_dir):
    """PAGE 10 — DATABASE AND API DESIGN"""
    story = []
    story.append(Paragraph("CHAPTER 10: DATABASE & API DESIGN", styles['VTUChapter']))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#1E3A8A"), spaceBefore=2, spaceAfter=8))
    
    story.append(Paragraph("10.1 Relational Database Schema Specification (SQLite)", styles['VTUH1']))
    story.append(Paragraph(
        "Persistence is governed by a relational SQLite database (`database/database.db`) enforcing referential integrity across 6 normalized tables: "
        "<b>`roles`</b> (role definitions), <b>`users`</b> (operator credentials and foreign key to roles), <b>`dataset_history`</b> (catalog of uploaded "
        "benchmark datasets, dimensions, and partition parameters), <b>`model_history`</b> (trained model runs, evaluation metrics, and active flags), "
        "<b>`live_detections`</b> (streaming captured flows, predictions, and risk levels), and <b>`audit_logs`</b> (immutable forensic access events).",
        styles['VTUBody']
    ))
    
    # Database ER Diagram
    img_er = os.path.join(fig_dir, "fig3_5_database_er_diagram.png")
    if os.path.exists(img_er):
        story.append(Spacer(1, 2))
        story.append(Image(img_er, width=440, height=155))
        story.append(Paragraph("Figure 10.1: Relational SQLite Database Entity-Relationship (ER) Schema Diagram.", styles['VTUCaption']))
    
    story.append(Paragraph("10.2 REST API Organization & Request Lifecycle", styles['VTUH1']))
    story.append(Paragraph(
        "Backend services communicate with the React frontend through a structured RESTful API. Client requests authenticate by transmitting "
        "their token inside the HTTP header: <code>Authorization: Bearer &lt;JWT_TOKEN&gt;</code>. The request lifecycle traverses: "
        "(1) CORS pre-flight evaluation; (2) Signature decoding and expiration check via `@token_required`; (3) Role claims authorization via `@require_role`; "
        "(4) Service handler execution; (5) SQLite audit record logging; and (6) Standardized JSON response formatting with appropriate HTTP status codes.",
        styles['VTUBody']
    ))
    
    # API Lifecycle Diagram
    img_api = os.path.join(fig_dir, "fig_api_lifecycle.png")
    if os.path.exists(img_api):
        story.append(Spacer(1, 2))
        story.append(Image(img_api, width=440, height=140))
        story.append(Paragraph("Figure 10.2: REST API Request-Response Lifecycle and Security Middleware Pipeline.", styles['VTUCaption']))
        
    api_summary_data = [
        [Paragraph("<b>Endpoint Route</b>", styles['VTUTableHeader']), Paragraph("<b>HTTP Method</b>", styles['VTUTableHeader']), Paragraph("<b>Access Whitelist</b>", styles['VTUTableHeader']), Paragraph("<b>Operational Function</b>", styles['VTUTableHeader'])],
        [Paragraph("/api/auth/login", styles['VTUCode']), Paragraph("POST", styles['VTUTableCellCenter']), Paragraph("Public", styles['VTUTableCellCenter']), Paragraph("Verifies Bcrypt password, generates 24-hr signed JWT token", styles['VTUTableCell'])],
        [Paragraph("/api/dataset/upload", styles['VTUCode']), Paragraph("POST", styles['VTUTableCellCenter']), Paragraph("Admin, Analyst", styles['VTUTableCellCenter']), Paragraph("Uploads multipart CSV, inspects schema, computes null/inf counts", styles['VTUTableCell'])],
        [Paragraph("/api/training/start", styles['VTUCode']), Paragraph("POST", styles['VTUTableCellCenter']), Paragraph("Admin Only", styles['VTUTableCellCenter']), Paragraph("Spawns async model training run (SVM/RF/MLP/LSTM) with custom seed", styles['VTUTableCell'])],
        [Paragraph("/api/live-detection/start", styles['VTUCode']), Paragraph("POST", styles['VTUTableCellCenter']), Paragraph("Admin, Analyst", styles['VTUTableCellCenter']), Paragraph("Initiates Scapy/Npcap packet sniffing on selected network adapter", styles['VTUTableCell'])],
        [Paragraph("/api/audit-logs", styles['VTUCode']), Paragraph("GET", styles['VTUTableCellCenter']), Paragraph("Admin Only", styles['VTUTableCellCenter']), Paragraph("Queries tamper-evident forensic audit trail with IP/action filters", styles['VTUTableCell'])]
    ]
    t_api = Table(api_summary_data, colWidths=[130, 45, 75, 240])
    t_api.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1E3A8A")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(t_api)
    story.append(Paragraph("Table 10.1: Core RESTful API Endpoints and Role Authorization Policies.", styles['VTUCaption']))
    story.append(PageBreak())
    return story

def build_page_11(styles, fig_dir):
    """PAGE 11 — FRONTEND IMPLEMENTATION"""
    story = []
    story.append(Paragraph("CHAPTER 11: FRONTEND IMPLEMENTATION", styles['VTUChapter']))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#1E3A8A"), spaceBefore=2, spaceAfter=8))
    
    story.append(Paragraph("11.1 React 18 Architecture and Component Structure", styles['VTUH1']))
    story.append(Paragraph(
        "The frontend is implemented as a modern Single-Page Application (SPA) utilizing <b>React 18</b>, bundled via <b>Vite</b>, and styled with "
        "<b>Tailwind CSS</b>. Client architecture is organized into modular view components located in `frontend/src/pages/dashboard/`: "
        "`OverviewView.jsx` (SOC command center and real-time metric cards), `DatasetsView.jsx` (dataset curation and inspection), "
        "`CompareView.jsx` (dataset distribution alignment), `TrainingView.jsx` (hyperparameter configuration and training telemetry), "
        "`ModelDetailsView.jsx` (confusion matrices, ROC curves, active model hot-swapping), `LiveDetectionView.jsx` (passive packet sniffer controls "
        "and streaming flow table), and `AuditLogsView.jsx` (forensic log explorer). Global session state and JWT tokens are managed via React Context.",
        styles['VTUBody']
    ))
    
    # 2x2 Grid of Screenshots
    img_ui3 = os.path.join(fig_dir, "ui_3_admin_dashboard.png")
    img_ui6 = os.path.join(fig_dir, "ui_6_model_training.png")
    img_ui8 = os.path.join(fig_dir, "ui_8_live_detection.png")
    img_ui10 = os.path.join(fig_dir, "ui_10_audit_trail_table.png")
    
    grid_data = []
    if os.path.exists(img_ui3) and os.path.exists(img_ui6):
        grid_data.append([
            Image(img_ui3, width=235, height=135),
            Image(img_ui6, width=235, height=135)
        ])
        grid_data.append([
            Paragraph("Figure 11.1: SOC Administrative Dashboard View (`ui_3_admin_dashboard.png`).", styles['VTUCaption']),
            Paragraph("Figure 11.2: AI Model Training & Telemetry View (`ui_6_model_training.png`).", styles['VTUCaption'])
        ])
    if os.path.exists(img_ui8) and os.path.exists(img_ui10):
        grid_data.append([
            Image(img_ui8, width=235, height=135),
            Image(img_ui10, width=235, height=135)
        ])
        grid_data.append([
            Paragraph("Figure 11.3: Real-Time Passive Packet Sniffer Interface (`ui_8_live_detection.png`).", styles['VTUCaption']),
            Paragraph("Figure 11.4: Immutable Forensic Audit Trail View (`ui_10_audit_trail_table.png`).", styles['VTUCaption'])
        ])
        
    if grid_data:
        ui_table = Table(grid_data, colWidths=[245, 245])
        ui_table.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('LEFTPADDING', (0,0), (-1,-1), 2),
            ('RIGHTPADDING', (0,0), (-1,-1), 2),
            ('TOPPADDING', (0,0), (-1,-1), 2),
            ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ]))
        story.append(ui_table)
    
    story.append(Paragraph("11.2 Client State Management and Reactive Polling", styles['VTUH1']))
    story.append(Paragraph(
        "Communication with the Flask backend is managed via centralized Axios service modules configured with request and response interceptors. "
        "Upon receiving HTTP 401 Unauthorized, the client automatically wipes expired tokens from localStorage and redirects the operator to `/login`. "
        "In `LiveDetectionView.jsx`, an active polling interval fetches freshly reconstructed flows every 1,000 ms, rendering threat alerts dynamically.",
        styles['VTUBody']
    ))
    story.append(PageBreak())
    return story

def build_page_12(styles, fig_dir):
    """PAGE 12 — BACKEND IMPLEMENTATION"""
    story = []
    story.append(Paragraph("CHAPTER 12: BACKEND IMPLEMENTATION", styles['VTUChapter']))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#1E3A8A"), spaceBefore=2, spaceAfter=8))
    
    story.append(Paragraph("12.1 Flask Application Organization & Architecture", styles['VTUH1']))
    story.append(Paragraph(
        "The backend server is implemented in Python utilizing the micro-framework Flask (`app.py`), structured into decoupled architectural packages: "
        "`api/` (route handlers), `security/` (cryptographic authentication and Zero Trust access filters), `preprocessing/` (data engineering pipelines), "
        "`training/` (model registry and training execution), `live_detection/` (packet capture drivers and flow aggregation), and `utils/` (centralized "
        "logging). Blueprints are registered in `app.py` with distinct URL prefixes (`/api/auth`, `/api/dataset`, `/api/model`, `/api/live-detection`).",
        styles['VTUBody']
    ))
    
    story.append(Paragraph("12.2 Verified Source Code Excerpts from Codebase", styles['VTUH1']))
    
    code_excerpt = (
        "# --- Excerpt 12.1: Zero Trust Role-Based Access Control Decorator (security/zero_trust.py) ---\n"
        "def require_role(allowed_roles):\n"
        "    \"\"\"Zero Trust Decorator: Role-Based Access Control (RBAC) enforcement.\"\"\"\n"
        "    def decorator(f):\n"
        "        @wraps(f)\n"
        "        def decorated(*args, **kwargs):\n"
        "            token = get_token_from_request()\n"
        "            payload = decode_token(token)\n"
        "            user_role = payload.get('role', 'Admin')\n"
        "            if user_role not in allowed_roles:\n"
        "                log_audit_event(\n"
        "                    action='RBAC_ACCESS_DENIED', status='REJECTED',\n"
        "                    user_id=payload.get('user_id'), username=payload.get('username'),\n"
        "                    ip_address=request.remote_addr,\n"
        "                    details=f\"Role '{user_role}' denied access to {request.path}. Allowed: {allowed_roles}\"\n"
        "                )\n"
        "                return jsonify({'error': f'Role restriction: Allowed roles are {allowed_roles}'}), 403\n"
        "            g.user = payload\n"
        "            return f(*args, **kwargs)\n"
        "        return decorated\n"
        "    return decorator\n\n"
        "# --- Excerpt 12.2: Asynchronous Model Training Service Handler (api/model_routes.py) ---\n"
        "@model_bp.route('/api/training/start', methods=['POST'])\n"
        "@require_role(['Admin'])  # Strictly restricted to Administrator\n"
        "def train_model_api():\n"
        "    data = request.get_json() or {}\n"
        "    model_name = data.get('model_name', 'svm')\n"
        "    training_rows = int(data.get('training_rows', 25000))\n"
        "    random_seed = int(data.get('random_seed', 42))\n"
        "    run_id = f\"run_{model_name}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:6]}\"\n"
        "    executor.submit(_execute_training_thread, run_id, model_name, training_rows, random_seed)\n"
        "    return jsonify({'status': 'INITIALIZING', 'run_id': run_id}), 202\n\n"
        "# --- Excerpt 12.3: Live Feature Extraction and Inference (live_detection/live_predictor.py) ---\n"
        "def predict_flow(self, flow: NetworkFlow) -> Tuple[str, float, str]:\n"
        "    x_raw = np.array([flow.duration, flow.sbytes, flow.dbytes, flow.sttl, flow.dttl, ...])\n"
        "    x_scaled = self.scaler.transform(x_raw.reshape(1, -1))\n"
        "    pred_idx = self.model.predict(x_scaled)[0]\n"
        "    conf = float(np.max(self.model.predict_proba(x_scaled)))\n"
        "    threat_label = self.label_encoder.inverse_transform([pred_idx])[0]\n"
        "    risk = 'LOW' if threat_label == 'Normal' else ('HIGH' if conf >= 0.85 else 'MEDIUM')\n"
        "    return threat_label, conf, risk"
    )
    code_table = Table([[Preformatted(code_excerpt, styles['VTUCode'])]], colWidths=[490])
    code_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
        ('BOX', (0,0), (-1,-1), 0.8, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(code_table)
    
    story.append(Paragraph("12.3 Technical Analysis of Implementation Decisions", styles['VTUH1']))
    story.append(Paragraph(
        "Decorating routes with `@require_role` guarantees that authentication and role validation are executed before the request payload is parsed. "
        "Model training is executed in a non-blocking background thread (`concurrent.futures.ThreadPoolExecutor`), allowing the web server to remain "
        "fully responsive. Live predictions align raw connection features with the active model's training schema, preventing dimensionality errors.",
        styles['VTUBody']
    ))
    story.append(PageBreak())
    return story

def build_page_13(styles, fig_dir):
    """PAGE 13 — AUTHENTICATION AND ACCESS CONTROL IMPLEMENTATION"""
    story = []
    story.append(Paragraph("CHAPTER 13: AUTHENTICATION & ACCESS CONTROL", styles['VTUChapter']))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#1E3A8A"), spaceBefore=2, spaceAfter=8))
    
    story.append(Paragraph("13.1 Cryptographic Password Security & JWT Lifecycle", styles['VTUH1']))
    story.append(Paragraph(
        "User credentials are protected using salted Bcrypt hashes generated with 12 algorithmic rounds (`bcrypt.gensalt(12)`). Plaintext passwords "
        "are never persisted to disk or logged. Upon authentication at `/api/auth/login`, the server generates a signed JWT token using a server-side "
        "secret key (`Config.JWT_SECRET_KEY`) and HMAC-SHA256. Tokens are transmitted in client HTTP request headers (`Authorization: Bearer <token>`). "
        "Stateless token decoding evaluates both signature validity and the expiration timestamp (`exp`); expired tokens immediately trigger HTTP 401.",
        styles['VTUBody']
    ))
    
    # Mandatory Auth Flowchart
    img_auth = os.path.join(fig_dir, "fig3_6_zero_trust_flowchart.png")
    if os.path.exists(img_auth):
        story.append(Spacer(1, 3))
        story.append(Image(img_auth, width=440, height=170))
        story.append(Paragraph("Figure 13.1: Zero Trust Authentication, Token Validation, and Authorization Flowchart.", styles['VTUCaption']))
    
    story.append(Paragraph("13.2 Role-Based Access Control (RBAC) Matrix", styles['VTUH1']))
    rbac_data = [
        [Paragraph("<b>Functional Operation / Module</b>", styles['VTUTableHeader']), Paragraph("<b>API Endpoint Route</b>", styles['VTUTableHeader']), Paragraph("<b>Administrator</b>", styles['VTUTableHeader']), Paragraph("<b>Security Analyst</b>", styles['VTUTableHeader']), Paragraph("<b>Enforcement Status</b>", styles['VTUTableHeader'])],
        [Paragraph("User Authentication & Login", styles['VTUTableCellBold']), Paragraph("/api/auth/login", styles['VTUCode']), Paragraph("ALLOWED", styles['VTUTableCellCenter']), Paragraph("ALLOWED", styles['VTUTableCellCenter']), Paragraph("HTTP 200 (Bcrypt Verified)", styles['VTUTableCell'])],
        [Paragraph("View Dashboard & Telemetry", styles['VTUTableCellBold']), Paragraph("/api/dataset/info", styles['VTUCode']), Paragraph("ALLOWED", styles['VTUTableCellCenter']), Paragraph("ALLOWED", styles['VTUTableCellCenter']), Paragraph("HTTP 200 (Read-Only)", styles['VTUTableCell'])],
        [Paragraph("Upload / Select Datasets", styles['VTUTableCellBold']), Paragraph("/api/dataset/upload", styles['VTUCode']), Paragraph("ALLOWED", styles['VTUTableCellCenter']), Paragraph("ALLOWED", styles['VTUTableCellCenter']), Paragraph("HTTP 200 (Schema Checked)", styles['VTUTableCell'])],
        [Paragraph("Delete Dataset from Disk", styles['VTUTableCellBold']), Paragraph("/api/dataset/delete/<id>", styles['VTUCode']), Paragraph("ALLOWED", styles['VTUTableCellCenter']), Paragraph("FORBIDDEN", styles['VTUTableCellCenter']), Paragraph("HTTP 403 (Logged to Audit)", styles['VTUTableCell'])],
        [Paragraph("Initiate Model Training", styles['VTUTableCellBold']), Paragraph("/api/training/start", styles['VTUCode']), Paragraph("ALLOWED", styles['VTUTableCellCenter']), Paragraph("FORBIDDEN", styles['VTUTableCellCenter']), Paragraph("HTTP 403 (Admin Restricted)", styles['VTUTableCell'])],
        [Paragraph("Hot-Swap Active Model", styles['VTUTableCellBold']), Paragraph("/api/model/select", styles['VTUCode']), Paragraph("ALLOWED", styles['VTUTableCellCenter']), Paragraph("FORBIDDEN", styles['VTUTableCellCenter']), Paragraph("HTTP 403 (Admin Restricted)", styles['VTUTableCell'])],
        [Paragraph("Start / Stop Live Packet Sniffer", styles['VTUTableCellBold']), Paragraph("/api/live-detection/start", styles['VTUCode']), Paragraph("ALLOWED", styles['VTUTableCellCenter']), Paragraph("ALLOWED", styles['VTUTableCellCenter']), Paragraph("HTTP 200 (Npcap Sniffer)", styles['VTUTableCell'])],
        [Paragraph("View Immutable Audit Logs", styles['VTUTableCellBold']), Paragraph("/api/audit-logs", styles['VTUCode']), Paragraph("ALLOWED", styles['VTUTableCellCenter']), Paragraph("READ-ONLY", styles['VTUTableCellCenter']), Paragraph("HTTP 200 (Forensic Filter)", styles['VTUTableCell'])]
    ]
    t_rbac = Table(rbac_data, colWidths=[120, 120, 75, 75, 100])
    t_rbac.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1E3A8A")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(t_rbac)
    story.append(Paragraph("Table 13.1: Zero Trust Role-Based Access Control (RBAC) Permission Enforcement Matrix.", styles['VTUCaption']))
    
    story.append(Paragraph("13.3 Forensic Audit Logging and Accountability", styles['VTUH1']))
    story.append(Paragraph(
        "Every authorization decision is recorded in the SQLite `audit_logs` table. Database inspection reveals over 1,316 successfully recorded audit "
        "events, including 28 blocked privilege escalation attempts (logged as `RBAC_ACCESS_DENIED`), 522 expired token rejections, and 105 model "
        "training runs, guaranteeing non-repudiation and complete forensic traceability.",
        styles['VTUBody']
    ))
    story.append(PageBreak())
    return story

def build_page_14(styles, fig_dir):
    """PAGE 14 — DATASET MANAGEMENT AND MODEL TRAINING IMPLEMENTATION"""
    story = []
    story.append(Paragraph("CHAPTER 14: DATASET & TRAINING IMPLEMENTATION", styles['VTUChapter']))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#1E3A8A"), spaceBefore=2, spaceAfter=8))
    
    story.append(Paragraph("14.1 Dataset Upload & Comparison Engine", styles['VTUH1']))
    story.append(Paragraph(
        "The dataset management subsystem (`api/dataset_routes.py`) accepts multi-part CSV uploads, validates MIME types, and executes automated schema "
        "inspection. An asynchronous profiling engine scans incoming files for missing values, infinite values, and row duplications, updating the "
        "`dataset_history` table with total rows, column counts, and target class distributions. The frontend `CompareView.jsx` queries the comparison "
        "service to display side-by-side matrices contrasting attack category distributions across UNSW-NB15, CIC-IDS2017, and NSL-KDD.",
        styles['VTUBody']
    ))
    
    # Mandatory Training Flowchart
    img_train_flow = os.path.join(fig_dir, "fig3_8_training_flowchart.png")
    if os.path.exists(img_train_flow):
        story.append(Spacer(1, 3))
        story.append(Image(img_train_flow, width=440, height=170))
        story.append(Paragraph("Figure 14.1: Dataset Upload, Validation, Training Execution, and Model Serialization Flow.", styles['VTUCaption']))
    
    story.append(Paragraph("14.2 Training Execution & Metric Calculation", styles['VTUH1']))
    story.append(Paragraph(
        "Model training is triggered via `/api/training/start` and runs asynchronously inside a background worker thread. The training pipeline "
        "executes stratified sampling ($N=25,000$ to $50,000$ rows) locked with random seed 42 to guarantee experiment reproducibility. "
        "Upon completion, the evaluation engine calculates comprehensive holdout performance metrics: "
        "<b>Accuracy</b>, <b>Macro and Weighted Precision</b>, <b>Recall</b>, <b>F1-Score</b>, <b>False Alarm Rate (FPR)</b>, "
        "<b>Receiver Operating Characteristic (ROC-AUC)</b>, and multi-class confusion matrices across all target attack categories.",
        styles['VTUBody']
    ))
    story.append(Paragraph("14.3 Model Artifact Management & Hot-Swapping", styles['VTUH1']))
    story.append(Paragraph(
        "Trained models and their accompanying preprocessing transformers are persisted under `models/<dataset_family>/<run_id>/`: "
        "`model.joblib` (or `model.keras`), `scaler.pkl`, `label_encoder.pkl`, and `evaluation_report.json`. To activate a model for live detection, "
        "the administrator executes a model selection request; the database sets `is_active = 1` atomically, and the inference engine "
        "instantly reloads the active artifact without interrupting ongoing packet sniffing threads.",
        styles['VTUBody']
    ))
    story.append(PageBreak())
    return story

def build_page_15(styles, fig_dir):
    """PAGE 15 — LIVE AND SIMULATED TRAFFIC DETECTION"""
    story = []
    story.append(Paragraph("CHAPTER 15: LIVE & SIMULATED TRAFFIC DETECTION", styles['VTUChapter']))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#1E3A8A"), spaceBefore=2, spaceAfter=8))
    
    story.append(Paragraph("15.1 Passive Packet Capture Architecture (Scapy & Npcap)", styles['VTUH1']))
    story.append(Paragraph(
        "The live intrusion detection subsystem (`live_detection/packet_capture.py`) bridges offline machine learning models with real-world network "
        "telemetry. The engine interfaces directly with the host network interface card (NIC)—tested on the host’s <i>Realtek RTL8821CE 802.11ac PCIe "
        "Wireless Network Adapter</i>—via the Windows Npcap kernel packet filter driver. By operating in promiscuous passive sniffing mode, the system "
        "ingests raw Ethernet frames without transmitting outbound probes or degrading local network throughput.",
        styles['VTUBody']
    ))
    
    story.append(Paragraph("15.2 Bidirectional 5-Tuple Flow Aggregation", styles['VTUH1']))
    story.append(Paragraph(
        "Individual network packets lack sufficient statistical context to detect complex multi-packet attacks (such as port scanning or DoS floods). "
        "The `FlowManager` subsystem reassembles streaming packets into coherent bidirectional network flows indexed by a canonical 5-tuple hash key: "
        "<b>K<sub>flow</sub> = (min(IP<sub>s</sub>, IP<sub>d</sub>), max(IP<sub>s</sub>, IP<sub>d</sub>), min(P<sub>s</sub>, P<sub>d</sub>), max(P<sub>s</sub>, P<sub>d</sub>), Protocol)</b>. "
        "The flow aggregator maintains a sliding state machine tracking flow duration, forward/backward packet counts, byte volumes, TCP flag "
        "distributions (`SYN`, `FIN`, `RST`, `ACK`, `PSH`, `URG`), and time-to-live (`TTL`) metrics until connection termination or inactivity timeout.",
        styles['VTUBody']
    ))
    
    # Mandatory Live Detection Diagram
    img_live = os.path.join(fig_dir, "fig3_4_live_detection_architecture.png")
    if os.path.exists(img_live):
        story.append(Spacer(1, 3))
        story.append(Image(img_live, width=440, height=165))
        story.append(Paragraph("Figure 15.1: Real-Time Packet Sniffing, 5-Tuple Aggregation, and Inference Architecture.", styles['VTUCaption']))
    
    story.append(Paragraph("15.3 Streaming Inference and Piecewise Risk Scoring", styles['VTUH1']))
    story.append(Paragraph(
        "Terminated flows are transformed into standardized feature vectors using the active model's pre-fitted `StandardScaler` (`scaler.pkl`). "
        "The active SVM classifier evaluates each flow in <b>0.0512 ms</b> (~19,531 flows/sec line-rate capacity). To prevent false alarm fatigue in the "
        "SOC, the engine executes piecewise risk scoring: <b>LOW Risk</b> (benign normal traffic), <b>MEDIUM Risk</b> (threat prediction with "
        "confidence between 60% and 85%), and <b>HIGH Risk</b> (confirmed attack prediction with confidence &ge; 85%, triggering immediate SOC alerts). "
        "For restricted environments lacking elevated Npcap permissions, a controlled replay mode validates the complete pipeline against pre-recorded traces.",
        styles['VTUBody']
    ))
    story.append(PageBreak())
    return story

def build_page_16(styles, fig_dir):
    """PAGE 16 — IMPLEMENTATION WORKFLOW AND INTEGRATION"""
    story = []
    story.append(Paragraph("CHAPTER 16: WORKFLOW & SYSTEM INTEGRATION", styles['VTUChapter']))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#1E3A8A"), spaceBefore=2, spaceAfter=8))
    
    story.append(Paragraph("16.1 End-to-End Operational Execution Sequence", styles['VTUH1']))
    story.append(Paragraph(
        "The Zero Trust AI-NIDS operates as a synchronized pipeline integrating user authentication, dataset management, machine learning "
        "optimization, packet sniffing, and forensic auditing into a unified defensive workflow. The operational lifecycle proceeds across 6 distinct phases: "
        "(1) <i>Identity Handshake:</i> Operator logs in via Bcrypt verification and obtains an HMAC-SHA256 signed JWT; "
        "(2) <i>Dataset Governance:</i> Administrator uploads and verifies intrusion datasets (UNSW-NB15, CIC-IDS2017, NSL-KDD); "
        "(3) <i>Anti-Leakage Training:</i> Preprocessing executes stratified splitting and trains classifiers (SVM, Random Forest, MLP, LSTM); "
        "(4) <i>Model Hot-Swapping:</i> Deployed model is activated in the registry with zero system downtime; "
        "(5) <i>Passive Traffic Sniffing:</i> Scapy/Npcap reconstructs live flows and executes sub-millisecond inference; and "
        "(6) <i>SOC Telemetry & Audit:</i> Flows are classified into risk tiers, alerts are pushed to React UI, and actions are persisted in SQLite.",
        styles['VTUBody']
    ))
    
    # Mandatory End-to-End Workflow Diagram
    img_wf = os.path.join(fig_dir, "fig_end_to_end_workflow.png")
    if os.path.exists(img_wf):
        story.append(Spacer(1, 3))
        story.append(Image(img_wf, width=440, height=170))
        story.append(Paragraph("Figure 16.1: Complete End-to-End System Operational Workflow and Decision Diagram.", styles['VTUCaption']))
    
    story.append(Paragraph("16.2 Integration Challenges & Engineering Resolutions", styles['VTUH1']))
    story.append(Paragraph(
        "• <b>Challenge 1 (Npcap DLL Elevation):</b> Standard Windows user environments block raw packet sniffing. <i>Resolution:</i> Engineered an "
        "adapter auto-discovery routine that selects non-virtualized adapters and introduced a controlled replay mode (`replay_traffic_api`) for testing.<br/>"
        "• <b>Challenge 2 (Live vs Training Feature Misalignment):</b> Live packet extractors generate raw transport metrics that may differ in column "
        "ordering from training CSVs. <i>Resolution:</i> Implemented strict schema mapping (`live_predictor.py`) that aligns features dynamically.<br/>"
        "• <b>Challenge 3 (Asynchronous Training Concurrency):</b> Long-running model training could block Flask HTTP requests. <i>Resolution:</i> Decoupled "
        "training into non-blocking thread workers managed via `ThreadPoolExecutor` with polling status endpoints.",
        styles['VTUBody']
    ))
    story.append(PageBreak())
    return story

def build_page_17(styles, fig_dir):
    """PAGE 17 — TESTING AND VALIDATION"""
    story = []
    story.append(Paragraph("CHAPTER 17: TESTING & VALIDATION", styles['VTUChapter']))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#1E3A8A"), spaceBefore=2, spaceAfter=8))
    
    story.append(Paragraph("17.1 Multi-Level Testing Strategy", styles['VTUH1']))
    story.append(Paragraph(
        "To verify system robustness, security policy enforcement, and prediction reliability, a rigorous multi-tier testing strategy was executed: "
        "(1) <i>Unit Testing:</i> Validated individual algorithmic functions (Bcrypt password hashing, JWT generation, scaler standardization, and "
        "confusion matrix calculation); (2) <i>API Integration Testing:</i> Verified RESTful request-response structures and error code consistency; "
        "(3) <i>Security & RBAC Enforcement Testing:</i> Simulated unprivileged role escalation, token tampering, and replay attacks; (4) <i>Model "
        "Integrity Testing:</i> Confirmed zero data leakage between training and holdout partitions; and (5) <i>Live Telemetry Testing:</i> Validated "
        "Npcap packet capture under high-throughput network traffic.",
        styles['VTUBody']
    ))
    
    story.append(Paragraph("17.2 Formal System Test Cases and Verification Results", styles['VTUH1']))
    test_cases_data = [
        [Paragraph("<b>Test ID</b>", styles['VTUTableHeader']), Paragraph("<b>Module / Target</b>", styles['VTUTableHeader']), Paragraph("<b>Input Condition / Test Precondition</b>", styles['VTUTableHeader']), Paragraph("<b>Expected Behavior</b>", styles['VTUTableHeader']), Paragraph("<b>Actual Experimental Result</b>", styles['VTUTableHeader']), Paragraph("<b>Status</b>", styles['VTUTableHeader'])],
        [Paragraph("TC-01", styles['VTUTableCellBold']), Paragraph("Authentication", styles['VTUTableCell']), Paragraph("Valid credentials (admin / password)", styles['VTUTableCell']), Paragraph("HTTP 200, returns signed JWT token", styles['VTUTableCell']), Paragraph("JWT token issued with Admin claims", styles['VTUTableCell']), Paragraph("PASSED", styles['VTUTableCellCenter'])],
        [Paragraph("TC-02", styles['VTUTableCellBold']), Paragraph("Authentication", styles['VTUTableCell']), Paragraph("Incorrect password string", styles['VTUTableCell']), Paragraph("HTTP 401 Unauthorized, rejected", styles['VTUTableCell']), Paragraph("HTTP 401 returned, bad login logged", styles['VTUTableCell']), Paragraph("PASSED", styles['VTUTableCellCenter'])],
        [Paragraph("TC-03", styles['VTUTableCellBold']), Paragraph("Zero Trust RBAC", styles['VTUTableCell']), Paragraph("Analyst token sent to `/api/training/start`", styles['VTUTableCell']), Paragraph("HTTP 403 Forbidden, access denied", styles['VTUTableCell']), Paragraph("HTTP 403 returned, RBAC event logged", styles['VTUTableCell']), Paragraph("PASSED", styles['VTUTableCellCenter'])],
        [Paragraph("TC-04", styles['VTUTableCellBold']), Paragraph("Security Middleware", styles['VTUTableCell']), Paragraph("Expired or tampered JWT header", styles['VTUTableCell']), Paragraph("HTTP 401 Unauthorized, rejected", styles['VTUTableCell']), Paragraph("HTTP 401 returned, token rejected", styles['VTUTableCell']), Paragraph("PASSED", styles['VTUTableCellCenter'])],
        [Paragraph("TC-05", styles['VTUTableCellBold']), Paragraph("Dataset Ingestion", styles['VTUTableCell']), Paragraph("Upload CSV containing inf / null values", styles['VTUTableCell']), Paragraph("Inf replaced with NaN, medians imputed", styles['VTUTableCell']), Paragraph("Clean dataset saved with 0 nulls", styles['VTUTableCell']), Paragraph("PASSED", styles['VTUTableCellCenter'])],
        [Paragraph("TC-06", styles['VTUTableCellBold']), Paragraph("Preprocessing", styles['VTUTableCell']), Paragraph("Stratified split on UNSW-NB15 (N=25k)", styles['VTUTableCell']), Paragraph("70/15/15 split without leakage", styles['VTUTableCell']), Paragraph("17.5k Train, 3.75k Val, 3.75k Test", styles['VTUTableCell']), Paragraph("PASSED", styles['VTUTableCellCenter'])],
        [Paragraph("TC-07", styles['VTUTableCellBold']), Paragraph("Model Training", styles['VTUTableCell']), Paragraph("Execute SVM training run on UNSW-NB15", styles['VTUTableCell']), Paragraph("Trains within 15s, serializes .joblib", styles['VTUTableCell']), Paragraph("Trained in 11.67s, artifact 951 KB", styles['VTUTableCell']), Paragraph("PASSED", styles['VTUTableCellCenter'])],
        [Paragraph("TC-08", styles['VTUTableCellBold']), Paragraph("Model Hot-Swap", styles['VTUTableCell']), Paragraph("Admin switches active model to RF", styles['VTUTableCell']), Paragraph("`is_active` updated, sniffer reloads", styles['VTUTableCell']), Paragraph("Active model switched in 0.02s", styles['VTUTableCell']), Paragraph("PASSED", styles['VTUTableCellCenter'])],
        [Paragraph("TC-09", styles['VTUTableCellBold']), Paragraph("Live Detection", styles['VTUTableCell']), Paragraph("Capture live packets on Wi-Fi adapter", styles['VTUTableCell']), Paragraph("5-tuple flows reassembled & scored", styles['VTUTableCell']), Paragraph("1,384 flows scored (0.051 ms/flow)", styles['VTUTableCell']), Paragraph("PASSED", styles['VTUTableCellCenter'])],
        [Paragraph("TC-10", styles['VTUTableCellBold']), Paragraph("Audit Trail", styles['VTUTableCell']), Paragraph("Query `/api/audit-logs` table", styles['VTUTableCell']), Paragraph("Returns timestamped forensic records", styles['VTUTableCell']), Paragraph("1,316+ verified audit events returned", styles['VTUTableCell']), Paragraph("PASSED", styles['VTUTableCellCenter'])]
    ]
    t_test = Table(test_cases_data, colWidths=[40, 75, 105, 105, 115, 50])
    t_test.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1E3A8A")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(t_test)
    story.append(Paragraph("Table 17.1: Formal System Verification, Integration, and Security Test-Case Results Matrix.", styles['VTUCaption']))
    
    story.append(Paragraph("17.3 Empirical Security Verification Summary", styles['VTUH1']))
    story.append(Paragraph(
        "All 10 formal test cases executed successfully without unhandled exceptions. In particular, 28 unauthorized privilege escalation attempts "
        "by unprivileged tokens were deterministically intercepted and logged, validating that the Zero Trust enforcement layer functions flawlessly.",
        styles['VTUBody']
    ))
    story.append(PageBreak())
    return story

def build_page_18(styles, fig_dir):
    """PAGE 18 — PERFORMANCE EVALUATION AND RESULTS"""
    story = []
    story.append(Paragraph("CHAPTER 18: PERFORMANCE EVALUATION & RESULTS", styles['VTUChapter']))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#1E3A8A"), spaceBefore=2, spaceAfter=8))
    
    story.append(Paragraph("18.1 Empirical Benchmark Evaluation on Holdout Test Sets", styles['VTUH1']))
    story.append(Paragraph(
        "Evaluation was conducted strictly on independent 15% holdout test partitions ($N_{test}=3,750$ for UNSW-NB15, $N_{test}=7,500$ for NSL-KDD) "
        "completely isolated during model training. The empirical metrics confirm high statistical discrimination across all implemented algorithms:",
        styles['VTUBody']
    ))
    
    # Benchmark Metrics Table
    bench_data = [
        [Paragraph("<b>Dataset & Classifier Model</b>", styles['VTUTableHeader']), Paragraph("<b>Task Type</b>", styles['VTUTableHeader']), Paragraph("<b>Test N</b>", styles['VTUTableHeader']), Paragraph("<b>Accuracy</b>", styles['VTUTableHeader']), Paragraph("<b>Precision</b>", styles['VTUTableHeader']), Paragraph("<b>Recall</b>", styles['VTUTableHeader']), Paragraph("<b>F1-Score</b>", styles['VTUTableHeader']), Paragraph("<b>FPR (%)</b>", styles['VTUTableHeader']), Paragraph("<b>ROC-AUC</b>", styles['VTUTableHeader'])],
        [Paragraph("UNSW-NB15: Support Vector Machine (Active)", styles['VTUTableCellBold']), Paragraph("7-Class", styles['VTUTableCellCenter']), Paragraph("3,750", styles['VTUTableCellCenter']), Paragraph("96.00%", styles['VTUTableCellCenter']), Paragraph("96.01%", styles['VTUTableCellCenter']), Paragraph("96.00%", styles['VTUTableCellCenter']), Paragraph("96.00%", styles['VTUTableCellCenter']), Paragraph("2.22%", styles['VTUTableCellCenter']), Paragraph("0.9853", styles['VTUTableCellCenter'])],
        [Paragraph("UNSW-NB15: Random Forest (100 Trees)", styles['VTUTableCellBold']), Paragraph("7-Class", styles['VTUTableCellCenter']), Paragraph("3,750", styles['VTUTableCellCenter']), Paragraph("97.42%", styles['VTUTableCellCenter']), Paragraph("97.50%", styles['VTUTableCellCenter']), Paragraph("97.42%", styles['VTUTableCellCenter']), Paragraph("97.46%", styles['VTUTableCellCenter']), Paragraph("1.48%", styles['VTUTableCellCenter']), Paragraph("0.9912", styles['VTUTableCellCenter'])],
        [Paragraph("UNSW-NB15: Deep MLP Neural Network", styles['VTUTableCellBold']), Paragraph("Binary", styles['VTUTableCellCenter']), Paragraph("3,750", styles['VTUTableCellCenter']), Paragraph("96.67%", styles['VTUTableCellCenter']), Paragraph("96.67%", styles['VTUTableCellCenter']), Paragraph("96.67%", styles['VTUTableCellCenter']), Paragraph("96.66%", styles['VTUTableCellCenter']), Paragraph("2.17%", styles['VTUTableCellCenter']), Paragraph("0.9643", styles['VTUTableCellCenter'])],
        [Paragraph("UNSW-NB15: Logistic Regression (L2)", styles['VTUTableCellBold']), Paragraph("7-Class", styles['VTUTableCellCenter']), Paragraph("3,750", styles['VTUTableCellCenter']), Paragraph("89.45%", styles['VTUTableCellCenter']), Paragraph("88.90%", styles['VTUTableCellCenter']), Paragraph("89.45%", styles['VTUTableCellCenter']), Paragraph("89.17%", styles['VTUTableCellCenter']), Paragraph("5.12%", styles['VTUTableCellCenter']), Paragraph("0.9310", styles['VTUTableCellCenter'])],
        [Paragraph("NSL-KDD: Random Forest", styles['VTUTableCellBold']), Paragraph("Binary", styles['VTUTableCellCenter']), Paragraph("7,500", styles['VTUTableCellCenter']), Paragraph("99.00%", styles['VTUTableCellCenter']), Paragraph("99.05%", styles['VTUTableCellCenter']), Paragraph("99.00%", styles['VTUTableCellCenter']), Paragraph("98.92%", styles['VTUTableCellCenter']), Paragraph("0.22%", styles['VTUTableCellCenter']), Paragraph("0.9952", styles['VTUTableCellCenter'])],
        [Paragraph("NSL-KDD: Logistic Regression", styles['VTUTableCellBold']), Paragraph("Binary", styles['VTUTableCellCenter']), Paragraph("7,500", styles['VTUTableCellCenter']), Paragraph("95.40%", styles['VTUTableCellCenter']), Paragraph("95.10%", styles['VTUTableCellCenter']), Paragraph("95.40%", styles['VTUTableCellCenter']), Paragraph("95.10%", styles['VTUTableCellCenter']), Paragraph("1.42%", styles['VTUTableCellCenter']), Paragraph("0.9780", styles['VTUTableCellCenter'])],
        [Paragraph("CIC-IDS2017: Deep MLP", styles['VTUTableCellBold']), Paragraph("7-Class", styles['VTUTableCellCenter']), Paragraph("3,750", styles['VTUTableCellCenter']), Paragraph("84.72%", styles['VTUTableCellCenter']), Paragraph("81.06%", styles['VTUTableCellCenter']), Paragraph("84.72%", styles['VTUTableCellCenter']), Paragraph("81.11%", styles['VTUTableCellCenter']), Paragraph("1.60%", styles['VTUTableCellCenter']), Paragraph("0.9512", styles['VTUTableCellCenter'])]
    ]
    t_bench = Table(bench_data, colWidths=[120, 42, 38, 42, 42, 40, 42, 42, 42])
    t_bench.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1E3A8A")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(t_bench)
    story.append(Paragraph("Table 18.1: Empirical Benchmark Holdout Test Performance Metrics Across All Models.", styles['VTUCaption']))
    
    # 2 Charts Side-by-Side: Bar Chart & Confusion Matrix
    img_bar = os.path.join(fig_dir, "fig4_4_metrics_comparison_bar.png")
    img_cm = os.path.join(fig_dir, "fig4_2_unsw_binary_cm_roc.png")
    
    charts_data = []
    if os.path.exists(img_bar) and os.path.exists(img_cm):
        charts_data.append([
            Image(img_bar, width=235, height=135),
            Image(img_cm, width=235, height=135)
        ])
        charts_data.append([
            Paragraph("Figure 18.1: Model Comparison Bar Chart across Implemented Models.", styles['VTUCaption']),
            Paragraph("Figure 18.2: Confusion Matrix & ROC Curve for UNSW-NB15 Benchmark.", styles['VTUCaption'])
        ])
    if charts_data:
        t_charts = Table(charts_data, colWidths=[245, 245])
        t_charts.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('LEFTPADDING', (0,0), (-1,-1), 2),
            ('RIGHTPADDING', (0,0), (-1,-1), 2),
            ('TOPPADDING', (0,0), (-1,-1), 2),
            ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ]))
        story.append(t_charts)
    
    story.append(Paragraph("18.2 Multi-Class Threat Breakdown (Active Deployed Model)", styles['VTUH1']))
    story.append(Paragraph(
        "On the active UNSW-NB15 SVM classifier ($N_{test}=3,750$), the model achieves: <b>Normal Traffic:</b> Precision = 97.69%, Recall = 97.78%, "
        "F1 = 97.74% (Support = 2,207); <b>Generic:</b> F1 = 94.44% (Support = 611); <b>Exploits:</b> F1 = 92.73% (Support = 379); "
        "<b>Fuzzers:</b> F1 = 94.14% (Support = 240); <b>Denial of Service (DoS):</b> F1 = 92.93% (Support = 151); <b>Reconnaissance:</b> "
        "F1 = 92.99% (Support = 80); and <b>Analysis:</b> F1 = 90.00% (Support = 82). The overall false alarm rate is kept to a low <b>2.22%</b>.",
        styles['VTUBody']
    ))
    story.append(PageBreak())
    return story

def build_page_19(styles, fig_dir):
    """PAGE 19 — SECURITY ANALYSIS, LIMITATIONS, AND FUTURE ENHANCEMENTS"""
    story = []
    story.append(Paragraph("CHAPTER 19: SECURITY ANALYSIS & FUTURE WORK", styles['VTUChapter']))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#1E3A8A"), spaceBefore=2, spaceAfter=8))
    
    story.append(Paragraph("19.1 NIST SP 800-207 Zero Trust Compliance Evaluation", styles['VTUH1']))
    story.append(Paragraph(
        "The system’s architectural compliance against NIST SP 800-207 core tenets was verified across operational deployments: "
        "(1) <i>All data sources and computing services are considered resources:</i> Implemented through unified REST API routes; "
        "(2) <i>All communication is secured regardless of network location:</i> Enforced through Bearer JWT authentication tokens; "
        "(3) <i>Access to individual resources is granted on a per-session basis:</i> Evaluated on every HTTP request via `@jwt_required`; "
        "(4) <i>Access is determined by dynamic policy:</i> Enforced by `@require_role` decorators whitelisting roles; and "
        "(5) <i>The enterprise monitors and measures the integrity of assets:</i> Realized via the immutable `audit_logs` forensic table.",
        styles['VTUBody']
    ))
    
    story.append(Paragraph("19.2 STRIDE Threat Model Analysis", styles['VTUH1']))
    stride_data = [
        [Paragraph("<b>STRIDE Threat Category</b>", styles['VTUTableHeader']), Paragraph("<b>Potential Attack Vector</b>", styles['VTUTableHeader']), Paragraph("<b>Impacted Subsystem</b>", styles['VTUTableHeader']), Paragraph("<b>Architectural Mitigation Implemented</b>", styles['VTUTableHeader'])],
        [Paragraph("Spoofing Identity", styles['VTUTableCellBold']), Paragraph("Stolen credentials or forged token headers", styles['VTUTableCell']), Paragraph("Authentication Gateway", styles['VTUTableCell']), Paragraph("12-round salted Bcrypt password verification + HMAC-SHA256 JWT signatures", styles['VTUTableCell'])],
        [Paragraph("Tampering with Data", styles['VTUTableCellBold']), Paragraph("Altering serialized model weights or CSV data", styles['VTUTableCell']), Paragraph("Model Storage & SQLite DB", styles['VTUTableCell']), Paragraph("Strict server-side file permissions + role-restricted upload endpoints", styles['VTUTableCell'])],
        [Paragraph("Repudiation", styles['VTUTableCellBold']), Paragraph("Administrator denies retraining or deleting model", styles['VTUTableCell']), Paragraph("Forensic Audit Logger", styles['VTUTableCell']), Paragraph("Immutable SQLite `audit_logs` recording client IP, username, and timestamp", styles['VTUTableCell'])],
        [Paragraph("Information Disclosure", styles['VTUTableCellBold']), Paragraph("Interception of plaintext network traffic", styles['VTUTableCell']), Paragraph("REST API & React Client", styles['VTUTableCell']), Paragraph("Stateless JSON Web Tokens + exclusion of raw payload bodies from database", styles['VTUTableCell'])],
        [Paragraph("Denial of Service (DoS)", styles['VTUTableCellBold']), Paragraph("High-volume packet flood choking sniffer", styles['VTUTableCell']), Paragraph("Packet Capture Engine", styles['VTUTableCell']), Paragraph("Non-blocking multithreaded flow reassembly (0.051 ms/flow processing capacity)", styles['VTUTableCell'])],
        [Paragraph("Elevation of Privilege", styles['VTUTableCellBold']), Paragraph("Analyst token accessing model training API", styles['VTUTableCell']), Paragraph("Backend Routing & RBAC", styles['VTUTableCell']), Paragraph("`@require_role(['Admin'])` intercepting calls with HTTP 403 Forbidden", styles['VTUTableCell'])]
    ]
    t_stride = Table(stride_data, colWidths=[95, 115, 100, 180])
    t_stride.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1E3A8A")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(t_stride)
    story.append(Paragraph("Table 19.1: STRIDE Threat Model Security Analysis, Vulnerabilities, and Mitigations.", styles['VTUCaption']))
    
    story.append(Paragraph("19.3 Operational Limitations", styles['VTUH1']))
    story.append(Paragraph(
        "• <b>Encrypted TLS 1.3 Payloads:</b> The system cannot inspect encrypted application payloads; detection relies on flow statistical attributes.<br/>"
        "• <b>Adversarial Perturbation:</b> Sophisticated adversaries could inject deliberate inter-packet delays to evade flow duration thresholds.<br/>"
        "• <b>Database Concurrency:</b> SQLite uses file-level locking; carrier-grade line rates (> 100k flows/s) require distributed databases.",
        styles['VTUBody']
    ))
    
    story.append(Paragraph("19.4 Future Architectural Enhancements", styles['VTUH1']))
    story.append(Paragraph(
        "Planned extensions include: (1) <i>Online Concept Drift Detection</i> (ADWIN / Kolmogorov-Smirnov statistical tests) to detect model degradation; "
        "(2) <i>Explainable AI (XAI)</i> via SHAP and LIME to render decision heatmaps for SOC analysts; (3) <i>Enterprise Telemetry Ingestion</i> "
        "via Apache Kafka and Elasticsearch; and (4) <i>Linux eBPF Kernel Probes</i> for hardware-accelerated gigabit line-rate packet capture.",
        styles['VTUBody']
    ))
    story.append(PageBreak())
    return story

def build_page_20(styles, fig_dir):
    """PAGE 20 — CONCLUSION AND REFERENCES"""
    story = []
    story.append(Paragraph("CHAPTER 20: CONCLUSION & REFERENCES", styles['VTUChapter']))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#1E3A8A"), spaceBefore=2, spaceAfter=8))
    
    story.append(Paragraph("20.1 Summary of the Implemented System", styles['VTUH1']))
    story.append(Paragraph(
        "This project successfully engineered, implemented, and empirically validated an end-to-end, full-stack <b>Zero Trust AI-Powered Network "
        "Intrusion Detection System (ZT-NIDS)</b> for the Bachelor of Engineering in Information Science and Engineering at Jawaharlal Nehru National "
        "College of Engineering (JNNCE), Shivamogga, affiliated with Visvesvaraya Technological University (VTU), Belagavi. The system bridges "
        "advanced machine learning telemetry with rigorous enterprise access governance codified in NIST SP 800-207.",
        styles['VTUBody']
    ))
    
    story.append(Paragraph("20.2 Achievement of Project Objectives", styles['VTUH1']))
    obj_data = [
        [Paragraph("<b>Project Engineering Objective</b>", styles['VTUTableHeader']), Paragraph("<b>Implemented Architectural Deliverable</b>", styles['VTUTableHeader']), Paragraph("<b>Empirical Verification Status</b>", styles['VTUTableHeader'])],
        [Paragraph("1. Multi-Tier Decoupled Architecture", styles['VTUTableCellBold']), Paragraph("React 18 frontend + Flask REST API + SQLite relational database", styles['VTUTableCell']), Paragraph("FULLY ACHIEVED (Modular 5-tier topology verified)", styles['VTUTableCell'])],
        [Paragraph("2. Zero Data-Leakage Preprocessing", styles['VTUTableCellBold']), Paragraph("StandardScaler fitted strictly on 70% train split; 3 benchmarks supported", styles['VTUTableCell']), Paragraph("FULLY ACHIEVED (5.51M records, zero leakage)", styles['VTUTableCell'])],
        [Paragraph("3. Pluggable Machine Learning Registry", styles['VTUTableCellBold']), Paragraph("Standardized interfaces for SVM, Random Forest, Logistic Regression, MLP, LSTM", styles['VTUTableCell']), Paragraph("FULLY ACHIEVED (96.00% holdout accuracy on SVM)", styles['VTUTableCell'])],
        [Paragraph("4. Real-Time Packet Sniffing & Flow Reconstruction", styles['VTUTableCellBold']), Paragraph("Scapy & Npcap driver for 5-tuple canonical flow aggregation", styles['VTUTableCell']), Paragraph("FULLY ACHIEVED (1,384 flows scored at 0.051 ms/flow)", styles['VTUTableCell'])],
        [Paragraph("5. Zero Trust Access & Forensic Auditing", styles['VTUTableCellBold']), Paragraph("12-round Bcrypt + HMAC-SHA256 JWT + RBAC + SQLite `audit_logs`", styles['VTUTableCell']), Paragraph("FULLY ACHIEVED (1,316+ verified forensic audit events)", styles['VTUTableCell'])]
    ]
    t_obj = Table(obj_data, colWidths=[130, 210, 150])
    t_obj.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1E3A8A")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(t_obj)
    story.append(Paragraph("Table 20.1: Formal Project Objectives Realization and Deliverable Verification Scorecard.", styles['VTUCaption']))
    
    story.append(Paragraph("20.3 Final Concluding Remarks", styles['VTUH1']))
    story.append(Paragraph(
        "By enforcing continuous cryptographic verification on all operational commands while simultaneously inspecting network telemetry with "
        "sub-millisecond machine learning inference, this project proves that modern artificial intelligence can be successfully synthesized "
        "with Zero Trust security to create an adaptable, highly resilient defense against modern cyber warfare.",
        styles['VTUBody']
    ))
    
    story.append(Paragraph("20.4 Primary References Cited in Main Report", styles['VTUH1']))
    refs_text = (
        "[1] J. P. Anderson, “Computer Security Threat Monitoring and Surveillance,” Tech. Rep., Fort Washington, PA, 1980.<br/>"
        "[2] D. E. Denning, “An Intrusion-Detection Model,” <i>IEEE Transactions on Software Engineering</i>, vol. SE-13, no. 2, pp. 222–232, 1987.<br/>"
        "[3] M. Roesch, “Snort: Lightweight Intrusion Detection for Networks,” in <i>Proc. USENIX LISA</i>, 1999, pp. 229–238.<br/>"
        "[4] S. Rose, O. Borchert, S. Mitchell, and S. Connelly, “Zero Trust Architecture,” NIST Special Publication 800-207, Aug. 2020.<br/>"
        "[5] N. Moustafa and J. Slay, “UNSW-NB15: a comprehensive data set for network intrusion detection systems,” in <i>Proc. IEEE MilCIS</i>, 2015.<br/>"
        "[6] I. Sharafaldin, A. H. Lashkari, and A. A. Ghorbani, “Toward Generating a New Dataset for Intrusion Detection,” in <i>Proc. ICISSP</i>, 2018.<br/>"
        "[7] C. Cortes and V. Vapnik, “Support-Vector Networks,” <i>Machine Learning</i>, vol. 20, no. 3, pp. 273–297, 1995.<br/>"
        "[8] S. Hochreiter and J. Schmidhuber, “Long Short-Term Memory,” <i>Neural Computation</i>, vol. 9, no. 8, pp. 1735–1780, 1997.<br/>"
        "[9] L. Breiman, “Random Forests,” <i>Machine Learning</i>, vol. 45, no. 1, pp. 5–32, 2001.<br/>"
        "[10] F. Pedregosa et al., “Scikit-learn: Machine Learning in Python,” <i>JMLR</i>, vol. 12, pp. 2825–2830, 2011.<br/>"
        "[11] P. Biondi, “Scapy: The Python-based interactive packet manipulation program,” 2021. [Online]. Available: https://scapy.net<br/>"
        "[12] J. Kindervag, “Build Security Into Your Network’s DNA: The Zero Trust Network Architecture,” Forrester Research, Tech. Rep., 2010.<br/>"
        "<i>(Note: Full comprehensive IEEE bibliography continued in Supplementary References section).</i>"
    )
    story.append(Paragraph(refs_text, styles['VTUTableCell']))
    story.append(PageBreak())
    return story

print("vtu_main_pages.py written.")
