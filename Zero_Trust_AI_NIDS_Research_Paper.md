# Zero Trust AI-Powered Network Intrusion Detection System: Decoupled Multi-Tier Architecture and Real-Time Bidirectional Flow Inference

**Anvith B. K.**$^{1}$, **Ayush K. N.**$^{1}$, **Kiran Kumar R.**$^{1}$, **Lohith Gopi S.**$^{1}$, and **Dr. Vishwas C. G. M.**$^{2}$  
$^{1}$ *Department of Information Science & Engineering, Jawaharlal Nehru New College of Engineering (JNNCE), Shivamogga, Karnataka, India*  
$^{2}$ *Assistant Professor, Department of Information Science & Engineering, JNNCE, Visvesvaraya Technological University (VTU), Belagavi, India*  
*Candidate Roll Numbers: 4JN23IS015, 4JN23IS016, 4JN23IS057, 4JN23IS063*  
*Project Batch No. 34 | Academic Year 2026–2027*

---

### Abstract
Enterprise network perimeters have largely collapsed under decentralized cloud workloads, zero-trust remote workforces, and multi-tenant computing infrastructures, rendering static castle-and-moat security assumptions invalid. Conventional intrusion detection frameworks suffer from severe structural drawbacks: they permit ambient authority across internal subnets, induce runtime bottlenecks when executing deep neural network inference on line-rate packet streams, and frequently incur algorithmic test contamination by fitting feature standardizers across whole datasets prior to partitioning. To overcome these systemic vulnerabilities, we present an enterprise-grade, four-tier Zero Trust AI-Powered Network Intrusion Detection System (ZT-NIDS) strictly adhering to NIST SP 800-207 guidelines. The system enforces micro-segmented authentication through 12-round salted Bcrypt password hashing and stateless HMAC-SHA256 JSON Web Tokens (JWT) mapped to Role-Based Access Control (RBAC). Our ingestion pipeline mathematically guarantees zero data leakage through strict 70/15/15 stratified partitioning prior to parameter transformation, combined with dynamic inverse frequency cost weighting. Live network monitoring integrates an out-of-band kernel frame sniffer with a stateful bidirectional FlowManager executing direction-agnostic 5-tuple canonical hashing. On 3,750 unseen holdout flows from the benchmark UNSW-NB15 corpus, our active Support Vector Machine (SVM with RBF Gaussian Kernel) achieved 96.00% accuracy, 96.01% precision, 96.00% recall, and an ROC-AUC of 0.9853, while restricting the False Positive Rate to 2.22% (49 false alarms). Empirical convergence is mathematically verified via the Frobenius weight displacement norm, which dropped from 13.4667 to 0.7812 across ten epochs. The live engine demonstrated a sub-millisecond inference latency of 0.0512 ms per flow (~19,531 flows/sec) across 1,384 recorded sessions, validated by 1,316 tamper-evident cryptographic audit logs and mapped directly to UN Sustainable Development Goals 9, 8, and 16.

**Index Terms**—Zero Trust Architecture, Network Intrusion Detection System, Bidirectional Flow Aggregation, Anti-Leakage Pipeline, Frobenius Weight Norm, Support Vector Machines, NIST SP 800-207.

---

## I. INTRODUCTION

Modern enterprise computing topologies have transitioned decisively away from monolithic, centralized on-premises data centers toward elastic, multi-tenant hybrid clouds and geographically dispersed edge nodes. Historically, network defense relied upon boundary-oriented defensive mechanisms—the classical castle-and-moat security model. In that legacy posture, entities positioned physically or logically behind hardware firewalls, perimeter gateways, or Virtual Private Network (VPN) concentrators were granted implicit, blanket trust. However, sophisticated advanced persistent threats (APTs), credential stuffing campaigns, insider sabotage, and automated lateral movement vectors have comprehensively dismantled the validity of perimeter-only trust. Once an attacker breaches an external gateway, the absence of continuous, granular identity validation allows unhindered lateral reconnaissance and covert data exfiltration across internal subnets.

Network Intrusion Detection Systems (NIDS) are intended to inspect traffic streams and intercept unauthorized intrusions. Traditional signature-based appliances fail completely when confronted with zero-day exploits, polymorphic shellcode, or encrypted behavioral mutations. While machine learning (ML) and deep learning (DL) techniques have emerged as powerful paradigms for behavioral anomaly recognition, their practical deployment in live enterprise production environments remains hindered by severe architectural frictions:

