# Report Subfolder — Action Log & Deliverables Manifest (`report/`)

**Project Title:** Zero Trust AI-Powered Network Intrusion Detection System (NIDS)  
**Institution:** Jawaharlal Nehru National College of Engineering (JNNCE), Shivamogga  
**Department:** Department of Information Science and Engineering (Batch No. 34)  
**Author:** Lohith Gopi  
**Chapters Generated in `report/`:**
- **Chapter 3 — System Design and Implementation** (Focused 20-Page Necessary Contents Report)
- **Chapter 4 — Results and Analysis** (Condensed Exactly 15-Page Evidence-Based Report with Actual Website Screenshots)

---

## 1. Summary of All Actions Performed in `report/`

### A. Chapter 3: System Design and Implementation (20 Pages)
1. **Full Codebase & Architecture Audit:**
   - Inspected all backend packages (`app.py`, `config.py`, `api/`, `database/`, `security/`, `preprocessing/`, `training/`, `live_detection/`, `utils/`), database schemas (`database/init_db.py`), and verified training evaluation artifacts.
2. **Programmatic Diagram & Flowchart Engine (`report/generate_chapter3_diagrams.py`):**
   - Generated **10 high-resolution (300-DPI) block diagrams and flowcharts** in `report/figures/` (`fig3_1_master_architecture.png` through `fig3_10_live_inference_flowchart.png`).
3. **Focused 20-Page Necessary Contents Report (`Chapter_3_System_Design_and_Implementation.pdf`, `.docx`, `.md`):**
   - Structured into 5 clearly separated sections (`3.1` Proposed Work, `3.2` System Architecture & Block Diagrams, `3.3` Mathematical Model, `3.4` Algorithms & Flowcharts, `3.5` Implementation Summary), excluding extraneous material and containing zero references to "Trojan Horse".

### B. Chapter 4: Results and Analysis (Condensed to Exactly 15 Pages with Live Website Screenshots)
1. **Empirical Evidence Extraction from Host Environment, SQLite Database & Model Checkpoints:**
   - Queried exact Windows 11 hardware specifications (`AMD Ryzen 5 3450U @ 2.10 GHz, 4C/8T, 8.00 GB Physical RAM / 5.94 GB Usable, AMD Radeon Vega 8 Graphics, 119.23 GB NVMe SSD`) and `venv` software versions (`Python 3.13.15`, `Flask 3.1.3`, `Scikit-Learn 1.9.1`, `SQLite 3.50.4`, `Pandas 3.0.6`, `NumPy 2.5.3`, `Scapy 2.7.0`, `PyJWT 2.15.0`, `Bcrypt 5.0.0`).
   - Extracted exact database counts from `database/database.db`: `3` roles, `4` users, `4` cataloged datasets in `dataset_history`, `18` training records in `model_history`, `1,006` security events in `audit_logs`, and `2,343` live network flow records in `live_detections`.
   - Extracted exact holdout evaluation reports from `models/latest_report.json` and `models/*/run_*/evaluation_report.json` across `UNSW-NB15` (Binary `96.67%` Acc, `0.9643` AUC; 7-Class `96.00%` Acc, `0.9819` AUC), `NSL-KDD` (Binary `99.11%` Acc; 7-Class `90.37%` Acc), and `CIC-IDS2017` (7-Class `84.72%` Acc).
2. **Programmatic 300-DPI Experimental Performance Charts (`report/generate_chapter4_charts.py`):**
   - Generated data-driven 300-DPI evaluation charts in `report/figures/` (`fig4_1_training_curves.png` through `fig4_6_live_detection_telemetry.png`).
3. **Live Web Application Execution & Genuine Website Screenshot Capture (`report/capture_website_screenshots.py`):**
   - Launched the Flask + React production application (`app.py`), authenticated via `POST /api/auth/login` (`HS256` JWT + cookie), started active Wi-Fi packet monitoring (`Wi-Fi Realtek RTL8821CE — 172.20.10.8`), and drove headless Chrome via Chrome DevTools Protocol (`1440x900` @ `1.5x` DPI) to capture **10 genuine high-resolution website screenshots** (`ui_1_landing_page.png` through `ui_10_audit_trail_table.png`), with zero "Trojan Horse" UI elements.
