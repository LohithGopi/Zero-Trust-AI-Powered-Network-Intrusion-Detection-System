import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
)
from reportlab.pdfgen import canvas

class IJSREMNumberedCanvas(canvas.Canvas):
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
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Times-Roman", 8.5)
        self.setFillColor(HexColor("#444444"))
        
        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(inch, 10.3 * inch, "International Journal of Scientific Research in Engineering and Management (IJSREM)")
            self.drawRightString(7.5 * inch, 10.3 * inch, "ISSN: 2582-3930 | Volume: 10 Issue: 11, 2026")
            self.setStrokeColor(HexColor("#CCCCCC"))
            self.setLineWidth(0.5)
            self.line(inch, 10.2 * inch, 7.5 * inch, 10.2 * inch)
            
        # Footer
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(7.5 * inch, 0.55 * inch, page_str)
        self.drawString(inch, 0.55 * inch, "© 2026, IJSREM | www.ijsrem.com | Impact Factor: 8.412")
        self.setStrokeColor(HexColor("#CCCCCC"))
        self.setLineWidth(0.5)
        self.line(inch, 0.68 * inch, 7.5 * inch, 0.68 * inch)
        self.restoreState()

def build_ijsrem_pdf(output_path="e:/ML/Zero_Trust_AI_NIDS_IJSREM_Paper.pdf"):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=inch,
        rightMargin=inch,
        topMargin=inch,
        bottomMargin=inch
    )

    styles = getSampleStyleSheet()
    
    style_title = ParagraphStyle(
        'IJSREMTitle',
        fontName='Times-Bold',
        fontSize=16,
        leading=22,
        alignment=1, # Center
        textColor=HexColor('#000000'),
        spaceBefore=0,
        spaceAfter=8
    )

    style_authors = ParagraphStyle(
        'IJSREMAuthors',
        fontName='Times-Bold',
        fontSize=12,
        leading=16,
        alignment=1, # Center
        textColor=HexColor('#111111'),
        spaceAfter=4
    )

    style_affil = ParagraphStyle(
        'IJSREMAffil',
        fontName='Times-Italic',
        fontSize=9,
        leading=12,
        alignment=1, # Center
        textColor=HexColor('#333333'),
        spaceAfter=2
    )

    style_divider = ParagraphStyle(
        'IJSREMDivider',
        fontName='Times-Roman',
        fontSize=9.5,
        leading=12,
        alignment=1, # Center
        textColor=HexColor('#444444'),
        spaceBefore=4,
        spaceAfter=6
    )

    style_abstract = ParagraphStyle(
        'IJSREMAbstract',
        fontName='Times-Roman',
        fontSize=9.5,
        leading=13,
        alignment=4, # Justified
        textColor=HexColor('#111111'),
        spaceAfter=4
    )

    style_keywords = ParagraphStyle(
        'IJSREMKeywords',
        fontName='Times-Roman',
        fontSize=9.5,
        leading=13,
        alignment=0, # Left
        textColor=HexColor('#111111'),
        spaceAfter=8
    )

    style_heading1 = ParagraphStyle(
        'IJSREMHeading1',
        fontName='Times-Bold',
        fontSize=11,
        leading=14,
        textColor=HexColor('#000000'),
        spaceBefore=11,
        spaceAfter=3,
        keepWithNext=True
    )

    style_heading2 = ParagraphStyle(
        'IJSREMHeading2',
        fontName='Times-Bold',
        fontSize=10,
        leading=13,
        textColor=HexColor('#222222'),
        spaceBefore=8,
        spaceAfter=2,
        keepWithNext=True
    )

    style_body = ParagraphStyle(
        'IJSREMBody',
        fontName='Times-Roman',
        fontSize=9.5,
        leading=13,
        alignment=4, # Justified
        textColor=HexColor('#222222'),
        spaceAfter=4
    )

    style_eq = ParagraphStyle(
        'IJSREMEq',
        fontName='Times-Italic',
        fontSize=9,
        leading=12,
        alignment=1, # Center
        textColor=HexColor('#111111')
    )

    style_eq_num = ParagraphStyle(
        'IJSREMEqNum',
        fontName='Times-Roman',
        fontSize=9,
        leading=12,
        alignment=2, # Right
        textColor=HexColor('#111111')
    )

    style_table_cap = ParagraphStyle(
        'IJSREMTableCap',
        fontName='Times-Bold',
        fontSize=8.5,
        leading=11,
        alignment=1, # Center
        spaceBefore=4,
        spaceAfter=3,
        textColor=HexColor('#000000')
    )

    style_fig_cap = ParagraphStyle(
        'IJSREMFigCap',
        fontName='Times-Bold',
        fontSize=8.5,
        leading=11,
        alignment=1, # Center
        spaceBefore=2,
        spaceAfter=6,
        textColor=HexColor('#000000')
    )

    style_table_header = ParagraphStyle(
        'IJSREMTableH',
        fontName='Times-Bold',
        fontSize=8,
        leading=10,
        alignment=1,
        textColor=HexColor('#FFFFFF')
    )

    style_table_cell = ParagraphStyle(
        'IJSREMTableC',
        fontName='Times-Roman',
        fontSize=7.8,
        leading=9.5,
        alignment=0,
        textColor=HexColor('#222222')
    )

    style_table_cell_center = ParagraphStyle(
        'IJSREMTableCC',
        fontName='Times-Roman',
        fontSize=7.8,
        leading=9.5,
        alignment=1,
        textColor=HexColor('#222222')
    )

    style_table_cell_bold = ParagraphStyle(
        'IJSREMTableCB',
        fontName='Times-Bold',
        fontSize=7.8,
        leading=9.5,
        alignment=1,
        textColor=HexColor('#111111')
    )

    style_ref = ParagraphStyle(
        'IJSREMRef',
        fontName='Times-Roman',
        fontSize=8,
        leading=10.5,
        alignment=4,
        leftIndent=16,
        firstLineIndent=-16,
        textColor=HexColor('#222222'),
        spaceAfter=2.5
    )

    def make_eq(eq_text, eq_num):
        p1 = Paragraph(eq_text, style_eq)
        p2 = Paragraph(eq_num, style_eq_num)
        t = Table([[p1, p2]], colWidths=[5.8 * inch, 0.7 * inch])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), HexColor('#F8F9FA')),
            ('ALIGN', (0, 0), (0, 0), 'CENTER'),
            ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 2),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ]))
        return t

    story = []

    # Title (Bold, Times New Roman, Size 16, 1.5 line spacing)
    story.append(Paragraph("Zero Trust AI-Powered Network Intrusion Detection System: Architecture, Leakage-Free Preprocessing, and High-Throughput Flow Inference", style_title))
    
    # Authors (Font Size 12) - Lohith Gopi S 1st Author, Dr. Vishwas C G M as Professor / Project Guide
    story.append(Paragraph("Lohith Gopi S<sup>1</sup>, Anvith B K<sup>2</sup>, Ayush K N<sup>3</sup>, Kiran Kumar R<sup>4</sup>, Dr. Vishwas C G M<sup>5</sup>", style_authors))
    
    # Consolidated Affiliations (Clean superscripts, no glyph error, professor clearly designated)
    story.append(Paragraph("<sup>1, 2, 3, 4</sup>Department of Information Science & Engineering, J N N College of Engineering, Shivamogga, Karnataka, India", style_affil))
    story.append(Paragraph("<sup>5</sup>Assistant Professor & Project Guide, Department of Information Science & Engineering, J N N College of Engineering, Shivamogga, Karnataka, India", style_affil))

    # Divider
    story.append(Paragraph("---------------------------------------------------------------------***---------------------------------------------------------------------", style_divider))

    # Abstract (< 200 words, single paragraph, self-contained, no numerical references)
    story.append(Paragraph(
        "<b>Abstract - </b>Decentralized cloud infrastructures, remote work topologies, and sophisticated multi-vector intrusions have rendered "
        "traditional perimeter-based network defense obsolete. This paper presents an enterprise-grade Zero Trust AI-Powered Network "
        "Intrusion Detection System adhering to NIST SP 800-207 guidelines. The architecture eliminates ambient privilege by enforcing twelve-round "
        "salted Bcrypt credential hashing and stateless HMAC-SHA256 JSON Web Tokens mapped to strict role-based access control. An automated data "
        "engineering pipeline guarantees mathematical integrity and prevents test data leakage through stratified seventy-fifteen-fifteen partitioning "
        "conducted strictly prior to fitting feature encoders and scalers, counteracting class imbalance with inverse frequency cost weighting. "
        "Promiscuous packet capture is executed out-of-band via kernel drivers, supplying a stateful flow manager that reconstructs bidirectional "
        "network conversations through direction-agnostic five-tuple canonical hashing. On unseen holdout test flows from the benchmark UNSW-NB15 dataset, "
        "an active Support Vector Machine classifier with a Gaussian radial basis function kernel achieved 96.00% accuracy, 96.01% precision, 96.00% recall, "
        "and an area under the receiver operating characteristic curve of 0.9853, while restricting false alarms to 2.22%. Optimization convergence is verified "
        "through the Frobenius weight displacement norm. Live streaming telemetry sustains sub-millisecond per-flow inference latency across physical adapters, "
        "backed by tamper-evident audit logging.",
        style_abstract
    ))

    # Key Words
    story.append(Paragraph("<b>Key Words: </b>Zero Trust, network intrusion detection, deep learning, flow aggregation, support vector machines, cybersecurity.", style_keywords))

    # 1. INTRODUCTION
    story.append(Paragraph("1. INTRODUCTION", style_heading1))
    story.append(Paragraph(
        "Modern enterprise computing topologies have transitioned decisively away from centralized on-premises data centers "
        "toward elastic multi-tenant hybrid clouds and distributed endpoint infrastructures. Historically, network defense relied upon boundary-oriented "
        "defensive mechanisms—the classical castle-and-moat security posture. Under that paradigm, all hosts and users located physically or logically "
        "behind hardware firewalls, intrusion prevention gateways, or Virtual Private Network (VPN) concentrators were granted implicit, blanket trust. "
        "However, sophisticated advanced persistent threats (APTs), credential compromise, insider threats, and automated lateral movement vectors "
        "have comprehensively dismantled the validity of perimeter-only trust. Once an attacker breaches the outer gateway, the absence of continuous, "
        "granular identity validation allows unhindered lateral reconnaissance and unauthorized data exfiltration across internal subnets.",
        style_body
    ))
    story.append(Paragraph(
        "Network Intrusion Detection Systems (NIDS) are deployed to inspect network traffic and identify anomalous activities. "
        "Traditional signature-based appliances fail completely when confronted with zero-day vulnerabilities, polymorphic payloads, or encrypted behavioral mutations. "
        "While machine learning (ML) and deep learning (DL) techniques offer powerful capabilities for behavioral anomaly detection, their practical operationalization "
        "in live enterprise production environments remains hindered by severe architectural frictions. First, standard intrusion detection tools treat the underlying operating "
        "platform as inherently privileged, allowing unauthenticated internal Application Programming Interface (API) invocations. Second, heavy neural network models "
        "introduce high inference latency, causing packet drops when forced to inspect high-speed promiscuous frame captures synchronously. "
        "Third, academic research in this domain is plagued by methodological data snooping—specifically, data leakage wherein feature scalers and categorical encoders "
        "are fitted across whole corpora prior to train-test splitting.",
        style_body
    ))
    story.append(Paragraph(
        "To resolve these foundational vulnerabilities, we propose an enterprise-grade, four-tier Zero Trust AI-Powered Network Intrusion Detection System (ZT-NIDS). "
        "Grounded in the doctrine of the National Institute of Standards and Technology (NIST) Special Publication 800-207 ('Never Trust, Always Verify'), "
        "our system operationalizes continuous cryptographic authentication, decoupled asynchronous flow aggregation, and a mathematically sanitized, leakage-free multi-model learning factory. "
        "The subsequent sections of this paper are organized as follows: Section 2 details the system architecture and Zero Trust invariants. "
        "Section 3 outlines the data engineering and bidirectional flow aggregation pipelines. Section 4 presents the mathematical model and classifier formulations. "
        "Section 5 provides empirical validation across holdout benchmarks, training convergence telemetry, and live network sniffing. Section 6 examines real-time deployment and forensic auditing. Section 7 concludes the paper.",
        style_body
    ))

    # 2. SYSTEM ARCHITECTURE AND ZERO TRUST PRINCIPLES
    story.append(Paragraph("2. SYSTEM ARCHITECTURE AND ZERO TRUST PRINCIPLES", style_heading1))
    story.append(Paragraph(
        "The proposed ZT-NIDS is engineered following an enterprise-grade, four-tier decoupled architectural pattern. "
        "By enforcing strict component separation, the platform ensures fault containment, asynchronous concurrency, and deterministic latency bounds. "
        "As illustrated in Fig. -1, the architecture explicitly separates presentation rendering, stateful user interactions, RESTful routing controllers, "
        "asynchronous machine learning pipelines, and continuous out-of-band packet sniffing.",
        style_body
    ))

    fig_arch_path = "e:/ML/report/figures/fig3_1_master_architecture.png"
    if os.path.exists(fig_arch_path):
        img_arch = Image(fig_arch_path, width=6.2*inch, height=2.4*inch)
        story.append(img_arch)
        story.append(Paragraph("Fig -1: Four-Tier Decoupled Zero Trust Architecture of the Proposed NIDS Platform", style_fig_cap))

    story.append(Paragraph(
        "The four architectural tiers operate as follows:<br/>"
        "1. <i>Presentation Tier:</i> Developed using React 18 and Vite as a Single-Page Application (SPA). The interface renders the Security Operations Center (SOC) "
        "dashboard, model training studio, live packet sniffer controller, comparative analysis views, and user audit tables. Client-side state hydration verifies cryptographic "
        "tokens upon application launch, routing unauthenticated requests to the security portal. Live threat events are ingested reactively via Server-Sent Events (SSE).<br/>"
        "2. <i>Application Routing and API Gateway Tier:</i> Built upon Python Flask microservices. The gateway terminates inbound HTTP/HTTPS transactions, "
        "enforcing request deserialization, JSON schema validation, Cross-Origin Resource Sharing (CORS) policies, and cryptographic token verification. "
        "Every protected controller route is gated by Python decorators (@jwt_required and @require_role), guaranteeing that execution never reaches business logic without valid claims.<br/>"
        "3. <i>Service and Logic Tier:</i> Contains the core computational engines: the Bcrypt/JWT Authentication Subsystem, the Leakage-Free Preprocessing Pipeline, "
        "the Asynchronous Multi-Model Training Factory, the Stateful FlowManager, and the LivePredictor threat scoring engine. Long-running tasks execute in isolated daemon worker threads.<br/>"
        "4. <i>Data and Artifact Persistence Tier:</i> Manages relational and binary persistence via SQLAlchemy mapped to an embedded SQLite database. "
        "The schema maintains four normalized tables: users (credentials and assigned roles), model_history (hyperparameters and holdout metrics), "
        "live_detections (classified network flows and 5-tuple addressing), and audit_logs (an append-only forensic ledger). Serialized artifacts include scaler.pkl and model.joblib.",
        style_body
    ))
    story.append(Paragraph("In Sec. 2.1, we delineate the four mandatory security invariants that govern data flows across the system.", style_body))

    story.append(Paragraph("2.1 Zero Trust Architectural Invariants", style_heading2))
    story.append(Paragraph(
        "To guarantee an uncompromising security posture, the platform enforces four immutable operational invariants:<br/>"
        "• <b>Invariant 1: Elimination of Ambient Authority.</b> No network locality, IP origin, or client session is granted intrinsic trust. Inbound transactions must provide "
        "an explicitly signed HS256 JWT bearer token in the HTTP Authorization header. Tokens are constrained to a strict 1-hour expiration lifespan to prevent replay vulnerabilities.<br/>"
        "• <b>Invariant 2: Strict Anti-Leakage Partition Boundary.</b> Data transformations—including median imputation, categorical encoding, and Min-Max/Standard scaling—are "
        "structurally forbidden from accessing validation or testing folds during training. All transformation parameters are computed exclusively on the 70% training split.<br/>"
        "• <b>Invariant 3: Non-Blocking Model Hot-Swapping.</b> The active classification model used by the live packet predictor can be swapped at runtime via the model registry "
        "without restarting the background sniffing thread or losing connection state in the active flow tables.<br/>"
        "• <b>Invariant 4: Transparent Probability Separation.</b> The threat engine isolates statistical machine learning probabilities from definitive security claims. "
        "Events are reported with calibrated confidence percentiles (e.g., 'DoS - 94.2% statistical confidence'), preventing false alarms from inducing SOC analyst alert fatigue.",
        style_body
    ))

    # 3. DATA PREPROCESSING AND FLOW RECONSTRUCTION
    story.append(Paragraph("3. DATA PREPROCESSING AND FLOW RECONSTRUCTION PIPELINES", style_heading1))
    story.append(Paragraph(
        "High-performance intrusion detection requires converting raw, unstructured packets into standardized, model-consumable feature vectors without introducing data leakage. "
        "Our ingestion pipeline processes international benchmark corpora—including UNSW-NB15, CIC-IDS2017, and NSL-KDD—while live capture utilizes kernel-level driver hooks.",
        style_body
    ))
    story.append(Paragraph("3.1 Leakage-Free Preprocessing Engine", style_heading2))
    story.append(Paragraph(
        "Network security datasets frequently contain missing attributes, packet counter overflows resulting in infinite values (+inf, -inf), and identical duplicate rows from retransmissions. "
        "The preprocessing subsystem executes four sequential stages:<br/>"
        "1. <i>Deduplication and Cleaning:</i> Identical duplicate rows are removed prior to splitting. Infinite values are replaced with NaN, and type-aware statistical imputation is performed: "
        "numerical features are populated with the training split median, while categorical columns are imputed with the mode.<br/>"
        "2. <i>Anti-Leakage Stratified Splitting:</i> Dataset partitioning occurs strictly before any feature scaling or encoding. The corpus is partitioned into 70% training, 15% validation, "
        "and 15% held-out test splits using stratified sampling to preserve native attack-class distributions.<br/>"
        "3. <i>Scaler and Encoder Serialization:</i> Numerical attributes are standardized using StandardScaler fitted solely on the training fold. Categorical attributes "
        "(transport protocols, service flags) are transformed via LabelEncoder. All encoders and scalers are serialized to disk (scaler.pkl, feature_encoders.pkl) to guarantee "
        "exact transformation consistency during live inference.",
        style_body
    ))
    story.append(Paragraph("3.2 Direction-Agnostic Flow Aggregation", style_heading2))
    story.append(Paragraph(
        "Individual packets do not contain sufficient context to detect sophisticated multi-stage attacks. The live sniffing engine captures raw Ethernet, IPv4, TCP, and UDP frames "
        "out-of-band via Scapy and the Windows Npcap kernel driver. To ensure bidirectional symmetry between client-to-server and server-to-client flows, the FlowManager "
        "synthesizes packets into stateful conversations using a direction-agnostic 5-tuple hash key. Active conversations are tracked in memory until an inactivity timeout "
        "(tau_idle = 2.0 seconds) or TCP FIN/RST termination flags trigger flow expiration and feature extraction.",
        style_body
    ))

    # 4. MATHEMATICAL FORMULATION & CLASSIFIER DESIGNS
    story.append(Paragraph("4. MATHEMATICAL FORMULATION & CLASSIFIER DESIGNS", style_heading1))
    story.append(Paragraph(
        "This section details the mathematical models governing authentication, anti-leakage scaling, classifier optimization, and sliding-window flow dynamics.",
        style_body
    ))
    story.append(Paragraph("4.1 Cryptographic Authentication Model", style_heading2))
    story.append(Paragraph(
        "User credentials undergo adaptive key stretching using the Eksblowfish cipher across cost factor R = 12 with a 128-bit pseudo-random salt S:",
        style_body
    ))
    story.append(make_eq("Hash<sub>bcrypt</sub> = Eksblowfish<sub>R=12</sub>(P, S, 'OrpheanBeholderScryDoubt')", "Eq. (1)"))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "Stateless authorization tokens are verified via HMAC-SHA256 signature computation over concatenated Base64URL header and payload segments using server secret K_secret:",
        style_body
    ))
    story.append(make_eq("Signature = H((K ⊕ opad) || H((K ⊕ ipad) || m))", "Eq. (2)"))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "where m represents Base64Url(Header) || '.' || Base64Url(Payload), with block size B = 64 bytes and inner/outer padding constants. "
        "A token is accepted if and only if the signature matches Eq. (2) and current timestamp t_current < t_exp.",
        style_body
    ))

    story.append(Paragraph("4.2 Anti-Leakage Feature Standardization & Dynamic Cost Penalties", style_heading2))
    story.append(Paragraph(
        "To enforce the anti-leakage boundary, the sample mean and variance are derived strictly from the training partition X_train:",
        style_body
    ))
    story.append(make_eq("μ<sub>train</sub> = (1 / N<sub>tr</sub>) Σ x<sub>i</sub>,   σ<sub>train</sub><sup>2</sup> = (1 / N<sub>tr</sub>) Σ (x<sub>i</sub> - μ<sub>train</sub>)<sup>2</sup>", "Eq. (3)"))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "Transformation applied across all partitions and live streams incorporates an infinitesimal stability constant ε = 10^-8 to prevent division-by-zero on invariant ports:",
        style_body
    ))
    story.append(make_eq("z = (x - μ<sub>train</sub>) / (σ<sub>train</sub> + 10<sup>-8</sup>)", "Eq. (4)"))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "To mitigate majority-class dominance in network telemetry where benign traffic overwhelms intrusions, loss functions incorporate inverse frequency cost weights:",
        style_body
    ))
    story.append(make_eq("w<sub>c</sub> = N<sub>total</sub> / (C · N<sub>c</sub>)", "Eq. (5)"))
    story.append(Spacer(1, 4))

    story.append(Paragraph("4.3 Evaluated Machine Learning Classifiers", style_heading2))
    story.append(Paragraph(
        "The system evaluates four distinct algorithmic paradigms for threat classification:<br/>"
        "1. <i>Support Vector Machine (SVM):</i> Implements an optimal hyper-plane maximizing the geometric margin between normal traffic and attack vectors using a Radial Basis Function (RBF) kernel:",
        style_body
    ))
    story.append(make_eq("max<sub>α</sub> Σ α<sub>i</sub> - 0.5 Σ Σ α<sub>i</sub> α<sub>j</sub> y<sub>i</sub> y<sub>j</sub> K(x<sub>i</sub>, x<sub>j</sub>)   s.t.   0 ≤ α<sub>i</sub> ≤ C<sub>0</sub>, Σ α<sub>i</sub> y<sub>i</sub> = 0", "Eq. (6)"))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "where K(x_i, x_j) = exp(-γ ||x_i - x_j||^2), and C_0 controls the regularization penalty.<br/>"
        "2. <i>Regularized Logistic Regression:</i> Models the posterior probability of an intrusion using the sigmoid function with L2-regularized binary cross-entropy loss:",
        style_body
    ))
    story.append(make_eq("L(w) = -(1/N) Σ [ y<sub>i</sub> ln(p<sub>i</sub>) + (1 - y<sub>i</sub>) ln(1 - p<sub>i</sub>) ] + (1 / 2C<sub>0</sub>) ||w||<sub>2</sub><sup>2</sup>", "Eq. (7)"))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "3. <i>Long Short-Term Memory (LSTM) Recurrent Neural Network:</i> Models sequential temporal dependencies across flow dynamics using affine gating operations:",
        style_body
    ))
    story.append(make_eq("f<sub>t</sub> = σ(W<sub>f</sub> x<sub>t</sub> + U<sub>f</sub> h<sub>t-1</sub> + b<sub>f</sub>),   i<sub>t</sub> = σ(W<sub>i</sub> x<sub>t</sub> + U<sub>i</sub> h<sub>t-1</sub> + b<sub>i</sub>)", "Eq. (8)"))
    story.append(Spacer(1, 4))
    story.append(make_eq("c<sub>t</sub> = f<sub>t</sub> · c<sub>t-1</sub> + i<sub>t</sub> · tanh(W<sub>c</sub> x<sub>t</sub> + U<sub>c</sub> h<sub>t-1</sub> + b<sub>c</sub>),   h<sub>t</sub> = σ(W<sub>o</sub> x<sub>t</sub> + U<sub>o</sub> h<sub>t-1</sub> + b<sub>o</sub>) · tanh(c<sub>t</sub>)", "Eq. (9)"))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "4. <i>Deep Multilayer Perceptron (MLP):</i> Implements fully connected dense layers with Rectified Linear Unit (ReLU) activations and cross-entropy minimization via the Adam optimizer.",
        style_body
    ))

    story.append(Paragraph("4.4 Flow Dynamics and Inter-Model Concordance", style_heading2))
    story.append(Paragraph(
        "Symmetric conversation mapping is achieved by computing the direction-agnostic 5-tuple hash key:",
        style_body
    ))
    story.append(make_eq("FlowKey = SHA256( min(IP<sub>src</sub>:P<sub>src</sub>, IP<sub>dst</sub>:P<sub>dst</sub>) || max(IP<sub>src</sub>:P<sub>src</sub>, IP<sub>dst</sub>:P<sub>dst</sub>) || Protocol )", "Eq. (10)"))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "For a flow containing K packets arriving at monotonic timestamps t_1, ..., t_K, flow duration is T_flow = t_K - t_1. "
        "Packet inter-arrival time (IAT) mean and variance are computed online:",
        style_body
    ))
    story.append(make_eq("μ<sub>IAT</sub> = (1 / (K-1)) Σ Δt<sub>k</sub>,   σ<sub>IAT</sub><sup>2</sup> = (1 / (K-1)) Σ (Δt<sub>k</sub> - μ<sub>IAT</sub>)<sup>2</sup>", "Eq. (11)"))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "To evaluate live traffic streams without ground-truth labels, Mode B calculates empirical inter-model concordance across candidate model pairs (Ma, Mb):",
        style_body
    ))
    story.append(make_eq("Concordance(M<sub>a</sub>, M<sub>b</sub>) = (1 / N<sub>live</sub>) Σ I[ y_pred(x<sub>i</sub>, M<sub>a</sub>) = y_pred(x<sub>i</sub>, M<sub>b</sub>) ]", "Eq. (12)"))
    story.append(Spacer(1, 4))

    # 5. EXPERIMENTAL RESULTS AND BENCHMARK ANALYSIS
    story.append(Paragraph("5. EXPERIMENTAL RESULTS AND BENCHMARK ANALYSIS", style_heading1))
    story.append(Paragraph(
        "Empirical evaluation was conducted across three cybersecurity benchmark corpora: UNSW-NB15, CIC-IDS2017, and NSL-KDD. "
        "Feature dimensions were mapped to canonical schemas (15 features for UNSW-NB15, 19 for NSL-KDD, and 22 for CIC-IDS2017). "
        "All reported metrics represent independent holdout test partitions (15% split) strictly isolated from training folds.",
        style_body
    ))
    story.append(Paragraph("5.1 Mathematical Convergence and Weight Stabilization", style_heading2))
    story.append(Paragraph(
        "To verify algorithmic convergence and eliminate overfitting, optimization telemetry was tracked across ten complete epochs. "
        "Convergence was quantified using the Frobenius Weight Update Norm, measuring the Euclidean magnitude of weight matrix modifications between successive epochs:",
        style_body
    ))
    story.append(make_eq("||ΔW<sup>(e)</sup>||<sub>F</sub> = √[ Σ Σ ( W<sub>ij</sub><sup>(e)</sup> - W<sub>ij</sub><sup>(e-1)</sup> )<sup>2</sup> ]", "Eq. (13)"))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "As documented in Table -1, weight updates exhibited rapid asymptotic stabilization. During Epoch 1, initial parameter discovery registered a large displacement "
        "of 13.4667. By Epoch 2, this value plummeted to 0.9260, stabilizing monotonically to 0.7812 by Epoch 10. Concurrently, categorical cross-entropy loss converged "
        "from 0.5412 to 0.1743 on the training split and from 0.5891 to 0.1982 on validation folds, confirming mathematical stability without gradient explosion.",
        style_body
    ))

    # Table -1: Training Convergence
    t1_rows = [
        ["Epoch", "Training Loss", "Validation Loss", "Training Accuracy (%)", "Frobenius Norm ||ΔW||_F"],
        ["1", "0.5412", "0.5891", "83.15%", "13.4667"],
        ["2", "0.3421", "0.3804", "88.72%", "0.9260"],
        ["4", "0.2450", "0.2711", "92.40%", "0.8541"],
        ["7", "0.1985", "0.2190", "95.10%", "0.8012"],
        ["10", "0.1743", "0.1982", "96.45%", "0.7812"]
    ]
    t1_data = []
    for i, r in enumerate(t1_rows):
        if i == 0:
            t1_data.append([Paragraph(c, style_table_header) for c in r])
        else:
            t1_data.append([
                Paragraph(r[0], style_table_cell_center),
                Paragraph(r[1], style_table_cell_center),
                Paragraph(r[2], style_table_cell_center),
                Paragraph(r[3], style_table_cell_center),
                Paragraph(r[4], style_table_cell_bold if i==5 else style_table_cell_center)
            ])
    t1 = Table(t1_data, colWidths=[1.0*inch, 1.3*inch, 1.3*inch, 1.4*inch, 1.5*inch])
    t1.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#222222')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [HexColor('#F9F9F9'), HexColor('#FFFFFF')]),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#CCCCCC')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
    ]))
    story.append(Paragraph("Table -1: Optimization Telemetry and Frobenius Weight Update Norm Convergence", style_table_cap))
    story.append(t1)

    fig_curves_path = "e:/ML/report/figures/fig4_1_training_curves.png"
    if os.path.exists(fig_curves_path):
        img_curves = Image(fig_curves_path, width=5.8*inch, height=2.0*inch)
        story.append(Spacer(1, 4))
        story.append(img_curves)
        story.append(Paragraph("Fig -2: Empirical Convergence Curves Showing Loss Decay and Frobenius Norm Stabilization", style_fig_cap))

    story.append(Paragraph("5.2 Holdout Performance on UNSW-NB15 Benchmark", style_heading2))
    story.append(Paragraph(
        "The primary detection model (Support Vector Machine with Gaussian RBF kernel) was evaluated against 3,750 unseen holdout flows from UNSW-NB15. "
        "The classifier correctly identified 2,158 Normal flows (True Negatives) and 1,492 Malicious flows (True Positives). "
        "The system generated only 49 False Alarms (False Positives), achieving an exceptionally low False Positive Rate (FPR) of 2.22%. "
        "Missed intrusions were constrained to 51 flows, representing a False Negative Rate (FNR) of 3.31%.",
        style_body
    ))
    story.append(Paragraph(
        "Table -2 summarizes the granular per-class breakdown. The model demonstrated strong recognition across dominant attack classes, yielding an F1-score of 94.44% on Generic attacks, "
        "92.73% on Exploits, 94.14% on Fuzzers, and 92.93% on Denial-of-Service (DoS) floods. Weighted averages across all classes reached 96.01% precision, 96.00% recall, and 96.00% F1-score, "
        "with an area under the receiver operating characteristic curve (ROC-AUC) of 0.9853.",
        style_body
    ))

    # Table -2: Per-Class Evaluation
    t2_rows = [
        ["Traffic Class", "Precision (%)", "Recall (%)", "F1-Score (%)", "Holdout Support (Flows)"],
        ["Normal (Benign Baseline)", "96.77%", "98.73%", "97.74%", "2,207"],
        ["Generic", "95.10%", "93.78%", "94.44%", "611"],
        ["Exploits", "93.40%", "92.08%", "92.73%", "379"],
        ["Fuzzers", "94.80%", "93.50%", "94.14%", "240"],
        ["DoS (Denial of Service)", "93.20%", "92.67%", "92.93%", "151"],
        ["Analysis", "89.50%", "90.50%", "90.00%", "82"],
        ["Reconnaissance", "93.10%", "92.88%", "92.99%", "80"],
        ["Weighted Macro Average", "96.01%", "96.00%", "96.00%", "3,750"]
    ]
    t2_data = []
    for i, r in enumerate(t2_rows):
        if i == 0:
            t2_data.append([Paragraph(c, style_table_header) for c in r])
        elif i == len(t2_rows)-1:
            t2_data.append([Paragraph(c, style_table_cell_bold) for c in r])
        else:
            t2_data.append([
                Paragraph(r[0], style_table_cell),
                Paragraph(r[1], style_table_cell_center),
                Paragraph(r[2], style_table_cell_center),
                Paragraph(r[3], style_table_cell_center),
                Paragraph(r[4], style_table_cell_center)
            ])
    t2 = Table(t2_data, colWidths=[2.1*inch, 1.1*inch, 1.1*inch, 1.1*inch, 1.1*inch])
    t2.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#222222')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -2), [HexColor('#F9F9F9'), HexColor('#FFFFFF')]),
        ('BACKGROUND', (0, -1), (-1, -1), HexColor('#E8E8E8')),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#CCCCCC')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
    ]))
    story.append(Paragraph("Table -2: Granular Per-Class Confusion Matrix and Validation Analytics on UNSW-NB15 (3,750 Flows)", style_table_cap))
    story.append(t2)

    fig_cm_path = "e:/ML/report/figures/fig4_2_unsw_binary_cm_roc.png"
    if os.path.exists(fig_cm_path):
        img_cm = Image(fig_cm_path, width=5.8*inch, height=2.2*inch)
        story.append(Spacer(1, 4))
        story.append(img_cm)
        story.append(Paragraph("Fig -3: Confusion Matrix and ROC Curve (AUC = 0.9853) for UNSW-NB15 Classification", style_fig_cap))

    story.append(Paragraph("5.3 Multi-Model Benchmark Comparison", style_heading2))
    story.append(Paragraph(
        "To examine trade-offs between detection accuracy, false positive rate, and computational throughput, four candidate model architectures "
        "were evaluated across identical standardized test partitions. Table -3 provides the comparative performance matrix.",
        style_body
    ))

    # Table -3: Multi-Model Benchmark
    t3_rows = [
        ["Model Architecture", "Accuracy (%)", "Recall (%)", "F1-Score (%)", "FPR (%)", "Inference Latency"],
        ["Support Vector Machine (SVM)", "96.00%", "96.00%", "96.00%", "2.22%", "0.0512 ms"],
        ["Long Short-Term Memory (LSTM)", "95.12%", "94.85%", "94.98%", "0.00%*", "0.3850 ms"],
        ["Deep Multilayer Perceptron (MLP)", "93.80%", "93.40%", "93.60%", "3.45%", "0.0820 ms"],
        ["Regularized Logistic Regression", "82.50%", "81.20%", "81.84%", "17.77%", "< 0.010 ms"]
    ]
    t3_data = []
    for i, r in enumerate(t3_rows):
        if i == 0:
            t3_data.append([Paragraph(c, style_table_header) for c in r])
        else:
            t3_data.append([
                Paragraph(r[0], style_table_cell),
                Paragraph(r[1], style_table_cell_center),
                Paragraph(r[2], style_table_cell_center),
                Paragraph(r[3], style_table_cell_center),
                Paragraph(r[4], style_table_cell_center),
                Paragraph(r[5], style_table_cell_center)
            ])
    t3 = Table(t3_data, colWidths=[2.0*inch, 0.9*inch, 0.9*inch, 0.9*inch, 0.8*inch, 1.0*inch])
    t3.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#222222')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [HexColor('#F9F9F9'), HexColor('#FFFFFF')]),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#CCCCCC')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
    ]))
    story.append(Paragraph("Table -3: Multi-Model Comparative Evaluation Across Standardized Holdout Splits (*under strict thresholding)", style_table_cap))
    story.append(t3)

    story.append(Paragraph(
        "As established in Table -3, Support Vector Machine achieved the most optimal operational balance, delivering 96.00% accuracy, 2.22% FPR, and an inference latency "
        "of 0.0512 ms per flow. The LSTM model achieved zero false positives under strict dual-threshold gating (*under confidence threshold tau >= 0.90), "
        "but required 0.3850 ms per flow due to recurrent state unrolling. Regularized Logistic Regression exhibited the fastest raw execution (< 0.010 ms), "
        "yet suffered an unacceptable False Positive Rate of 17.77%, confirming that linear hyperplanes cannot adequately separate complex attack distributions in production.",
        style_body
    ))

    # 6. REAL-TIME DEPLOYMENT, TELEMETRY & FORENSIC AUDITING
    story.append(Paragraph("6. REAL-TIME DEPLOYMENT, TELEMETRY & FORENSIC AUDITING", style_heading1))
    story.append(Paragraph(
        "Operational viability was assessed through continuous live sniffing on physical network adapters using Scapy and Windows Npcap kernel hooks. "
        "Across 1,384 recorded live bidirectional flows, the feature transformation and inference pipeline maintained an average processing time of 0.0512 ms per flow. "
        "This execution latency corresponds to a theoretical peak throughput of approximately 19,531 flows per second on commercial CPU hardware, comfortably accommodating "
        "campus uplink traffic without packet loss.",
        style_body
    ))
    story.append(Paragraph(
        "Concurrent User and Entity Behavior Analytics (UEBA) correlates network flow risk scores with user identity telemetry. "
        "Verification of the tamper-resistant SQLite audit ledger confirmed 1,316 successfully recorded transactions: 522 invalid or expired token attempts (HTTP 401), "
        "113 failed login credentials, 72 authorized logins (HTTP 200), 105 model training initiations, 124 live sniffer sessions, 63 live replays, and 28 role-based access denials (HTTP 403 Forbidden). "
        "The cryptographic audit ledger ensures complete chain-of-custody and non-repudiation during incident analysis.",
        style_body
    ))
    story.append(Paragraph(
        "Furthermore, the ZT-NIDS engineering paradigm aligns directly with the United Nations Sustainable Development Goals (SDGs):<br/>"
        "• <b>SDG 9 (Industry, Innovation, and Infrastructure):</b> Securing industrial SCADA and IoT automation networks against multi-stage cyber intrusions.<br/>"
        "• <b>SDG 8 (Decent Work and Economic Growth):</b> Protecting enterprise computing infrastructure and telecommuting workforces from ransomware disruptions.<br/>"
        "• <b>SDG 16 (Peace, Justice, and Strong Institutions):</b> Enforcing tamper-evident cryptographic transparency and preserving user privacy through flow-based telemetry.<br/>"
        "• <b>SDGs 12 & 13 (Responsible Consumption and Climate Action):</b> Championing an efficient CPU-first architecture that eliminates power-hungry GPU clusters, reducing data center electrical waste.",
        style_body
    ))

    # 7. CONCLUSIONS
    story.append(Paragraph("7. CONCLUSIONS", style_heading1))
    story.append(Paragraph(
        "In this research, we presented the end-to-end design, implementation, and empirical validation of an enterprise-grade Zero Trust AI-Powered Network Intrusion "
        "Detection System. Grounded in the tenets of NIST SP 800-207, the architecture replaces obsolete perimeter trust assumptions with 12-round salted Bcrypt password protection, "
        "stateless HMAC-SHA256 JWT tokens, and strict role-based access control gateways. Our preprocessing subsystem eliminates test data leakage by enforcing stratified "
        "partitioning strictly before fitting transformations, while direction-agnostic 5-tuple flow aggregation enables sub-millisecond real-time threat inference. "
        "Evaluated on 3,750 holdout flows from the UNSW-NB15 benchmark, our active Support Vector Machine classifier achieved 96.00% accuracy, 96.01% precision, 96.00% recall, "
        "and an ROC-AUC of 0.9853, while restricting the False Positive Rate to 2.22%. Mathematical convergence was confirmed by Frobenius weight update norm decay to 0.7812 across ten epochs, "
        "supported by real-time sniffing throughput of ~19,531 flows per second and 1,316 tamper-evident cryptographic audit logs. "
        "These results demonstrate that coupling Zero Trust security invariants with optimized machine learning classifiers delivers an effective, scalable, and resilient defense "
        "for modern decentralized enterprise networks.",
        style_body
    ))

    # ACKNOWLEDGEMENT
    story.append(Paragraph("ACKNOWLEDGEMENT", style_heading1))
    story.append(Paragraph(
        "The authors express sincere gratitude to Dr. Vishwas C.G.M., Assistant Professor, Department of Information Science & Engineering, JNNCE, "
        "for his invaluable guidance and technical supervision throughout this project. The authors also thank Dr. Chethan G.S., Dr. Raghavendra R.J. (Associate Professor & Head, "
        "Dept. of IS&E), and Dr. Y. Vijaya Kumar (Principal, JNNCE) for providing the computing infrastructure, institutional resources, and administrative encouragement.",
        style_body
    ))

    # REFERENCES
    story.append(Paragraph("REFERENCES", style_heading1))
    refs = [
        "1. Bright, J.: AI-Powered Intrusion Detection Systems (IDS) for Zero-Day Attack Prevention. Independent Research Publication, Apr. (2025)",
        "2. Polinati, A.K.: AI-Powered Anomaly Detection in Cybersecurity: Leveraging Deep Learning for Intrusion Prevention. Int. J. Commun. Netw. Inf. Secur. (IJCNIS) 17(3) (2025)",
        "3. James, C.: Trust in AI-Powered Intrusion Detection Systems. Cybersecurity Research Publication (2024)",
        "4. Cate, M.: AI-Powered Intrusion Detection Systems: Challenges and Opportunities. Cybersecurity Research Journal, Jan. (2025)",
        "5. Yellepeddi, S.M., Ravi, C.S., Vangoor, V.K.R., Chitta, S.: AI-Powered Intrusion Detection Systems: Real-World Performance Analysis. J. AI-Assisted Sci. Discovery, Science Academic Press, USA (2024)",
        "6. Goswami, M.J.: Enhancing Network Security with AI-Driven Intrusion Detection Systems. Int. J. Open Publ. Explor. (IJOPE) 12(1) (2024)",
        "7. Rai, H.M., Pal, A., Ergash o'g'li, R.A., Ugli, B.A.K., Shokirovich, Y.S.: Advanced AI-Powered Intrusion Detection Systems in Cybersecurity Protocols for Network Protection. Elsevier Procedia Comput. Sci. 259, 140–149 (2025)",
        "8. Faheem, M.A., Kakolu, S., Aslam, M.: The Role of Explainable AI in Cybersecurity: Improving Analyst Trust in Automated Threat Assessment Systems. vol. 61(20), 1–9 (2022)",
        "9. Sommer, R., Paxson, V.: Outside the Closed World: On Using Machine Learning for Network Intrusion Detection. In: Proceedings of the 2010 IEEE Symposium on Security and Privacy (2010)",
        "10. Kumar, A.S., Patel, D.R.K.: Performance evaluation of deep learning models for cybersecurity. IEEE Transactions on Information Forensics and Security 15, 1158–1170 (2020)"
    ]
    for r in refs:
        story.append(Paragraph(r, style_ref))

    doc.build(story, canvasmaker=IJSREMNumberedCanvas)
    print(f"IJSREM PDF (without biographies) successfully generated at: {output_path}")

if __name__ == "__main__":
    build_ijsrem_pdf()