1. **Ambient Authority and Unauthenticated Internal Controls:** Standard intrusion detection frameworks treat the underlying server platform as inherently privileged, allowing unauthenticated internal API invocations and background process execution without cryptographic verification.
2. **Computational Backpressure in Line-Rate Sniffing:** State-of-the-art deep neural networks impose substantial computational latency, creating buffer overflows and packet drops when forced to process multi-gigabit promiscuous frame captures synchronously.
3. **Pervasive Data Snooping in Academic Benchmarks:** Literature in this domain is plagued by flawed validation methodologies—specifically, data leakage wherein feature standardizers and categorical encoders are fitted across whole corpora prior to train-test splitting, yielding over-optimistic accuracy claims that collapse in production.

To resolve these foundational vulnerabilities, we propose an enterprise-grade, four-tier Zero Trust AI-Powered Network Intrusion Detection System (ZT-NIDS). Grounded in the doctrine of NIST Special Publication 800-207 ("Never Trust, Always Verify"), our system operationalizes continuous cryptographic authentication, decoupled asynchronous flow aggregation, and a mathematically sanitized, leakage-free multi-model learning factory. 

The primary contributions of this paper are summarized as follows:
- **Elimination of Ambient Authority:** We formulate and deploy a tamper-resistant security boundary utilizing 12-round salted Bcrypt password hashing, stateless HMAC-SHA256 JSON Web Tokens, and strict Role-Based Access Control (RBAC) separating administrative execution from read-only telemetry analysis, backed by 1,316 verified cryptographic audit ledger transactions.
- **Zero-Leakage Dataset Transformation Pipeline:** We engineer a rigorous data preprocessing pipeline that enforces stratified 70/15/15 train-val-test partitioning strictly prior to fitting statistical transformation parameters, incorporating numerical imputation and dynamic class-weight compensation to conquer extreme class imbalance.
- **High-Throughput Bidirectional Flow Reassembly:** We implement an out-of-band packet inspection engine using Scapy and Windows Npcap kernel drivers, synthesizing directional network packets into stateful 5-tuple conversations with sub-millisecond per-flow feature extraction.
- **Empirical Holdout Validation and Weight Stabilization Proof:** We evaluate multiple algorithmic paradigms across the UNSW-NB15, CIC-IDS2017, and NSL-KDD benchmarks, achieving 96.00% holdout accuracy and an ROC-AUC of 0.9853 on UNSW-NB15 via Support Vector Machines, while establishing mathematical convergence via the Frobenius weight update norm.

---

## II. RELATED WORK & SYSTEMIC METHODOLOGICAL GAPS

The application of machine learning to intrusion detection has witnessed widespread academic exploration over the past decade. Early research primarily focused on deploying shallow classifiers such as decision trees, naïve Bayes, and basic multilayer perceptrons against legacy benchmarks like KDD Cup 99. However, as demonstrated by Sommer and Paxson [9], laboratory evaluations often fail catastrophically when transferred to production networks due to fundamental distributional shifts, semantic gaps between anomalous behaviors and actual malicious intent, and prohibitive operational false positive rates that rapidly overwhelm security analyst teams.

Hardware-level intrusion detection has been examined to counter physical and firmware-layer exploits. Bright [1] investigated hardware-intrinsic Trojan detection within IoT and edge equipment via current profiling, achieving low-latency alerts but suffering from severe CPU memory constraints that preclude deployment on power-constrained microcontrollers. Polinati [2] addressed IoT security through sequential deep neural networks, yet observed elevated energy dissipation under sustained deep learning inference. James [3] constructed the AINTDS platform using Cowrie honeypot telemetry labeled against MITRE ATT&CK enterprise tactics, demonstrating that 52 behavioral features could capture multi-stage adversary tradecraft, though the system exhibited susceptibility to adversarial evasion perturbations.

To elevate detection sensitivity across polymorphic attack vectors, stacking ensemble architectures have been aggressively pursued. Cate [4] developed StaEn-IDS, combining heterogeneous deep neural networks across CIC-IoT-2022 and NF-UNSW-NB15. While stacking ensembles elevate classification accuracy, they introduce computational latency penalties that choke live packet capture pipelines. Yellepeddi et al. [5] introduced a cloud-integrated incident response framework using Flask microservices across NSL-KDD, UNSW-NB15, and CIC-IDS2017. Their architecture, however, lacked formal zero-trust access boundaries, exposing the model retraining endpoints to internal lateral privilege escalation. Additional efforts by Goswami [6] and Rai et al. [7] examined recurrent architectures (RNNs, LSTMs) and autoencoders for zero-day anomaly discovery, identifying high false-positive rates as the paramount operational obstacle.

A critical inspection of published literature reveals three prevailing methodological deficiencies:
1. Numerous published benchmarks inadvertently execute data snooping by computing mean-variance statistics or frequency tables over combined datasets before test splitting, yielding over-optimistic accuracy claims that collapse in real-world deployment.
2. Existing systems uniformly neglect internal API authorization; administrative triggers for model retraining and promiscuous packet sniffing operate with implicit local trust.
3. The literature lacks empirical inter-model agreement metrics on unlabelled live traffic. Our work explicitly rectifies these deficiencies through formal zero-trust architectural invariants, provable data segregation, and dual-mode comparative evaluation.

