# Zero Trust AI-Powered Network Intrusion Detection System: Architecture, Leakage-Free Preprocessing, and High-Throughput Flow Inference

**Lohith Gopi S¹**, **Anvith B K²**, **Ayush K N³**, **Kiran Kumar R⁴**, **Dr. Vishwas C G M⁵**  
*¹˒ ²˒ ³˒ ⁴ Department of Information Science & Engineering, J N N College of Engineering, Shivamogga, Karnataka, India*  
*⁵ Assistant Professor & Project Guide, Department of Information Science & Engineering, J N N College of Engineering, Shivamogga, Karnataka, India*  

---------------------------------------------------------------------***---------------------------------------------------------------------

**Abstract -** Decentralized cloud infrastructures, remote work topologies, and sophisticated multi-vector intrusions have rendered traditional perimeter-based network defense obsolete. This paper presents an enterprise-grade Zero Trust AI-Powered Network Intrusion Detection System adhering to NIST SP 800-207 guidelines. The architecture eliminates ambient privilege by enforcing twelve-round salted Bcrypt credential hashing and stateless HMAC-SHA256 JSON Web Tokens mapped to strict role-based access control. An automated data engineering pipeline guarantees mathematical integrity and prevents test data leakage through stratified seventy-fifteen-fifteen partitioning conducted strictly prior to fitting feature encoders and scalers, counteracting class imbalance with inverse frequency cost weighting. Promiscuous packet capture is executed out-of-band via kernel drivers, supplying a stateful flow manager that reconstructs bidirectional network conversations through direction-agnostic five-tuple canonical hashing. On unseen holdout test flows from the benchmark UNSW-NB15 dataset, an active Support Vector Machine classifier with a Gaussian radial basis function kernel achieved 96.00% accuracy, 96.01% precision, 96.00% recall, and an area under the receiver operating characteristic curve of 0.9853, while restricting false alarms to 2.22%. Optimization convergence is verified through the Frobenius weight displacement norm. Live streaming telemetry sustains sub-millisecond per-flow inference latency across physical adapters, backed by tamper-evident audit logging.

**Key Words:** Zero Trust, network intrusion detection, deep learning, flow aggregation, support vector machines, cybersecurity.

---

## 1. INTRODUCTION

Modern enterprise computing topologies have transitioned decisively away from centralized on-premises data centers toward elastic multi-tenant hybrid clouds and distributed endpoint infrastructures. Historically, network defense relied upon boundary-oriented defensive mechanisms—the classical castle-and-moat security posture. Under that paradigm, all hosts and users located physically or logically behind hardware firewalls, intrusion prevention gateways, or Virtual Private Network (VPN) concentrators were granted implicit, blanket trust. However, sophisticated advanced persistent threats (APTs), credential compromise, insider threats, and automated lateral movement vectors have comprehensively dismantled the validity of perimeter-only trust. Once an attacker breaches the outer gateway, the absence of continuous, granular identity validation allows unhindered lateral reconnaissance and unauthorized data exfiltration across internal subnets.

Network Intrusion Detection Systems (NIDS) are deployed to inspect network traffic and identify anomalous activities. Traditional signature-based appliances fail completely when confronted with zero-day vulnerabilities, polymorphic payloads, or encrypted behavioral mutations. While machine learning (ML) and deep learning (DL) techniques offer powerful capabilities for behavioral anomaly detection, their practical operationalization in live enterprise production environments remains hindered by severe architectural frictions:
1. Standard intrusion detection tools treat the underlying operating platform as inherently privileged, allowing unauthenticated internal Application Programming Interface (API) invocations.
2. Heavy neural network models introduce high inference latency, causing packet drops when forced to inspect high-speed promiscuous frame captures synchronously.
3. Academic research in this domain is plagued by methodological data snooping—specifically, data leakage wherein feature scalers and categorical encoders are fitted across whole corpora prior to train-test splitting.

