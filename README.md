# AI-Powered Zero Trust Network Intrusion Detection System (NIDS)

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0+-black.svg)](https://flask.palletsprojects.com/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.6+-orange.svg)](https://scikit-learn.org/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.x-red.svg)](https://www.tensorflow.org/)
[![Zero Trust](https://img.shields.io/badge/Security-Zero%20Trust%20RBAC-green.svg)](#zero-trust-architecture)
[![License](https://img.shields.io/badge/License-MIT-purple.svg)](LICENSE)

An enterprise-grade **AI-Powered Network Intrusion Detection System (NIDS)** combined with a **Zero Trust Network Security Architecture** (*"Never Trust, Always Verify"*). Features end-to-end dataset management, deep learning neural network training, passive live packet capture and flow aggregation, real-time intrusion classification, and an interactive executive SOC dashboard.

---

## 📌 Table of Contents
- [Project Overview](#-project-overview)
- [Zero Trust Architecture](#-zero-trust-architecture)
- [Live Network Traffic Detection Module](#-live-network-traffic-detection-module)
- [Hardware Capture & Windows Npcap Setup](#-hardware-capture--windows-npcap-setup)
- [Model Compatibility & Feature Schemas](#-model-compatibility--feature-schemas)
- [Technology Stack](#-technology-stack)
- [Project Folder Structure](#-project-folder-structure)
- [Installation & Setup](#-installation--setup)
- [How to Run](#-how-to-run)
- [API Endpoints Documentation](#-api-endpoints-documentation)
- [Automated Testing](#-automated-testing)
- [Ethical Safety & Passive Monitoring Notice](#-ethical-safety--passive-monitoring-notice)
- [Author & License](#-author--license)

---

## 🛡️ Project Overview

Traditional perimeter security relies on castle-and-moat models: once an entity crosses the outer firewall, it is treated as inherently trusted. Attackers taking advantage of stolen credentials or lateral movements can probe internal hosts without triggering alerts.

This platform enforces **Zero Trust**:
1. **Zero Trust Authentication & RBAC**: Every request verifies cryptographically signed JWT tokens and enforces strict Role-Based Access Control (`Admin` vs `Analyst`).
2. **AI-Powered Intrusion Detection**: Neural network models classify traffic into benign baseline flows and specific threat categories (DDoS, DoS, PortScan, Exploits, Infiltration) with statistical confidence scoring.
3. **Passive Live Traffic Monitoring**: Real-time packet sniffing on local network adapters, 5-tuple bidirectional flow aggregation, feature extraction, and continuous SOC alerting.

---

## 🔒 Zero Trust Architecture

- **Stateless Authentication**: Cryptographically signed HS256 JSON Web Tokens (JWT) verified on every API request.
- **Role-Based Access Control (RBAC)**: Fine-grained authorization restricting administrative configuration, model retraining, and live capture to authorized roles (`Admin` and `Analyst`).
- **Immutable Security Audit Log**: SQLite-backed audit trails recording all logins, dataset selections, training runs, live captures, and configuration changes with client IP tracking.
- **Statistical Disclaimers**: Threat predictions are explicitly labeled as statistical classifications rather than absolute proof of compromise, avoiding false certainty.

---

## 📡 Live Network Traffic Detection Module

The live detection module inspects network traffic passively on the host machine without packet injection or external scanning.

```
Network Adapter (Wi-Fi / Ethernet / Loopback)
                    │
                    ▼
       Passive Packet Sniffing (Scapy)
                    │
                    ▼
     Bidirectional Flow Aggregation (5-Tuple Canonical Key)
                    │
                    ▼
  Schema-Aligned Feature Extraction (CIC-IDS2017 / UNSW / NSL)
                    │
                    ▼
      Existing Preprocessor (StandardScaler Normalization)
                    │
                    ▼
       Trained AI Model (.joblib / .keras)
                    │
                    ▼
 Prediction & Risk Scoring (LOW / MEDIUM / HIGH Confidence)
                    │
                    ▼
     Persistence & Telemetry (SQLite & Rolling Memory Cache)
                    │
                    ▼
       Live SOC Dashboard UI (/live-detection)
```

### Key Capabilities
- **Bidirectional Flow Aggregator**: Tracks forward and backward flows using canonical 5-tuples `(min_ip, max_ip, min_port, max_port, proto)` with LRU eviction.
- **Connection Boundary Detection**: Emits flows on TCP termination (`FIN`/`RST`), inactivity timeouts, or configurable packet batch thresholds for near real-time live reporting.
- **Risk Level Assignment**:
  - `LOW`: Normal baseline traffic or low-confidence anomaly ($< 60\%$).
  - `MEDIUM`: Confirmed attack prediction with $60\% \le \text{Confidence} < 85\%$.
  - `HIGH`: Confirmed attack prediction with $\text{Confidence} \ge 85\%$.
- **Controlled Replay Mode**: Generates simulated host traffic packets to verify the complete flow aggregation $\rightarrow$ feature extraction $\rightarrow$ model inference $\rightarrow$ persistence pipeline even without Npcap or elevated privileges.
- **CSV Log Export**: One-click export of captured flow records with timestamps, endpoints, protocols, predictions, and risk levels.

---

## 🔌 Hardware Capture & Windows Npcap Setup

To capture live layer 2 / layer 3 packets from physical network adapters on Windows:

1. Download and install **Npcap** from [https://npcap.com/](https://npcap.com/).
2. During installation, select **"Install Npcap in WinPcap API-compatible Mode"**.
3. Launch PowerShell or Command Prompt as **Administrator** before starting the server.

> **Zero-Dependency Fallback:** If Npcap is not installed or elevated privileges are unavailable, the application gracefully alerts the analyst and allows instant pipeline verification using the built-in **Replay Test Flow** button.

---

## 🧠 Model Compatibility & Feature Schemas

The feature extractor dynamically adapts to the selected trained model's feature schema:

| Dataset Schema | Feature Count | Extracted Attributes |
| :--- | :---: | :--- |
| **CIC-IDS2017** | **22 Features** | Destination Port, Flow Duration, Fwd/Bwd Packets, Fwd/Bwd Bytes, Packet Lengths (Min/Max/Mean), Flow Rates, IAT Statistics, TCP Flags (FIN, SYN, RST, PSH, ACK, URG) |
| **UNSW-NB15** | **15 Features** | Duration, Protocol, Service, Connection State, Packet Counts, Byte Volumes, Packet Rate, Source/Destination TTL, Sload/Dload, Packet Loss |
| **NSL-KDD** | **19 Features** | Duration, Protocol Type, Service, Flag, Src/Dst Bytes, Land, Wrong Fragment, Urgent, Hot, Failed Logins, Logged In, Host/Service Window Rates |

Incompatible models are rejected with actionable error feedback; the system never invents fake data to force compatibility.

---

## 💻 Technology Stack

| Layer | Technology | Purpose |
| :--- | :--- | :--- |
| **Backend Framework** | Flask 3.0+ | REST API server, blueprint routing, authentication middleware |
| **Packet Capture** | Scapy 2.7+ | Passive packet sniffing and layer inspection on Windows adapters |
| **Machine Learning** | Scikit-Learn & TensorFlow | Trained neural network classifiers, `StandardScaler`, `LabelEncoder` |
| **Database** | SQLite & SQLAlchemy ORM | User accounts, audit logs, dataset records, and `live_detections` |
| **Frontend SPA** | React 18, Vite, Tailwind CSS | Modular executive SOC dashboard, live traffic feed, Lucide icons |
| **Security** | PyJWT & Bcrypt | Stateless token authentication and salted credential hashing |

---

## 📁 Project Folder Structure

```
AI-Powered-Zero-Trust-Network-Intrusion-Detection-System/
├── api/                            # Flask REST API Blueprints
│   ├── auth_routes.py              # Authentication & Session APIs
│   ├── dataset_routes.py           # Dataset Upload, Compare, Delete APIs
│   ├── model_routes.py             # Model Training & Evaluation APIs
│   └── live_detection_routes.py    # Live Capture, Status, Traffic, Export APIs
├── database/                       # Database Models & Seeder
│   ├── database.db                 # SQLite Relational Database
│   └── init_db.py                  # User, Role, DatasetHistory, ModelHistory, LiveDetection
├── datasets/                       # Raw & Processed Datasets
│   ├── raw/                        # CIC-IDS2017, UNSW-NB15, NSL-KDD CSVs
│   └── sampled/                    # Stratified Training Samples
├── frontend/                       # Modern React 18 + Vite SPA
│   ├── src/
│   │   ├── components/             # Sidebar, CommandPalette, CitationModal
│   │   ├── pages/dashboard/        # LiveDetectionView, OverviewView, TrainingView
│   │   └── context/                # AuthContext, ThemeContext
│   └── dist/                       # Compiled Production Bundle
├── live_detection/                 # Core Live Network Traffic Engine
│   ├── packet_capture.py           # Interface Discovery, Sniffer Thread, Replay Mode
│   ├── flow_manager.py             # Bidirectional 5-Tuple Flow Aggregation & LRU
│   ├── feature_extractor.py        # Schema-Aligned Feature Extractors (CIC, UNSW, NSL)
│   ├── live_predictor.py           # ML Inference, Probability & Risk Level Scoring
│   └── detection_logger.py         # DB Persistence, Rolling Cache & CSV Export
├── models/                         # Serialized Model Checkpoints & Scalers
├── preprocessing/                  # Data Cleaning & Normalization Pipelines
├── security/                       # Zero Trust RBAC & JWT Middleware
├── tests/                          # Automated Test Suite
│   └── test_live_detection.py      # Unit & Integration Tests
├── app.py                          # Application Factory & Entrypoint
├── config.py                       # Global Settings & Path Configuration
├── requirements.txt                # Python Dependencies
└── README.md                       # Comprehensive Project Documentation
```

---

## ⚙️ Installation & Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/LohithGopi/AI-Powered-Zero-Trust-Network-Intrusion-Detection-System.git
   cd AI-Powered-Zero-Trust-Network-Intrusion-Detection-System
   ```

2. **Activate Virtual Environment**:
   - **Windows (PowerShell)**:
     ```powershell
     .\venv\Scripts\activate
     ```
   - **Linux / macOS**:
     ```bash
     source venv/bin/activate
     ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Build Frontend Bundle (Optional, pre-built in `frontend/dist`)**:
   ```bash
   cd frontend
   npm install
   npm run build
   cd ..
   ```

---

## 🚀 How to Run

1. **Start the Flask Application Server**:
   ```bash
   python app.py
   ```

2. **Access the Web Dashboard**:
   Open your browser to: **`http://127.0.0.1:5000`**

3. **Default Role Credentials**:
   - **Admin**: `admin` / `admin123` (Full configuration, training, and live capture rights)
   - **Analyst**: `analyst` / `analyst123` (Dataset analysis, model inspection, live detection)

---

## 🔌 API Endpoints Documentation

| Method | Endpoint | Allowed Roles | Description |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/auth/login` | Public | Authenticates credentials and returns JWT token |
| `GET` | `/api/live-detection/interfaces` | Admin, Analyst | Enumerates network adapters and reports Npcap status |
| `GET` | `/api/live-detection/models` | Admin, Analyst | Lists trained models with schema compatibility flags |
| `POST` | `/api/live-detection/start` | Admin, Analyst | Starts passive monitoring on selected adapter |
| `POST` | `/api/live-detection/stop` | Admin, Analyst | Stops live capture and flushes in-flight flows |
| `GET` | `/api/live-detection/status` | Admin, Analyst | Returns sniffer engine state and live throughput |
| `GET` | `/api/live-detection/traffic` | Admin, Analyst | Polls recent analyzed flows, alerts, and metrics |
| `POST` | `/api/live-detection/replay` | Admin, Analyst | Executes controlled test packet replay verification |
| `POST` | `/api/live-detection/reset` | Admin, Analyst | Resets real-time telemetry counters |
| `GET` | `/api/live-detection/export` | Admin, Analyst | Downloads CSV file of captured detection logs |

---

## 🧪 Automated Testing

Run the automated test suite covering packet parsing, flow aggregation, schema extraction, ML inference, and RBAC endpoints:

```bash
python -m unittest tests/test_live_detection.py
```

All 9 test cases run in $<1.0\text{s}$ against in-memory components and SQLite test databases.

---

## ⚠️ Ethical Safety & Passive Monitoring Notice

- **Passive Monitoring Only**: This system captures and inspects packets passively on the user's host machine.
- **No Offensive Capabilities**: The system contains no packet injection, denial-of-service, vulnerability exploitation, credential harvesting, or malware execution capabilities.
- **Statistical Predictions**: All classifications represent statistical machine learning predictions. High-risk alerts must be verified against system logs and endpoint telemetry.

---

## 👤 Author & License

**Lohith Gopi**
- **Institution**: Jawaharlal Nehru National College of Engineering (JNNCE), Shivamogga
- **Department**: Department of Information Science and Engineering
- **Project Batch**: Batch No. 34
- **License**: MIT License