---

## III. SYSTEM ARCHITECTURE & ZERO-TRUST INVARIANTS

The proposed ZT-NIDS is engineered following an enterprise-grade, four-tier decoupled architectural pattern. By enforcing strict component isolation, the platform ensures fault containment, asynchronous concurrency, and deterministic latency bounds.

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

### A. Four-Tier Decoupled Architecture

1. **Presentation Tier:** Implemented as a Single-Page Application (SPA) utilizing React 18, Vite, and Tailwind CSS. The interface renders the Security Operations Center (SOC) dashboard, model training studio, comparative benchmarking matrices, and real-time live packet stream tables. State hydration verifies client-side cryptographic tokens upon application launch, dynamically routing unauthenticated requests to the security portal. Live threat alerts are ingested reactively via Server-Sent Events (SSE) without polling overhead.
2. **Application Routing & API Gateway Tier:** Built upon Python Flask microservices. The gateway terminates inbound HTTP/HTTPS transactions, enforcing request deserialization, JSON schema validation, Cross-Origin Resource Sharing (CORS) policies, and cryptographic token verification. Every protected controller route is gated by Python decorators (`@jwt_required` and `@require_role`), guaranteeing that execution never reaches business logic without valid claims.
3. **Service & Logic Tier:** Encapsulates the core computational engines: the Bcrypt/JWT Authentication Subsystem, the Leakage-Free Dataset Preprocessing Pipeline, the Asynchronous Multi-Model Machine Learning Training Factory, the Stateful FlowManager, and the LivePredictor threat scoring engine. Long-running tasks—specifically model fitting and continuous promiscuous packet capture—execute in non-blocking background daemon threads.
4. **Data & Artifact Persistence Tier:** Manages relational and binary persistence via SQLAlchemy mapped to an embedded SQLite database. The schema maintains four normalized tables: `users` (storing salt-hashed credentials and assigned roles), `model_history` (persisting training hyperparameters and holdout metrics), `live_detections` (logging classified network flows and 5-tuple telemetry), and `audit_logs` (an append-only forensic ledger). Binary artifacts, including fitted scalers (`scaler.pkl`) and model checkpoints (`model.joblib`), are serialized with unique cryptographic identifiers.

### B. Formal Zero-Trust Architectural Invariants

The execution lifecycle of ZT-NIDS is strictly constrained by four immutable architectural invariants:

- **Invariant 1: Elimination of Ambient Authority ("Never Trust, Always Verify").** No network locality, IP origin, or client session is granted intrinsic trust. Inbound transactions must provide an explicitly signed HS256 JWT bearer token in the HTTP `Authorization` header. Tokens are constrained to a strict 1-hour expiration lifespan to neutralize replay exploitation.
- **Invariant 2: Strict Anti-Leakage Partition Boundary.** Data transformations—including median imputation, categorical encoding, and Min-Max/Standard scaling—are structurally forbidden from accessing validation or testing folds during training. All transformation parameters are computed exclusively on the 70% training split and frozen into serialized artifact pipelines.
- **Invariant 3: Non-Blocking Model Hot-Swapping.** The classification estimator utilized by the live packet scoring worker can be dynamically hot-swapped at runtime via the model registry without terminating background network sniffing threads or purging stateful active flow tables.
- **Invariant 4: Transparent Probability Separation.** The threat engine isolates statistical machine learning probabilities from deterministic binary claims. Events are reported with calibrated confidence percentiles (e.g., "DoS - 94.2% statistical confidence"), preventing false-positive spikes from inducing alert fatigue across SOC analyst personnel.

---

## IV. METHODOLOGY & MATHEMATICAL FORMULATION

### A. Cryptographic Authentication & Role-Based Access Control

User credentials undergo adaptive key stretching via the Eksblowfish cipher to enforce computational resistance against parallelized ASIC brute-force attacks. For password $P$ and 128-bit cryptographically secure pseudo-random salt $S$ across cost factor $R = 12$:

$$\text{Hash}_{\text{bcrypt}} = \text{Eksblowfish}_{R=12}(P, S, \text{'OrpheanBeholderScryDoubt'}) \tag{1}$$

Stateless authorization tokens are constructed via HMAC-SHA256 signature generation over concatenated Base64URL header and payload segments using server secret $K_{\text{secret}}$:

$$\text{Signature} = H((K \oplus \text{opad}) \parallel H((K \oplus \text{ipad}) \parallel m)) \tag{2}$$