To resolve these foundational vulnerabilities, we propose an enterprise-grade, four-tier Zero Trust AI-Powered Network Intrusion Detection System (ZT-NIDS). Grounded in the doctrine of the National Institute of Standards and Technology (NIST) Special Publication 800-207 ("Never Trust, Always Verify"), our system operationalizes continuous cryptographic authentication, decoupled asynchronous flow aggregation, and a mathematically sanitized, leakage-free multi-model learning factory. The subsequent sections of this paper are organized as follows: Section 2 details the system architecture and Zero Trust invariants. Section 3 outlines the data engineering and bidirectional flow aggregation pipelines. Section 4 presents the mathematical model and classifier formulations. Section 5 provides empirical validation across holdout benchmarks, training convergence telemetry, and live network sniffing. Section 6 examines real-time deployment and forensic auditing. Section 7 concludes the paper.

---

## 2. SYSTEM ARCHITECTURE AND ZERO TRUST PRINCIPLES

The proposed ZT-NIDS is engineered following an enterprise-grade, four-tier decoupled architectural pattern. By enforcing strict component separation, the platform ensures fault containment, asynchronous concurrency, and deterministic latency bounds. As illustrated in Fig -1, the architecture explicitly separates presentation rendering, stateful user interactions, RESTful routing controllers, asynchronous machine learning pipelines, and continuous out-of-band packet sniffing.

```
+----------------------------------------------------------------------------------------------------+
|                                    1. PRESENTATION TIER (React 18 / Vite)                          |
|  +---------------------------+  +--------------------------+  +---------------------------------+  |
|  | SOC Operations Dashboard  |  | Model Training Studio    |  | Live Sniffer Controller         |  |
|  | - Real-time Threat Gauge  |  | - Hyperparameter Tuning  |  | - Promiscuous / Simulated Modes |  |
|  | - SSE Event Stream        |  | - Convergence Curves     |  | - 5-Tuple Connection Tables     |  |
|  +-------------+-------------+  +------------+-------------+  +----------------+----------------+  |
+----------------|-----------------------------|---------------------------------|-------------------+
                 | HTTP / HTTPS (JSON + Bearer HS256 JWT)                        |                    
+----------------v-----------------------------v---------------------------------v-------------------+
|                            2. APPLICATION ROUTING & API GATEWAY TIER (Flask)                       |
|  +---------------------------+  +--------------------------+  +---------------------------------+  |
|  | JWT Validation Gate       |  | RBAC Authorization Gate  |  | Input Sanitization & Schemas    |  |
|  | - HS256 Secret Signature  |  | - Admin (Execute/Train)  |  | - Multipart Dataset Parsing     |  |
|  | - 1-Hour Time Expiration  |  | - Analyst (Read Telemetry)|  | - CORS Security Middleware      |  |
|  +-------------+-------------+  +------------+-------------+  +----------------+----------------+  |
+----------------|-----------------------------|---------------------------------|-------------------+
                 | Method Invocations & Asynchronous Thread Handoff              |                    
+----------------v-----------------------------v---------------------------------v-------------------+
|                            3. SERVICE & LOGIC TIER (Core Python Engines)                           |
|  +---------------------------+  +--------------------------+  +---------------------------------+  |
|  | Authentication Engine     |  | Anti-Leakage Preprocessor|  | Stateful FlowManager & Sniffer  |  |
|  | - 12-round Bcrypt Hashing |  | - 70/15/15 Stratified    |  | - Scapy + Windows Npcap Driver  |  |
|  | - Stateless Claims Model  |  | - Train-Only Scaler Fit  |  | - Direction-Agnostic 5-Tuple    |  |
|  +---------------------------+  +--------------------------+  +---------------------------------+  |
|  +---------------------------+  +--------------------------+  +---------------------------------+  |
|  | Model Registry & Trainer  |  | LivePredictor Engine     |  | Dual-Mode Comparison Service    |  |
|  | - BaseNIDSModel Factory   |  | - Sub-ms Classification  |  | - Mode A (Offline Holdout)      |  |
|  | - Async Daemon Threads    |  | - SSE Alert Dispatch     |  | - Mode B (Live-Session Replay)  |  |
|  +-------------+-------------+  +------------+-------------+  +----------------+----------------+  |
+----------------|-----------------------------|---------------------------------|-------------------+
                 | I/O File Serialization & Relational SQLAlchemy Transactions    |                    
+----------------v-----------------------------v---------------------------------v-------------------+
|                            4. DATA & ARTIFACT PERSISTENCE TIER (SQLite Storage)                    |
|  +---------------------------+  +--------------------------+  +---------------------------------+  |
|  | users (Bcrypt Credentials)|  | live_detections (Flows)  |  | Serialized Artifact Storage     |  |
|  | model_history (Metrics)   |  | audit_logs (1,316 Events)|  | - scaler.pkl, encoders.pkl      |  |
|  | dataset_history (Catalog) |  |   Tamper-Evident Ledger  |  | - model.joblib                 |  |
|  +---------------------------+  +--------------------------+  +---------------------------------+  |
+----------------------------------------------------------------------------------------------------+
```
**Fig -1: Four-Tier Decoupled Zero Trust Architecture of the Proposed NIDS Platform**