4. **Condensed 15-Page Chapter 4 Deliverables (`Chapter_4_Results_and_Analysis.pdf`, `.docx`, `.md`):**
   - Edited and condensed Chapter 4 from 20 pages to **exactly 15 PDF pages** (`Total PDF Pages Generated: 15`), removing repetitive background theory and redundant tables while retaining all verified metrics, **8 essential tables (`Tables 4.1–4.8`)**, **3 empirical evaluation figures (`Figures 4.5–4.7`)**, and **9 actual website implementation screenshots (`Figures 4.1–4.4` in Section 4.3 and `Figures 4.8–4.12` in Section 4.6)**.

---

## 2. Inventory of Files Created in `report/`

| File / Directory Path | Type | Description |
| :--- | :--- | :--- |
| `report/Chapter_3_System_Design_and_Implementation.pdf` | PDF Document | Compiled 20-page academic PDF report for Chapter 3 |
| `report/Chapter_3_System_Design_and_Implementation.docx` | Word Document | Editable Microsoft Word `.docx` version of Chapter 3 |
| `report/Chapter_3_System_Design_and_Implementation.md` | Markdown Source | Complete Markdown source for Chapter 3 |
| `report/Chapter_4_Results_and_Analysis.pdf` | PDF Document | Compiled **exactly 15-page** academic PDF report for Chapter 4 with embedded website screenshots |
| `report/Chapter_4_Results_and_Analysis.docx` | Word Document | Editable Microsoft Word `.docx` version of the 15-page Chapter 4 with embedded website screenshots |
| `report/Chapter_4_Results_and_Analysis.md` | Markdown Source | Condensed Markdown source for Chapter 4 (`Sections 4.1–4.10`, `Tables 4.1–4.8`, `Figures 4.1–4.12`) |
| `report/figures/ui_1_landing_page.png` | Live UI PNG | Figure 4.1: Academic Project Overview and Landing Page (`/`) |
| `report/figures/ui_2_login_portal.png` | Live UI PNG | Figure 4.2: Zero Trust Security Portal (`/login`) |
| `report/figures/ui_4_datasets_management.png` | Live UI PNG | Figure 4.3: Datasets Inventory and Active Selection Screen |
| `report/figures/ui_6_model_training.png` | Live UI PNG | Figure 4.4: AI Model Training Console |
| `report/figures/fig4_1_training_curves.png` | 300-DPI PNG | Figure 4.5: Epoch-by-Epoch Training/Validation Loss, Accuracy & Frobenius Norm $\Delta W$ |
| `report/figures/fig4_2_unsw_binary_cm_roc.png` | 300-DPI PNG | Figure 4.6: UNSW-NB15 Holdout Binary Confusion Matrix & ROC Curve (`AUC = 0.9643`) |
| `report/figures/fig4_4_metrics_comparison_bar.png` | 300-DPI PNG | Figure 4.7: Comparative Bar Chart of Holdout Metrics Across Datasets |
| `report/figures/ui_3_admin_dashboard.png` | Live UI PNG | Figure 4.8: Administrator Security Operations Dashboard (`/dashboard`) |
| `report/figures/ui_5_dataset_comparison.png` | Live UI PNG | Figure 4.9: NIDS Dataset Comparison Matrix Screen |
| `report/figures/ui_7_performance_evaluation.png` | Live UI PNG | Figure 4.10: System Performance Evaluation and 7-Class Confusion Matrix Screen |
| `report/figures/ui_8_live_detection.png` | Live UI PNG | Figure 4.11: Live Network Traffic Detection and Intrusion Prediction Console |
| `report/figures/ui_9_audit_logs.png` | Live UI PNG | Figure 4.12: Behavioral Analytics Integration and Zero Trust Audit Trail Console |
| `report/figures/ui_10_audit_trail_table.png` | Live UI PNG | Supplementary scrolled view of the Tamper-Resistant Zero Trust Audit Log Table |
| `report/capture_website_screenshots.py` | Python Script | Launches live Flask/React server and captures genuine UI screenshots via Chrome CDP |
| `report/generate_chapter4_charts.py` | Python Script | Generates empirical evaluation charts for Chapter 4 |
| `report/generate_chapter4_pdf.py` | Python Script | Compiles the exact 15-page `Chapter_4_Results_and_Analysis.pdf` |
| `report/generate_chapter4_docx.py` | Python Script | Compiles `Chapter_4_Results_and_Analysis.docx` |
| `report/ACTION_LOG.md` | Markdown Log | Complete log of all actions and deliverables created inside `report/` |