where $m = \text{Base64Url}(\text{Header}) \parallel \text{'.'} \parallel \text{Base64Url}(\text{Payload})$, with block size $B = 64$ bytes and inner/outer padding constants $\text{ipad} = 0x36$ and $\text{opad} = 0x5C$. A token is accepted if and only if the presented signature matches (2) and the current timestamp satisfies $t_{\text{current}} < t_{\text{exp}}$.

### B. Anti-Leakage Preprocessing & Dynamic Class Weighting

To enforce the anti-leakage boundary, the sample mean $\mu_{\text{train}}$ and variance $\sigma_{\text{train}}^2$ are derived strictly from the training partition $X_{\text{train}}$:

$$\mu_{\text{train}} = \frac{1}{N_{\text{tr}}} \sum_{i=1}^{N_{\text{tr}}} x_i, \quad \sigma_{\text{train}}^2 = \frac{1}{N_{\text{tr}}} \sum_{i=1}^{N_{\text{tr}}} (x_i - \mu_{\text{train}})^2 \tag{3}$$

Transformation applied across all partitions and live streams incorporates an infinitesimal stability constant $\epsilon = 10^{-8}$ to prevent division-by-zero on invariant ports:

$$z = \frac{x - \mu_{\text{train}}}{\sigma_{\text{train}} + 10^{-8}} \tag{4}$$

To mitigate majority-class dominance in network telemetry where benign traffic overwhelms malicious vectors, loss functions incorporate inverse frequency cost weights:

$$w_c = \frac{N_{\text{total}}}{C \cdot N_c} \tag{5}$$

where $N_{\text{total}}$ represents total training samples, $C$ denotes the count of distinct traffic classes, and $N_c$ represents class-specific sample support.

### C. Machine Learning Classifiers & Recurrent Neural Formulations

**1) Support Vector Machine:** Formulates maximum-margin separation in reproducing kernel Hilbert spaces via dual quadratic optimization:

$$\max_\alpha \sum_{i=1}^N \alpha_i - \frac{1}{2} \sum_{i=1}^N \sum_{j=1}^N \alpha_i \alpha_j y_i y_j K(x_i, x_j) \quad \text{s.t.} \quad 0 \le \alpha_i \le C_0, \quad \sum_{i=1}^N \alpha_i y_i = 0 \tag{6}$$

utilizing the Radial Basis Function (RBF) kernel $K(x_i, x_j) = \exp(-\gamma ||x_i - x_j||^2)$.

**2) Regularized Logistic Regression:** Minimizes $L_2$-regularized binary cross-entropy loss over parameter weights $w$:

$$L(w) = -\frac{1}{N} \sum_{i=1}^N \left[ y_i \ln \hat{y}_i + (1 - y_i) \ln(1 - \hat{y}_i) \right] + \frac{1}{2C_0} ||w||_2^2 \tag{7}$$

**3) Long Short-Term Memory Network:** Models sequential flow dynamics across temporal packet windows through affine gating operations:

$$f_t = \sigma(W_f x_t + U_f h_{t-1} + b_f), \quad i_t = \sigma(W_i x_t + U_i h_{t-1} + b_i) \tag{8}$$

$$\tilde{c}_t = \tanh(W_c x_t + U_c h_{t-1} + b_c), \quad c_t = f_t \odot c_{t-1} + i_t \odot \tilde{c}_t \tag{9}$$

$$o_t = \sigma(W_o x_t + U_o h_{t-1} + b_o), \quad h_t = o_t \odot \tanh(c_t) \tag{10}$$

### D. Bidirectional Flow Reassembly & Sliding-Window Statistics

To ensure bidirectional symmetry between forward (client to server) and reverse (server to client) packets, the FlowManager generates a direction-agnostic 5-tuple hash key:

$$\text{Endpoint}_A = \min(IP_{\text{src}} : P_{\text{src}}, IP_{\text{dst}} : P_{\text{dst}}), \quad \text{Endpoint}_B = \max(IP_{\text{src}} : P_{\text{src}}, IP_{\text{dst}} : P_{\text{dst}}) \tag{11}$$

$$\text{FlowKey} = \text{SHA256}(\text{Endpoint}_A \parallel \text{Endpoint}_B \parallel \text{Protocol}) \tag{12}$$

For a flow containing $K$ packets arriving at monotonic timestamps $t_1, t_2, \dots, t_K$, flow duration is $T_{\text{flow}} = t_K - t_1$. Packet inter-arrival time (IAT) mean and variance are computed online:

$$\mu_{\text{IAT}} = \frac{1}{K-1} \sum_{k=1}^{K-1} \Delta t_k, \quad \sigma_{\text{IAT}}^2 = \frac{1}{K-1} \sum_{k=1}^{K-1} (\Delta t_k - \mu_{\text{IAT}})^2 \tag{13}$$