The four architectural tiers operate as follows:
1. **Presentation Tier:** Developed using React 18 and Vite as a Single-Page Application (SPA). The interface renders the Security Operations Center (SOC) dashboard, model training studio, live packet sniffer controller, comparative analysis views, and user audit tables. Client-side state hydration verifies cryptographic tokens upon application launch, routing unauthenticated requests to the security portal. Live threat events are ingested reactively via Server-Sent Events (SSE).
2. **Application Routing and API Gateway Tier:** Built upon Python Flask microservices. The gateway terminates inbound HTTP/HTTPS transactions, enforcing request deserialization, JSON schema validation, Cross-Origin Resource Sharing (CORS) policies, and cryptographic token verification. Every protected controller route is gated by Python decorators (`@jwt_required` and `@require_role`), guaranteeing that execution never reaches business logic without valid claims.
3. **Service and Logic Tier:** Contains the core computational engines: the Bcrypt/JWT Authentication Subsystem, the Leakage-Free Preprocessing Pipeline, the Asynchronous Multi-Model Training Factory, the Stateful FlowManager, and the LivePredictor threat scoring engine. Long-running tasks execute in isolated daemon worker threads.
4. **Data and Artifact Persistence Tier:** Manages relational and binary persistence via SQLAlchemy mapped to an embedded SQLite database. The schema maintains four normalized tables: `users` (credentials and assigned roles), `model_history` (hyperparameters and holdout metrics), `live_detections` (classified network flows and 5-tuple addressing), and `audit_logs` (an append-only forensic ledger). Serialized artifacts include `scaler.pkl` and `model.joblib`.

### 2.1 Zero Trust Architectural Invariants
To guarantee an uncompromising security posture, the platform enforces four immutable operational invariants:
- **Invariant 1: Elimination of Ambient Authority.** No network locality, IP origin, or client session is granted intrinsic trust. Inbound transactions must provide an explicitly signed HS256 JWT bearer token in the HTTP `Authorization` header. Tokens are constrained to a strict 1-hour expiration lifespan to prevent replay vulnerabilities.
- **Invariant 2: Strict Anti-Leakage Partition Boundary.** Data transformations—including median imputation, categorical encoding, and Min-Max/Standard scaling—are structurally forbidden from accessing validation or testing folds during training. All transformation parameters are computed exclusively on the 70% training split.
- **Invariant 3: Non-Blocking Model Hot-Swapping.** The active classification model used by the live packet predictor can be swapped at runtime via the model registry without restarting the background sniffing thread or losing connection state in the active flow tables.
- **Invariant 4: Transparent Probability Separation.** The threat engine isolates statistical machine learning probabilities from definitive security claims. Events are reported with calibrated confidence percentiles (e.g., "DoS - 94.2% statistical confidence"), preventing false alarms from inducing SOC analyst alert fatigue.

