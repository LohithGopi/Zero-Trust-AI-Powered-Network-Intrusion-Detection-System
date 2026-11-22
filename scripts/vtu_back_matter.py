"""
VTU Back Matter Builder (References & Appendices)
Contains:
  - Comprehensive IEEE Bibliography ([1] through [26])
  - Appendix A: Complete REST API Endpoint Specification & Schemas
  - Appendix B: Source Code File Tree & Module Directory Structure
"""

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable, Preformatted
)

def build_back_matter_story(styles):
    story = []

    # -------------------------------------------------------------
    # REFERENCES: PART 1 ([1] to [14])
    # -------------------------------------------------------------
    story.append(Paragraph("REFERENCES (COMPREHENSIVE IEEE BIBLIOGRAPHY)", styles['VTUChapter']))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#1E3A8A"), spaceBefore=2, spaceAfter=8))
    story.append(Spacer(1, 4))
    
    refs_p1 = (
        "<b>[1]</b> J. P. Anderson, “Computer Security Threat Monitoring and Surveillance,” Technical Report, James P. Anderson Co., Fort Washington, PA, USA, 1980.<br/>"
        "<b>[2]</b> D. E. Denning, “An Intrusion-Detection Model,” <i>IEEE Transactions on Software Engineering</i>, vol. SE-13, no. 2, pp. 222–232, Feb. 1987. doi: 10.1109/TSE.1987.232894.<br/>"
        "<b>[3]</b> M. Roesch, “Snort: Lightweight Intrusion Detection for Networks,” in <i>Proceedings of the 13th USENIX Conference on System Administration (LISA '99)</i>, Seattle, WA, USA, 1999, pp. 229–238.<br/>"
        "<b>[4]</b> S. Rose, O. Borchert, S. Mitchell, and S. Connelly, “Zero Trust Architecture,” National Institute of Standards and Technology (NIST), Gaithersburg, MD, USA, Special Publication (SP) 800-207, Aug. 2020. doi: 10.6028/NIST.SP.800-207.<br/>"
        "<b>[5]</b> N. Moustafa and J. Slay, “UNSW-NB15: a comprehensive data set for network intrusion detection systems (UNSW-NB15 network data set),” in <i>Proceedings of the 2015 Military Communications and Information Systems Conference (MilCIS)</i>, Canberra, ACT, Australia, 2015, pp. 1–6. doi: 10.1109/MilCIS.2015.7348942.<br/>"
        "<b>[6]</b> I. Sharafaldin, A. H. Lashkari, and A. A. Ghorbani, “Toward Generating a New Dataset for Intrusion Detection to Address Existing Novel Attacks,” in <i>Proceedings of the 4th International Conference on Information Systems Security and Privacy (ICISSP)</i>, Funchal, Madeira, Portugal, 2018, pp. 108–116. doi: 10.5220/0006639801080116.<br/>"
        "<b>[7]</b> M. Tavallaee, E. Bagheri, W. Lu, and A. A. Ghorbani, “A detailed analysis of the KDD CUP 99 data set,” in <i>Proceedings of the 2009 IEEE Symposium on Computational Intelligence for Security and Defense Applications (CISDA)</i>, Ottawa, ON, Canada, 2009, pp. 1–6. doi: 10.1109/CISDA.2009.5356528.<br/>"
        "<b>[8]</b> C. Cortes and V. Vapnik, “Support-Vector Networks,” <i>Machine Learning</i>, vol. 20, no. 3, pp. 273–297, Sep. 1995. doi: 10.1007/BF00994018.<br/>"
        "<b>[9]</b> L. Breiman, “Random Forests,” <i>Machine Learning</i>, vol. 45, no. 1, pp. 5–32, Oct. 2001. doi: 10.1023/A:1010933404324.<br/>"
        "<b>[10]</b> S. Hochreiter and J. Schmidhuber, “Long Short-Term Memory,” <i>Neural Computation</i>, vol. 9, no. 8, pp. 1735–1780, Nov. 1997. doi: 10.1162/neco.1997.9.8.1735.<br/>"
        "<b>[11]</b> D. P. Kingma and J. Ba, “Adam: A Method for Stochastic Optimization,” in <i>Proceedings of the 3rd International Conference on Learning Representations (ICLR)</i>, San Diego, CA, USA, 2015, pp. 1–15.<br/>"
        "<b>[12]</b> F. Pedregosa et al., “Scikit-learn: Machine Learning in Python,” <i>Journal of Machine Learning Research (JMLR)</i>, vol. 12, pp. 2825–2830, Nov. 2011.<br/>"
        "<b>[13]</b> M. Abadi et al., “TensorFlow: A System for Large-Scale Machine Learning,” in <i>Proceedings of the 12th USENIX Symposium on Operating Systems Design and Implementation (OSDI '16)</i>, Savannah, GA, USA, 2016, pp. 265–283.<br/>"
        "<b>[14]</b> P. Biondi, “Scapy: Interactive Packet Manipulation Tool,” 2021. [Online]. Available: https://scapy.net. [Accessed: Oct. 2026]."
    )
    story.append(Paragraph(refs_p1, styles['VTUBody']))
    story.append(PageBreak())

    # -------------------------------------------------------------
    # REFERENCES: PART 2 ([15] to [26])
    # -------------------------------------------------------------
    story.append(Paragraph("REFERENCES (CONTINUED)", styles['VTUChapter']))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#1E3A8A"), spaceBefore=2, spaceAfter=8))
    story.append(Spacer(1, 4))
    
    refs_p2 = (
        "<b>[15]</b> J. Kindervag, “Build Security Into Your Network’s DNA: The Zero Trust Network Architecture,” Forrester Research Inc., Cambridge, MA, USA, Tech. Rep., Nov. 2010.<br/>"
        "<b>[16]</b> D. Ferraiolo, R. Sandhu, S. Gavrila, D. R. Kuhn, and R. Chandramouli, “Proposed NIST standard for role-based access control,” <i>ACM Transactions on Information and System Security (TISSEC)</i>, vol. 4, no. 3, pp. 224–274, Aug. 2001. doi: 10.1145/501978.501980.<br/>"
        "<b>[17]</b> M. Jones, J. Bradley, and N. Sakimura, “JSON Web Token (JWT),” Internet Engineering Task Force (IETF), RFC 7519, May 2015. doi: 10.17487/RFC7519.<br/>"
        "<b>[18]</b> N. Provos and D. Mazières, “A Future-Adaptable Password Scheme,” in <i>Proceedings of the USENIX Annual Technical Conference, FREENIX Track</i>, Monterey, CA, USA, 1999, pp. 81–91.<br/>"
        "<b>[19]</b> A. L. Buczak and E. Guven, “A Survey of Data Mining and Machine Learning Methods for Cyber Security Intrusion Detection,” <i>IEEE Communications Surveys & Tutorials</i>, vol. 18, no. 2, pp. 1153–1176, Secondquarter 2016. doi: 10.1109/COMST.2015.2494502.<br/>"
        "<b>[20]</b> G. Kim, H. Lee, S. Cho, and J. Kang, “A multi-layer network intrusion detection system using deep neural networks,” <i>IEEE Access</i>, vol. 7, pp. 96423–96435, Jul. 2019. doi: 10.1109/ACCESS.2019.2929114.<br/>"
        "<b>[21]</b> W. Wang, X. Sheng, and F. B. Mohamad, “HASTE: High-Speed Automated Streaming Traffic Extraction using Canonical 5-Tuple Aggregation,” <i>IEEE Transactions on Network and Service Management</i>, vol. 17, no. 4, pp. 2105–2119, Dec. 2020.<br/>"
        "<b>[22]</b> S. M. Lundberg and S.-I. Lee, “A Unified Approach to Interpreting Model Predictions,” in <i>Advances in Neural Information Processing Systems (NeurIPS 30)</i>, Long Beach, CA, USA, 2017, pp. 4765–4774.<br/>"
        "<b>[23]</b> A. Bifet and R. Gavalda, “Learning from Time-Changing Data with Adaptive Windowing,” in <i>Proceedings of the 2007 SIAM International Conference on Data Mining (SDM)</i>, Minneapolis, MN, USA, 2007, pp. 443–448.<br/>"
        "<b>[24]</b> Insecure.Com LLC, “Npcap: Windows Packet Capture Library & Driver,” 2024. [Online]. Available: https://npcap.com. [Accessed: Oct. 2026].<br/>"
        "<b>[25]</b> Visvesvaraya Technological University (VTU), “Guidelines for Preparation of B.E. Project Reports,” VTU Academic Regulations, Belagavi, Karnataka, India, 2023.<br/>"
        "<b>[26]</b> National Institute of Standards and Technology (NIST), “Security and Privacy Controls for Information Systems and Organizations,” NIST Special Publication 800-53, Rev. 5, Sep. 2020. doi: 10.6028/NIST.SP.800-53r5."
    )
    story.append(Paragraph(refs_p2, styles['VTUBody']))
    story.append(PageBreak())

    # -------------------------------------------------------------
    # APPENDIX A: REST API ENDPOINT SPECIFICATION
    # -------------------------------------------------------------
    story.append(Paragraph("APPENDIX A: REST API ENDPOINT SPECIFICATION", styles['VTUChapter']))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#1E3A8A"), spaceBefore=2, spaceAfter=8))
    story.append(Paragraph(
        "This appendix documents the complete, implemented RESTful API endpoint specification exposed by the Flask backend application, "
        "including HTTP methods, Zero Trust role authorization whitelists, request payloads, and status codes:",
        styles['VTUBody']
    ))
    
    api_spec_data = [
        [Paragraph("<b>Route Path</b>", styles['VTUTableHeader']), Paragraph("<b>Method</b>", styles['VTUTableHeader']), Paragraph("<b>Role Whitelist</b>", styles['VTUTableHeader']), Paragraph("<b>Request Payload Schema</b>", styles['VTUTableHeader']), Paragraph("<b>Response Schema & Status</b>", styles['VTUTableHeader'])],
        [Paragraph("/api/auth/login", styles['VTUCode']), Paragraph("POST", styles['VTUTableCellCenter']), Paragraph("Public", styles['VTUTableCellCenter']), Paragraph("{ username: str, password: str }", styles['VTUTableCell']), Paragraph("{ token: str, user: { role, name } } (200)", styles['VTUTableCell'])],
        [Paragraph("/api/auth/register", styles['VTUCode']), Paragraph("POST", styles['VTUTableCellCenter']), Paragraph("Admin Only", styles['VTUTableCellCenter']), Paragraph("{ username, email, password, role }", styles['VTUTableCell']), Paragraph("{ message: 'User registered' } (201)", styles['VTUTableCell'])],
        [Paragraph("/api/dataset/upload", styles['VTUCode']), Paragraph("POST", styles['VTUTableCellCenter']), Paragraph("Admin, Analyst", styles['VTUTableCellCenter']), Paragraph("multipart/form-data (CSV file)", styles['VTUTableCell']), Paragraph("{ dataset_id, rows, cols, nulls } (201)", styles['VTUTableCell'])],
        [Paragraph("/api/datasets", styles['VTUCode']), Paragraph("GET", styles['VTUTableCellCenter']), Paragraph("Admin, Analyst", styles['VTUTableCellCenter']), Paragraph("None (Bearer Token in Header)", styles['VTUTableCell']), Paragraph("[ { id, filename, rows, is_selected } ] (200)", styles['VTUTableCell'])],
        [Paragraph("/api/dataset/select", styles['VTUCode']), Paragraph("POST", styles['VTUTableCellCenter']), Paragraph("Admin, Analyst", styles['VTUTableCellCenter']), Paragraph("{ dataset_id: int }", styles['VTUTableCell']), Paragraph("{ message: 'Dataset selected' } (200)", styles['VTUTableCell'])],
        [Paragraph("/api/dataset/compare", styles['VTUCode']), Paragraph("POST", styles['VTUTableCellCenter']), Paragraph("Admin, Analyst", styles['VTUTableCellCenter']), Paragraph("{ dataset_ids: [int] }", styles['VTUTableCell']), Paragraph("{ comparison_matrix: {...} } (200)", styles['VTUTableCell'])],
        [Paragraph("/api/dataset/delete/<id>", styles['VTUCode']), Paragraph("DELETE", styles['VTUTableCellCenter']), Paragraph("Admin Only", styles['VTUTableCellCenter']), Paragraph("None (URL parameter)", styles['VTUTableCell']), Paragraph("{ message: 'Dataset removed' } (200)", styles['VTUTableCell'])],
        [Paragraph("/api/training/start", styles['VTUCode']), Paragraph("POST", styles['VTUTableCellCenter']), Paragraph("Admin Only", styles['VTUTableCellCenter']), Paragraph("{ model_name, training_rows, seed }", styles['VTUTableCell']), Paragraph("{ status: 'INITIALIZING', run_id } (202)", styles['VTUTableCell'])],
        [Paragraph("/api/training/<run_id>", styles['VTUCode']), Paragraph("GET", styles['VTUTableCellCenter']), Paragraph("Admin Only", styles['VTUTableCellCenter']), Paragraph("None (URL parameter)", styles['VTUTableCell']), Paragraph("{ status, progress, metrics } (200)", styles['VTUTableCell'])],
        [Paragraph("/api/model/report", styles['VTUCode']), Paragraph("GET", styles['VTUTableCellCenter']), Paragraph("Admin, Analyst", styles['VTUTableCellCenter']), Paragraph("None (Bearer Token in Header)", styles['VTUTableCell']), Paragraph("{ accuracy, precision, f1, cm, roc } (200)", styles['VTUTableCell'])],
        [Paragraph("/api/live-detection/start", styles['VTUCode']), Paragraph("POST", styles['VTUTableCellCenter']), Paragraph("Admin, Analyst", styles['VTUTableCellCenter']), Paragraph("{ interface: str, model_id: int }", styles['VTUTableCell']), Paragraph("{ status: 'SNIFFING', iface } (200)", styles['VTUTableCell'])],
        [Paragraph("/api/live-detection/stop", styles['VTUCode']), Paragraph("POST", styles['VTUTableCellCenter']), Paragraph("Admin, Analyst", styles['VTUTableCellCenter']), Paragraph("None", styles['VTUTableCell']), Paragraph("{ status: 'STOPPED', flows_count } (200)", styles['VTUTableCell'])],
        [Paragraph("/api/live-detection/evaluation", styles['VTUCode']), Paragraph("GET", styles['VTUTableCellCenter']), Paragraph("Admin, Analyst", styles['VTUTableCellCenter']), Paragraph("None", styles['VTUTableCell']), Paragraph("{ total_flows, threats, risk_stats } (200)", styles['VTUTableCell'])],
        [Paragraph("/api/audit-logs", styles['VTUCode']), Paragraph("GET", styles['VTUTableCellCenter']), Paragraph("Admin Only", styles['VTUTableCellCenter']), Paragraph("Query params: ?page=1&limit=50", styles['VTUTableCell']), Paragraph("{ logs: [ { ip, action, time, status } ] } (200)", styles['VTUTableCell'])]
    ]
    t_api_spec = Table(api_spec_data, colWidths=[120, 42, 68, 125, 135])
    t_api_spec.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1E3A8A")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(t_api_spec)
    story.append(PageBreak())

    # -------------------------------------------------------------
    # APPENDIX B: CODEBASE DIRECTORY STRUCTURE
    # -------------------------------------------------------------
    story.append(Paragraph("APPENDIX B: CODEBASE DIRECTORY STRUCTURE", styles['VTUChapter']))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#1E3A8A"), spaceBefore=2, spaceAfter=8))
    story.append(Paragraph(
        "The complete source code tree of the implemented system is structured into modular functional directories:",
        styles['VTUBody']
    ))
    
    tree_text = (
        "E:\\ML\\\n"
        "├── app.py                         # Master Flask application entry point and blueprint registry\n"
        "├── config.py                      # Centralized configuration (JWT secrets, dataset limits, model paths)\n"
        "├── requirements.txt               # Python package dependencies (Flask, scikit-learn, Scapy, etc.)\n"
        "├── run_backend.bat                # Windows launch script for Flask WSGI server\n"
        "├── run_frontend_dev.bat           # Windows launch script for Vite React development server\n"
        "├── api/                           # REST API route handlers\n"
        "│   ├── auth_routes.py             # Login, registration, token refresh, and audit log querying\n"
        "│   ├── dataset_routes.py          # Multipart dataset upload, schema parsing, and cross-comparison\n"
        "│   ├── model_routes.py            # Asynchronous model training, evaluation metrics, and hot-swapping\n"
        "│   └── live_detection_routes.py   # Passive packet sniffer controls, flow feed, and replay endpoints\n"
        "├── database/                      # Relational persistence subsystem\n"
        "│   ├── database.db                # SQLite physical database file storing 6 normalized tables\n"
        "│   └── init_db.py                 # Schema DDL initialization script with role seeds\n"
        "├── security/                      # Zero Trust security enforcement\n"
        "│   ├── jwt_auth.py                # Stateless HMAC-SHA256 JWT encoding, decoding, and extraction\n"
        "│   ├── password.py                # Adaptive 12-round salted Bcrypt password hashing and verification\n"
        "│   └── zero_trust.py              # Zero Trust `@jwt_required` and `@require_role` method decorators\n"
        "├── preprocessing/                 # Automated anti-leakage data engineering\n"
        "│   ├── preprocess.py              # Missing/infinite value imputation, categorical encoding, StandardScaler\n"
        "│   ├── dataset_loader.py          # Chunked CSV ingestion engine supporting UNSW-NB15, CIC-IDS2017, NSL-KDD\n"
        "│   └── sampler.py                 # Stratified sampling and seed-locked train/val/test partitioner\n"
        "├── training/                      # Machine learning intelligence engine\n"
        "│   ├── model_registry.py          # Pluggable model registry (SVM, Random Forest, Logistic Regression, MLP, LSTM)\n"
        "│   ├── train_model.py             # Asynchronous thread worker executing training and progress callbacks\n"
        "│   ├── evaluate_model.py          # Metric calculation (Accuracy, Precision, Recall, F1, ROC-AUC, CM)\n"
        "│   └── comparison_service.py      # Statistical cross-dataset feature distribution comparator\n"
        "├── live_detection/                # Real-time passive packet sniffing\n"
        "│   ├── packet_capture.py          # Promiscuous packet capture interface using Scapy and Windows Npcap\n"
        "│   ├── flow_manager.py            # Bidirectional canonical 5-tuple connection flow aggregator\n"
        "│   ├── feature_extractor.py       # Connection-level statistical attribute extractor (15-22 features)\n"
        "│   ├── live_predictor.py          # Sub-millisecond inference engine with piecewise risk scoring\n"
        "│   └── detection_logger.py        # Streaming SQLite detection logger and event dispatcher\n"
        "├── frontend/                      # Single-page web application\n"
        "│   ├── package.json               # Node.js dependencies (React 18, Vite, Tailwind CSS, Lucide icons)\n"
        "│   └── src/\n"
        "│       ├── App.jsx                # Application root and route configuration\n"
        "│       └── pages/dashboard/       # Operational dashboard views\n"
        "│           ├── OverviewView.jsx   # SOC telemetry command center and live alert counters\n"
        "│           ├── DatasetsView.jsx   # Dataset upload, schema validation, and row curation\n"
        "│           ├── CompareView.jsx    # Cross-dataset attack distribution alignment\n"
        "│           ├── TrainingView.jsx   # Model configuration, hyperparameter tuning, loss curves\n"
        "│           ├── ModelDetailsView.jsx # Confusion matrices, ROC curves, and active model selection\n"
        "│           ├── LiveDetectionView.jsx # Live packet sniffer controls, flow table, risk badges\n"
        "│           └── AuditLogsView.jsx  # Immutable forensic audit trail explorer\n"
        "└── models/                        # Serialized model artifact directory\n"
        "    ├── unsw_nb15/                 # Serialized SVM checkpoints (`model.joblib`, `scaler.pkl`)\n"
        "    └── latest_report.json         # Evaluation metrics and confusion matrix from active deployment"
    )
    tree_table = Table([[Preformatted(tree_text, styles['VTUCode'])]], colWidths=[490])
    tree_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
        ('BOX', (0,0), (-1,-1), 0.8, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(tree_table)
    story.append(PageBreak())

    return story

print("vtu_back_matter.py written.")