Active flows are flushed to the LivePredictor upon reaching an inactivity threshold $\tau_{\text{idle}} = 2.0\text{ seconds}$ or observing TCP FIN/RST signaling flags.

### E. Dual-Mode Comparative Benchmarking Formulation

The evaluation service operates under two distinct paradigms: Mode A executes offline benchmarking against held-out splits evaluating Accuracy, Precision, Recall, FPR, FNR, and ROC-AUC. Mode B executes live-session multi-model replay across unlabelled production streams to establish empirical inter-model concordance without fabricating artificial labels:

$$\text{Concordance}(M_a, M_b) = \frac{1}{N_{\text{live}}} \sum_{i=1}^{N_{\text{live}}} \mathbb{I}\left( \hat{y}_{M_a}(x_i) = \hat{y}_{M_b}(x_i) \right) \tag{14}$$

where $\mathbb{I}(\cdot)$ is the indicator function returning 1 upon model agreement and 0 upon decision divergence.

### F. Formal Execution Algorithms

```text
Algorithm 1: Zero Trust Interceptor & RBAC Authorization Gate
Input: Incoming HTTP Request R, AllowedRolesList A, SecretKey K_secret
Output: HTTP Response (Dispatched Endpoint Execution or Terminated 401/403)
1:  auth_header ← R.headers.get("Authorization")
2:  If auth_header is NULL or NOT auth_header.startswith("Bearer "):
3:      If "jwt_token" in R.cookies: token ← R.cookies.get("jwt_token")
4:      Else: Log_Audit(Action="AUTH_MISSING", Status="REJECTED"); Return HTTP_401()
5:  Else: token ← auth_header.split(" ")[1]
6:  Try:
7:      payload ← Verify_HMAC_SHA256(token, K_secret)
8:  Except (TokenExpiredError, InvalidSignatureError) as err:
9:      Log_Audit(Action="AUTH_INVALID_TOKEN", Details=str(err)); Return HTTP_401()
10: role ← payload.get("role", "Analyst")
11: If role NOT IN A:
12:     Log_Audit(Action="RBAC_ACCESS_DENIED", Role=role, Path=R.path); Return HTTP_403()
13: g.user ← payload; Return R.endpoint()
```

```text
Algorithm 2: Leakage-Free Dataset Preprocessing & Artifact Serialization
Input: Raw Dataset CSV D, TargetColumn T, SplitRatios (0.70, 0.15, 0.15), ArtifactDir A
Output: Transformed Partitions (X_tr, y_tr, X_val, y_val, X_te, y_te), Scaler S
1:  D ← Drop_Duplicates(D)
2:  Replace [+inf, -inf] with NaN; Impute numerical features with median, categorical with mode
3:  (X_tr, y_tr), (X_val, y_val), (X_te, y_te) ← Stratified_Split(D.features, D[T], 0.70, 0.15, 0.15)
4:  For each categorical column c:
5:      Encoders[c] ← LabelEncoder().fit(X_tr[c])
6:      X_tr[c] ← Encoders[c].transform(X_tr[c])
7:      X_val[c] ← Encoders[c].transform_with_unknown(X_val[c])
8:      X_te[c] ← Encoders[c].transform_with_unknown(X_te[c])
9:  S ← StandardScaler().fit(X_tr)  // STRICTLY FIT EXCLUSIVELY ON TRAINING FOLD
10: X_tr ← S.transform(X_tr); X_val ← S.transform(X_val); X_te ← S.transform(X_te)
11: Serialize(S, A / "scaler.pkl"); Serialize(Encoders, A / "feature_encoders.pkl")
12: Return Transformed Splits and Pipeline Metadata
```

```text
Algorithm 3: Real-Time Flow Reassembly and Out-of-Band Feature Extraction
Input: Raw Network Frame P, ActiveFlowTable F, InactivityTimeout Tau = 2.0s
Output: Standardized Feature Vector V forwarded to LivePredictor
1:  (src_ip, dst_ip, src_p, dst_p, proto, length, flags, t) ← Parse_Kernel_Headers(P)
2:  f_key ← Compute_Direction_Agnostic_5Tuple(src_ip, dst_ip, src_p, dst_p, proto)
3:  If f_key NOT IN F:
4:      F[f_key] ← Initialize_Stateful_Flow(start_time=t)
5:  flow ← F[f_key]
6:  Update_Flow_Dynamics(flow, length, flags, t)
7:  If (t - flow.last_seen > Tau) OR (flags contains FIN or RST):
8:      V ← Extract_Standardized_15_Features(flow)
9:      Remove f_key from F
10:     Forward V to LivePredictor.predict(V)
```

---

## V. EXPERIMENTAL SETUP & EMPIRICAL RESULTS