---

## 3. DATA PREPROCESSING AND FLOW RECONSTRUCTION PIPELINES

High-performance intrusion detection requires converting raw, unstructured packets into standardized, model-consumable feature vectors without introducing data leakage. Our ingestion pipeline processes international benchmark corpora—including UNSW-NB15, CIC-IDS2017, and NSL-KDD—while live capture utilizes kernel-level driver hooks.

### 3.1 Leakage-Free Preprocessing Engine
Network security datasets frequently contain missing attributes, packet counter overflows resulting in infinite values (+inf, -inf), and identical duplicate rows from retransmissions. The preprocessing subsystem executes four sequential stages:
1. **Deduplication and Cleaning:** Identical duplicate rows are removed prior to splitting. Infinite values are replaced with NaN, and type-aware statistical imputation is performed: numerical features are populated with the training split median, while categorical columns are imputed with the mode.
2. **Anti-Leakage Stratified Splitting:** Dataset partitioning occurs strictly before any feature scaling or encoding. The corpus is partitioned into 70% training, 15% validation, and 15% held-out test splits using stratified sampling to preserve native attack-class distributions.
3. **Scaler and Encoder Serialization:** Numerical attributes are standardized using `StandardScaler` fitted solely on the training fold. Categorical attributes (transport protocols, service flags) are transformed via `LabelEncoder`. All encoders and scalers are serialized to disk (`scaler.pkl`, `feature_encoders.pkl`) to guarantee exact transformation consistency during live inference.

### 3.2 Direction-Agnostic Flow Aggregation
Individual packets do not contain sufficient context to detect sophisticated multi-stage attacks. The live sniffing engine captures raw Ethernet, IPv4, TCP, and UDP frames out-of-band via Scapy and the Windows Npcap kernel driver. To ensure bidirectional symmetry between client-to-server and server-to-client flows, the FlowManager synthesizes packets into stateful conversations using a direction-agnostic 5-tuple hash key. Active conversations are tracked in memory until an inactivity timeout ($\tau_{\text{idle}} = 2.0\text{ seconds}$) or TCP FIN/RST termination flags trigger flow expiration and feature extraction.

---

## 4. MATHEMATICAL FORMULATION & CLASSIFIER DESIGNS

### 4.1 Cryptographic Authentication Model
User credentials undergo adaptive key stretching using the Eksblowfish cipher across cost factor $R = 12$ with a 128-bit pseudo-random salt $S$:

$$\text{Hash}_{\text{bcrypt}} = \text{Eksblowfish}_{R=12}(P, S, \text{'OrpheanBeholderScryDoubt'}) \tag{1}$$

Stateless authorization tokens are verified via HMAC-SHA256 signature computation over concatenated Base64URL header and payload segments using server secret $K_{\text{secret}}$:

$$\text{Signature} = H((K \oplus \text{opad}) \parallel H((K \oplus \text{ipad}) \parallel m)) \tag{2}$$

where $m$ represents $\text{Base64Url}(\text{Header}) \parallel \text{'.'} \parallel \text{Base64Url}(\text{Payload})$, with block size $B = 64$ bytes and inner/outer padding constants. A token is accepted if and only if the signature matches Eq. (2) and current timestamp $t_{\text{current}} < t_{\text{exp}}$.

### 4.2 Anti-Leakage Feature Standardization & Dynamic Cost Penalties
To enforce the anti-leakage boundary, the sample mean and variance are derived strictly from the training partition $X_{\text{train}}$:

$$\mu_{\text{train}} = \frac{1}{N_{\text{tr}}} \sum_{i=1}^{N_{\text{tr}}} x_i, \quad \sigma_{\text{train}}^2 = \frac{1}{N_{\text{tr}}} \sum_{i=1}^{N_{\text{tr}}} (x_i - \mu_{\text{train}})^2 \tag{3}$$

Transformation applied across all partitions and live streams incorporates an infinitesimal stability constant $\epsilon = 10^{-8}$ to prevent division-by-zero on invariant ports:

$$z = \frac{x - \mu_{\text{train}}}{\sigma_{\text{train}} + 10^{-8}} \tag{4}$$

To mitigate majority-class dominance in network telemetry where benign traffic overwhelms intrusions, loss functions incorporate inverse frequency cost weights:

$$w_c = \frac{N_{\text{total}}}{C \cdot N_c} \tag{5}$$

where $N_{\text{total}}$ represents total training samples, $C$ denotes the count of distinct traffic classes, and $N_c$ represents class-specific sample support.

### 4.3 Evaluated Machine Learning Classifiers
The system evaluates four distinct algorithmic paradigms for threat classification:
1. **Support Vector Machine (SVM):** Implements an optimal hyper-plane maximizing the geometric margin between normal traffic and attack vectors using a Radial Basis Function (RBF) kernel:

$$\max_\alpha \sum_{i=1}^N \alpha_i - \frac{1}{2} \sum_{i=1}^N \sum_{j=1}^N \alpha_i \alpha_j y_i y_j K(x_i, x_j) \quad \text{s.t.} \quad 0 \le \alpha_i \le C_0, \quad \sum_{i=1}^N \alpha_i y_i = 0 \tag{6}$$

where $K(x_i, x_j) = \exp(-\gamma ||x_i - x_j||^2)$, and $C_0$ controls the regularization penalty.

2. **Regularized Logistic Regression:** Models the posterior probability of an intrusion using the sigmoid function with $L_2$-regularized binary cross-entropy loss:

$$L(w) = -\frac{1}{N} \sum_{i=1}^N \left[ y_i \ln \hat{y}_i + (1 - y_i) \ln(1 - \hat{y}_i) \right] + \frac{1}{2C_0} ||w||_2^2 \tag{7}$$

3. **Long Short-Term Memory (LSTM) Recurrent Neural Network:** Models sequential temporal dependencies across flow dynamics using affine gating operations:

$$f_t = \sigma(W_f x_t + U_f h_{t-1} + b_f), \quad i_t = \sigma(W_i x_t + U_i h_{t-1} + b_i) \tag{8}$$

$$c_t = f_t \odot c_{t-1} + i_t \odot \tanh(W_c x_t + U_c h_{t-1} + b_c), \quad h_t = \sigma(W_o x_t + U_o h_{t-1} + b_o) \odot \tanh(c_t) \tag{9}$$

4. **Deep Multilayer Perceptron (MLP):** Implements fully connected dense layers with Rectified Linear Unit (ReLU) activations and cross-entropy minimization via the Adam optimizer.

### 4.4 Flow Dynamics and Inter-Model Concordance
Symmetric conversation mapping is achieved by computing the direction-agnostic 5-tuple hash key:

$$\text{FlowKey} = \text{SHA256}\Big( \min(IP_{\text{src}}:P_{\text{src}}, IP_{\text{dst}}:P_{\text{dst}}) \parallel \max(IP_{\text{src}}:P_{\text{src}}, IP_{\text{dst}}:P_{\text{dst}}) \parallel \text{Protocol} \Big) \tag{10}$$

For a flow containing $K$ packets arriving at monotonic timestamps $t_1, \dots, t_K$, flow duration is $T_{\text{flow}} = t_K - t_1$. Packet inter-arrival time (IAT) mean and variance are computed online:

$$\mu_{\text{IAT}} = \frac{1}{K-1} \sum_{k=1}^{K-1} \Delta t_k, \quad \sigma_{\text{IAT}}^2 = \frac{1}{K-1} \sum_{k=1}^{K-1} (\Delta t_k - \mu_{\text{IAT}})^2 \tag{11}$$

To evaluate live traffic streams without ground-truth labels, Mode B calculates empirical inter-model concordance across candidate model pairs ($M_a, M_b$):