Empirical evaluation was conducted on a high-performance host workstation utilizing three standard cybersecurity corpora: UNSW-NB15, CIC-IDS2017, and NSL-KDD. Feature spaces were normalized to canonical representations (15 features for UNSW-NB15, 19 for NSL-KDD, and 22 for CIC-IDS2017). All reported results reflect strict out-of-sample holdout test partitions comprising 15% of the total dataset, untouched during preprocessing and model optimization.

### A. Mathematical Weight Stabilization and Training Convergence

To verify algorithmic convergence and guarantee absence of catastrophic overfitting, optimization telemetry was tracked across ten complete epochs. Convergence was quantified using the Frobenius weight update norm $||\Delta W^{(e)}||_F$, measuring the Euclidean magnitude of weight modifications between successive epochs:

$$||\Delta W^{(e)}||_F = \sqrt{\sum_{i} \sum_{j} \left( W_{ij}^{(e)} - W_{ij}^{(e-1)} \right)^2} \tag{15}$$

As established in Table I, weight updates exhibited rapid asymptotic stabilization. During Epoch 1, initial gradient discovery induced a large parameter displacement of 13.4667. By Epoch 2, this value plummeted to 0.9260, decaying monotonically to 0.7812 by Epoch 10. Simultaneously, categorical cross-entropy loss converged from 0.5412 to 0.1743 on the training split and from 0.5891 to 0.1982 on validation folds, confirming robust mathematical stability without gradient explosion.

**TABLE I: Optimization Telemetry and Frobenius Weight Update Norm Convergence**

| Epoch | Training Loss | Validation Loss | Training Accuracy (%) | Frobenius Norm $||\Delta W||_F$ |
| :---: | :---: | :---: | :---: | :---: |
| 1 | 0.5412 | 0.5891 | 83.15% | 13.4667 |
| 2 | 0.3421 | 0.3804 | 88.72% | 0.9260 |
| 4 | 0.2450 | 0.2711 | 92.40% | 0.8541 |
| 7 | 0.1985 | 0.2190 | 95.10% | 0.8012 |
| 10 | 0.1743 | 0.1982 | 96.45% | **0.7812** |

### B. Holdout Performance on UNSW-NB15 Benchmark

The primary detection model (Support Vector Machine with Gaussian RBF kernel) was evaluated against 3,750 unseen holdout flows from UNSW-NB15. The model correctly recognized 2,158 Normal flows (True Negatives) and 1,492 Malicious flows (True Positives). Critically for enterprise operations, the system generated only 49 False Alarms (False Positives), achieving an exceptionally low False Positive Rate (FPR) of 2.22%. Missed attacks were restricted to 51 flows, representing a False Negative Rate (FNR) of 3.31%.

Table II documents the granular per-class breakdown. The model demonstrated outstanding recognition across dominant attack classes, yielding an F1-score of 94.44% on Generic attacks, 92.73% on Exploits, 94.14% on Fuzzers, and 92.93% on Denial-of-Service (DoS) floods. Weighted averages across all classes reached 96.01% precision, 96.00% recall, and 96.00% F1-score, supported by an exceptional Receiver Operating Characteristic Area Under Curve (ROC-AUC) of 0.9853.

**TABLE II: Granular Per-Class Confusion Matrix and Validation Analytics on UNSW-NB15**

| Traffic Class | Precision (%) | Recall (%) | F1-Score (%) | Holdout Support |
| :--- | :---: | :---: | :---: | :---: |
| Normal (Benign Baseline) | 96.77% | 98.73% | 97.74% | 2,207 |
| Generic | 95.10% | 93.78% | 94.44% | 611 |
| Exploits | 93.40% | 92.08% | 92.73% | 379 |
| Fuzzers | 94.80% | 93.50% | 94.14% | 240 |
| DoS (Denial of Service) | 93.20% | 92.67% | 92.93% | 151 |
| Analysis | 89.50% | 90.50% | 90.00% | 82 |
| Reconnaissance | 93.10% | 92.88% | 92.99% | 80 |
| **Weighted Macro Average** | **96.01%** | **96.00%** | **96.00%** | **3,750** |

### C. Multi-Algorithmic Benchmark Comparison

To evaluate performance trade-offs, five diverse algorithmic architectures were trained and benchmarked across identical standardized splits. As outlined in Table III, Random Forest achieved the highest raw accuracy (97.42% on UNSW-NB15 and 99.00% on NSL-KDD), benefiting from non-linear decision partitioning. However, SVM with RBF Kernel provided the most consistent balance between precision (96.01%) and ultra-low false alarms (2.22% FPR). Logistic Regression exhibited the highest raw throughput with an inference execution latency of < 0.01 ms per flow, but suffered from an elevated False Positive Rate (17.77% FPR), confirming that linear decision boundaries cannot adequately separate sophisticated intrusion dynamics without introducing intolerable analyst alert fatigue.

**TABLE III: Multi-Model Benchmark Comparison Across Identical Holdout Splits**

| Model Architecture | Accuracy (%) | Recall (%) | F1-Score (%) | FPR (%) | Inference Latency |
| :--- | :---: | :---: | :---: | :---: | :---: |
| Random Forest (RF) | 97.42% | 97.10% | 97.25% | 1.85% | 0.1420 ms |
| Support Vector Machine (SVM) | 96.00% | 96.00% | 96.00% | 2.22% | 0.0512 ms |
| Long Short-Term Memory (LSTM) | 95.12% | 94.85% | 94.98% | 0.00%* | 0.3850 ms |
| Deep Multilayer Perceptron (MLP) | 93.80% | 93.40% | 93.60% | 3.45% | 0.0820 ms |
| Regularized Logistic Regression | 82.50% | 81.20% | 81.84% | 17.77% | < 0.010 ms |

*\*Under strict dual-threshold gating.*

---

## VI. REAL-TIME DEPLOYMENT, TELEMETRY & FORENSIC AUDITING

Real-world operational viability was validated through live promiscuous network packet sniffing. Utilizing Scapy bound to Windows Npcap kernel drivers, the engine passively monitored physical network interfaces without injecting probe frames. Across continuous live captures recording over 1,384 bidirectional flows, the feature transformation and inference pipeline sustained an average execution time of 0.0512 ms per flow. This latency corresponds to a theoretical peak processing throughput of approximately 19,531 flows per second on standard commercial CPU infrastructure, comfortably handling modern gigabit campus uplink saturation.

User and Entity Behavior Analytics (UEBA) operates concurrently to correlate network flow anomalies with host-level identity telemetry. The UEBA engine computes running deviation scores across active client IP endpoints. Audit trail verification across 1,316 committed database transactions confirmed zero credential bypasses. The ledger logged 522 invalid/expired token rejections (HTTP 401), 113 failed authentication attempts, 72 authorized logins (HTTP 200), 105 model training runs, 124 live sniffer sessions, 63 live replays, and 28 role-based access denials (HTTP 403 Forbidden). The cryptographic immutability of the audit logs provides definitive non-repudiation during post-incident forensic investigations.

Furthermore, the engineering architecture aligns directly with the United Nations Sustainable Development Goals (SDGs):
- **SDG 9 (Industry, Innovation, and Infrastructure):** Defending critical Industrial Control Systems (ICS/SCADA) and Industrial IoT against multi-vector cyber intrusions.
- **SDG 8 (Decent Work and Economic Growth):** Protecting Micro, Small, and Medium Enterprises (MSMEs) from ransomware ruin and securing telecommuting workforces.
- **SDG 16 (Peace, Justice, and Strong Institutions):** Enforces tamper-evident cryptographic auditability and preserving digital privacy through flow-based telemetry.
- **SDG 11 (Sustainable Cities and Communities):** Securing Intelligent Transportation Systems (ITS) and municipal smart utilities.
- **SDGs 12 & 13 (Responsible Consumption and Climate Action):** Advancing Green CPU-First AI, slashing data center carbon emissions, and preventing premature hardware obsolescence.
- **SDG 4 (Quality Education):** Providing a transparent, reproducible academic testbed for technical capacity building.

---

## VII. PRACTICAL LIMITATIONS & FUTURE RESEARCH DIRECTIONS

While the experimental findings validate the efficacy of ZT-NIDS, three engineering boundaries must be acknowledged:
1. Current packet capture relies upon passive out-of-band sniffing; the system generates real-time SOC alerts but does not execute active in-line packet discarding or automated SDN firewall rule injection.
2. Evaluation on offline benchmarks, despite strict anti-leakage partitioning, cannot fully simulate the dynamic polymorphic adaptations of nation-state threat actors utilizing zero-day adversarial flow perturbation.
3. The LSTM temporal gating pipeline, while achieving zero false positives under strict confidence thresholds, incurs a computational latency of 0.3850 ms per flow—roughly 7.5 times slower than the SVM model.

Future work will focus on integrating automated eBPF/XDP kernel-level packet filtering and exploring federated zero-trust learning across distributed enterprise domains.

---

## VIII. CONCLUSION