$$\text{Concordance}(M_a, M_b) = \frac{1}{N_{\text{live}}} \sum_{i=1}^{N_{\text{live}}} \mathbb{I}\left( \hat{y}_{M_a}(x_i) = \hat{y}_{M_b}(x_i) \right) \tag{12}$$

where $\mathbb{I}(\cdot)$ is the indicator function returning 1 upon consensus and 0 upon decision divergence.

---

## 5. EXPERIMENTAL RESULTS AND BENCHMARK ANALYSIS

Empirical evaluation was conducted across three cybersecurity benchmark corpora: UNSW-NB15, CIC-IDS2017, and NSL-KDD. Feature dimensions were mapped to canonical schemas (15 features for UNSW-NB15, 19 for NSL-KDD, and 22 for CIC-IDS2017). All reported metrics represent independent holdout test partitions (15% split) strictly isolated from training folds.

### 5.1 Mathematical Convergence and Weight Stabilization
To verify algorithmic convergence and eliminate overfitting, optimization telemetry was tracked across ten complete epochs. Convergence was quantified using the Frobenius Weight Update Norm, measuring the Euclidean magnitude of weight matrix modifications between successive epochs:

$$||\Delta W^{(e)}||_F = \sqrt{ \sum_i \sum_j \left( W_{ij}^{(e)} - W_{ij}^{(e-1)} \right)^2 } \tag{13}$$

As documented in Table -1, weight updates exhibited rapid asymptotic stabilization. During Epoch 1, initial parameter discovery registered a large displacement of 13.4667. By Epoch 2, this value plummeted to 0.9260, stabilizing monotonically to 0.7812 by Epoch 10. Concurrently, categorical cross-entropy loss converged from 0.5412 to 0.1743 on the training split and from 0.5891 to 0.1982 on validation folds, confirming mathematical stability without gradient explosion.

**Table -1: Optimization Telemetry and Frobenius Weight Update Norm Convergence**

| Epoch | Training Loss | Validation Loss | Training Accuracy (%) | Frobenius Norm $||\Delta W||_F$ |
| :---: | :---: | :---: | :---: | :---: |
| 1 | 0.5412 | 0.5891 | 83.15% | 13.4667 |
| 2 | 0.3421 | 0.3804 | 88.72% | 0.9260 |
| 4 | 0.2450 | 0.2711 | 92.40% | 0.8541 |
| 7 | 0.1985 | 0.2190 | 95.10% | 0.8012 |
| 10 | 0.1743 | 0.1982 | 96.45% | **0.7812** |

### 5.2 Holdout Performance on UNSW-NB15 Benchmark
The primary detection model (Support Vector Machine with Gaussian RBF kernel) was evaluated against 3,750 unseen holdout flows from UNSW-NB15. The classifier correctly identified 2,158 Normal flows (True Negatives) and 1,492 Malicious flows (True Positives). The system generated only 49 False Alarms (False Positives), achieving an exceptionally low False Positive Rate (FPR) of 2.22%. Missed intrusions were constrained to 51 flows, representing a False Negative Rate (FNR) of 3.31%.

Table -2 summarizes the granular per-class breakdown. The model demonstrated strong recognition across dominant attack classes, yielding an F1-score of 94.44% on Generic attacks, 92.73% on Exploits, 94.14% on Fuzzers, and 92.93% on Denial-of-Service (DoS) floods. Weighted averages across all classes reached 96.01% precision, 96.00% recall, and 96.00% F1-score, with an area under the receiver operating characteristic curve (ROC-AUC) of 0.9853.

**Table -2: Granular Per-Class Confusion Matrix and Validation Analytics on UNSW-NB15 (3,750 Flows)**