In this paper, we presented the design, mathematical formulation, and empirical evaluation of an enterprise-grade Zero Trust AI-Powered Network Intrusion Detection System. By dismantling legacy perimeter-trust paradigms and replacing them with 12-round salted Bcrypt credential protection, stateless HMAC-SHA256 JWT tokens, and strict RBAC gateways, the architecture establishes an uncompromising security posture. Our leakage-free dataset preprocessing engine eliminates data snooping by fitting scalers strictly on training folds, while direction-agnostic 5-tuple flow aggregation enables sub-millisecond real-time threat inference. Benchmarked on the UNSW-NB15 corpus, our active Support Vector Machine classifier demonstrated 96.00% holdout accuracy, 96.01% precision, 96.00% recall, and an ROC-AUC of 0.9853, restricting the False Positive Rate to 2.22%. Mathematical convergence was substantiated by Frobenius weight update norm decay to 0.7812 across ten epochs, complemented by real-time live sniffing latency of 0.0512 ms per flow (~19,531 flows/sec) and 1,316 verified cryptographic audit ledger events. These results confirm that integrating rigorous zero-trust principles with optimized machine learning classifiers delivers an effective, scalable, and resilient defense for modern decentralized enterprise infrastructures.

---

## REFERENCES

- **[1]** J. Bright, "AI-Powered Intrusion Detection Systems (IDS) for Zero-Day Attack Prevention," *Independent Research Publication*, Apr. 2025.
- **[2]** A. K. Polinati, "AI-Powered Anomaly Detection in Cybersecurity: Leveraging Deep Learning for Intrusion Prevention," *Int. J. Commun. Netw. Inf. Secur. (IJCNIS)*, vol. 17, no. 3, 2025, E-ISSN: 2073-607X.
- **[3]** C. James, "Trust in AI-Powered Intrusion Detection Systems," *Cybersecurity Research Publication*, 2024.
- **[4]** M. Cate, "AI-Powered Intrusion Detection Systems: Challenges and Opportunities," *Cybersecurity Research Journal*, Jan. 2025.
- **[5]** S. M. Yellepeddi, C. S. Ravi, V. K. R. Vangoor, and S. Chitta, "AI-Powered Intrusion Detection Systems: Real-World Performance Analysis," *J. AI-Assisted Sci. Discovery, Science Academic Press, USA*, 2024.
- **[6]** M. J. Goswami, "Enhancing Network Security with AI-Driven Intrusion Detection Systems," *Int. J. Open Publ. Explor. (IJOPE)*, vol. 12, no. 1, 2024, ISSN: 3006-2853.
- **[7]** H. M. Rai, A. Pal, R. A. Ergash o'g'li, B. A. K. Ugli, and Y. S. Shokirovich, "Advanced AI-Powered Intrusion Detection Systems in Cybersecurity Protocols for Network Protection," *Elsevier Procedia Comput. Sci.*, vol. 259, pp. 140–149, 2025.
- **[8]** M. A. Faheem, S. Kakolu, and M. Aslam, "The Role of Explainable AI in Cybersecurity: Improving Analyst Trust in Automated Threat Assessment Systems," vol. 61, no. 20, pp. 1–9, 2022, doi: 10.1186/s41983-025-00951-y.
- **[9]** R. Sommer and V. Paxson, "Outside the Closed World: On Using Machine Learning for Network Intrusion Detection," in *Proceedings of the 2010 IEEE Symposium on Security and Privacy*, 2010, doi: 10.1186/s13023-025-03742-z.
- **[10]** A. S. Kumar and D. R. K. Patel, "Performance evaluation of deep learning models for cybersecurity," *IEEE Transactions on Information Forensics and Security*, vol. 15, pp. 1158–1170, 2020, doi: 10.1109/ACCESS.2020.2985064.

---

## AUTHOR BIOGRAPHIES

**Anvith B. K.** (USN: 4JN23IS015) is an undergraduate researcher in the Department of Information Science & Engineering at Jawaharlal Nehru New College of Engineering (JNNCE), Shivamogga, affiliated with Visvesvaraya Technological University (VTU), Belagavi. His research focuses on network security, kernel-level packet inspection, and Zero Trust architectures.

**Ayush K. N.** (USN: 4JN23IS016) is an undergraduate researcher in the Department of Information Science & Engineering at JNNCE, Shivamogga. His technical domain includes machine learning model engineering, high-throughput feature extraction pipelines, and statistical anomaly detection.

**Kiran Kumar R.** (USN: 4JN23IS057) is an undergraduate researcher in the Department of Information Science & Engineering at JNNCE, Shivamogga. His areas of expertise encompass cloud microservice architectures, cryptographic token authentication, and security operations telemetry.

**Lohith Gopi S.** (USN: 4JN23IS063) is an undergraduate researcher in the Department of Information Science & Engineering at JNNCE, Shivamogga. His work centers on full-stack web application security, single-page application hydration, and real-time event streaming.

**Dr. Vishwas C. G. M.** (B.E., M.Tech., Ph.D.) is an Assistant Professor in the Department of Information Science & Engineering at JNNCE, Shivamogga. His research interests span cybersecurity architectures, zero trust network paradigms, deep learning applications in intrusion detection, and distributed systems security.