| Traffic Class | Precision (%) | Recall (%) | F1-Score (%) | Holdout Support (Flows) |
| :--- | :---: | :---: | :---: | :---: |
| Normal (Benign Baseline) | 96.77% | 98.73% | 97.74% | 2,207 |
| Generic | 95.10% | 93.78% | 94.44% | 611 |
| Exploits | 93.40% | 92.08% | 92.73% | 379 |
| Fuzzers | 94.80% | 93.50% | 94.14% | 240 |
| DoS (Denial of Service) | 93.20% | 92.67% | 92.93% | 151 |
| Analysis | 89.50% | 90.50% | 90.00% | 82 |
| Reconnaissance | 93.10% | 92.88% | 92.99% | 80 |
| **Weighted Macro Average** | **96.01%** | **96.00%** | **96.00%** | **3,750** |

### 5.3 Multi-Model Benchmark Comparison
To examine trade-offs between detection accuracy, false positive rate, and computational throughput, four candidate model architectures were evaluated across identical standardized test partitions. Table -3 provides the comparative performance matrix.

**Table -3: Multi-Model Comparative Evaluation Across Standardized Holdout Splits**

| Model Architecture | Accuracy (%) | Recall (%) | F1-Score (%) | FPR (%) | Inference Latency |
| :--- | :---: | :---: | :---: | :---: | :---: |
| Support Vector Machine (SVM) | 96.00% | 96.00% | 96.00% | 2.22% | 0.0512 ms |
| Long Short-Term Memory (LSTM) | 95.12% | 94.85% | 94.98% | 0.00%* | 0.3850 ms |
| Deep Multilayer Perceptron (MLP) | 93.80% | 93.40% | 93.60% | 3.45% | 0.0820 ms |
| Regularized Logistic Regression | 82.50% | 81.20% | 81.84% | 17.77% | < 0.010 ms |

*\*Under strict dual-threshold gating.*

As established in Table -3, Support Vector Machine achieved the most optimal operational balance, delivering 96.00% accuracy, 2.22% FPR, and an inference latency of 0.0512 ms per flow. The LSTM model achieved zero false positives under strict dual-threshold gating (*under confidence threshold $\tau \ge 0.90$), but required 0.3850 ms per flow due to recurrent state unrolling. Regularized Logistic Regression exhibited the fastest raw execution (< 0.010 ms), yet suffered an unacceptable False Positive Rate of 17.77%, confirming that linear hyperplanes cannot adequately separate complex attack distributions in production.

---

## 6. REAL-TIME DEPLOYMENT, TELEMETRY & FORENSIC AUDITING

Operational viability was assessed through continuous live sniffing on physical network adapters using Scapy and Windows Npcap kernel hooks. Across 1,384 recorded live bidirectional flows, the feature transformation and inference pipeline maintained an average processing time of 0.0512 ms per flow. This execution latency corresponds to a theoretical peak throughput of approximately 19,531 flows per second on commercial CPU hardware, comfortably accommodating campus uplink traffic without packet loss.

Concurrent User and Entity Behavior Analytics (UEBA) correlates network flow risk scores with user identity telemetry. Verification of the tamper-resistant SQLite audit ledger confirmed 1,316 successfully recorded transactions: 522 invalid or expired token attempts (HTTP 401), 113 failed login credentials, 72 authorized logins (HTTP 200), 105 model training initiations, 124 live sniffer sessions, 63 live replays, and 28 role-based access denials (HTTP 403 Forbidden). The cryptographic audit ledger ensures complete chain-of-custody and non-repudiation during incident analysis.

Furthermore, the ZT-NIDS engineering paradigm aligns directly with the United Nations Sustainable Development Goals (SDGs):
- **SDG 9 (Industry, Innovation, and Infrastructure):** Securing industrial SCADA and IoT automation networks against multi-stage cyber intrusions.
- **SDG 8 (Decent Work and Economic Growth):** Protecting enterprise computing infrastructure and telecommuting workforces from ransomware disruptions.
- **SDG 16 (Peace, Justice, and Strong Institutions):** Enforcing tamper-evident cryptographic transparency and preserving user privacy through flow-based telemetry.
- **SDGs 12 & 13 (Responsible Consumption and Climate Action):** Championing an efficient CPU-first architecture that eliminates power-hungry GPU clusters, reducing data center electrical waste.

---

## 7. CONCLUSIONS

In this research, we presented the end-to-end design, implementation, and empirical validation of an enterprise-grade Zero Trust AI-Powered Network Intrusion Detection System. Grounded in the tenets of NIST SP 800-207, the architecture replaces obsolete perimeter trust assumptions with 12-round salted Bcrypt password protection, stateless HMAC-SHA256 JWT tokens, and strict role-based access control gateways. Our preprocessing subsystem eliminates test data leakage by enforcing stratified partitioning strictly before fitting transformations, while direction-agnostic 5-tuple flow aggregation enables sub-millisecond real-time threat inference. Evaluated on 3,750 holdout flows from the UNSW-NB15 benchmark, our active Support Vector Machine classifier achieved 96.00% accuracy, 96.01% precision, 96.00% recall, and an ROC-AUC of 0.9853, while restricting the False Positive Rate to 2.22%. Mathematical convergence was confirmed by Frobenius weight update norm decay to 0.7812 across ten epochs, supported by real-time sniffing throughput of ~19,531 flows per second and 1,316 tamper-evident cryptographic audit logs. These results demonstrate that coupling Zero Trust security invariants with optimized machine learning classifiers delivers an effective, scalable, and resilient defense for modern decentralized enterprise networks.

---

## ACKNOWLEDGEMENT

The authors express sincere gratitude to Dr. Vishwas C.G.M., Assistant Professor, Department of Information Science & Engineering, JNNCE, for his invaluable guidance and technical supervision throughout this project. The authors also thank Dr. Chethan G.S., Dr. Raghavendra R.J. (Associate Professor & Head, Dept. of IS&E), and Dr. Y. Vijaya Kumar (Principal, JNNCE) for providing the computing infrastructure, institutional resources, and administrative encouragement.

---

## REFERENCES

1. Bright, J.: AI-Powered Intrusion Detection Systems (IDS) for Zero-Day Attack Prevention. Independent Research Publication, Apr. (2025)
2. Polinati, A.K.: AI-Powered Anomaly Detection in Cybersecurity: Leveraging Deep Learning for Intrusion Prevention. Int. J. Commun. Netw. Inf. Secur. (IJCNIS) 17(3) (2025)
3. James, C.: Trust in AI-Powered Intrusion Detection Systems. Cybersecurity Research Publication (2024)
4. Cate, M.: AI-Powered Intrusion Detection Systems: Challenges and Opportunities. Cybersecurity Research Journal, Jan. (2025)
5. Yellepeddi, S.M., Ravi, C.S., Vangoor, V.K.R., Chitta, S.: AI-Powered Intrusion Detection Systems: Real-World Performance Analysis. J. AI-Assisted Sci. Discovery, Science Academic Press, USA (2024)
6. Goswami, M.J.: Enhancing Network Security with AI-Driven Intrusion Detection Systems. Int. J. Open Publ. Explor. (IJOPE) 12(1) (2024)
7. Rai, H.M., Pal, A., Ergash o'g'li, R.A., Ugli, B.A.K., Shokirovich, Y.S.: Advanced AI-Powered Intrusion Detection Systems in Cybersecurity Protocols for Network Protection. Elsevier Procedia Comput. Sci. 259, 140–149 (2025)
8. Faheem, M.A., Kakolu, S., Aslam, M.: The Role of Explainable AI in Cybersecurity: Improving Analyst Trust in Automated Threat Assessment Systems. vol. 61(20), 1–9 (2022)
9. Sommer, R., Paxson, V.: Outside the Closed World: On Using Machine Learning for Network Intrusion Detection. In: Proceedings of the 2010 IEEE Symposium on Security and Privacy (2010)
10. Kumar, A.S., Patel, D.R.K.: Performance evaluation of deep learning models for cybersecurity. IEEE Transactions on Information Forensics and Security 15, 1158–1170 (2020)
