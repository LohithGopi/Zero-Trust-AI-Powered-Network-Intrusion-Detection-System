# Composition Brief — JNNCE Academic Landing Page, Model Training & Zero Trust AI-NIDS

## 1. Visual & Brand Identity

- **Canvas**: `1920 × 1080` (`16:9` landscape), `30 fps`, `20.00s` (`data-duration="20"`).
- **Fonts**: `'Instrument Serif'`, `'Inter'`, `'JetBrains Mono'`.
- **Palette**:
  - Academic Light Surface (`LandingPage.jsx` & Dashboard): Background `#f4f7fc`, Card `#ffffff`, Border `#cbd5e1`, Slate Text `#0f172a`, Royal Blue Accent `#1d4ed8`, Emerald Trained/Normal `#047857`, Crimson Alert `#b91c1c`.
  - Calibrated Training Graph Stage (`TrainingView.jsx`): Dark Navy `#070e22`, Accuracy Curve `#3b82f6`, Loss Curve `#f59e0b`.
- **Logo Asset**: `./assets/jnnce_logo.png`.

---

## 2. Scene-by-Scene Storyboard (`20.00s`)

1. **Scene 1 (`0.00s – 4.39s`) — Official JNNCE Academic Landing Page (`LandingPage.jsx`)**
   - Faithful full-width Academic Landing Page with zero Trojan Horse references:
     - Top Header: JNNCE Logo, `Zero Trust AI-Powered NIDS`, `BATCH 34`, `JNNCE Shivamogga • Dept. of Information Science & Engineering`, and `🔒 Login to Security Portal`.
     - Center Academic Card: JNNCE Emblem (`/jnnce_logo.png`), `JAWAHARLAL NEHRU NATIONAL COLLEGE OF ENGINEERING, SHIVAMOGGA`, `DEPARTMENT OF INFORMATION SCIENCE AND ENGINEERING`, `Affiliated to Visvesvaraya Technological University (VTU), Belagavi • Approved by AICTE, New Delhi`, `FINAL YEAR B.E. ACADEMIC PROJECT (2023–2027)`, `Zero Trust AI-Powered Network Intrusion Detection System`, `Phase 1 — Dataset Preparation, Zero Trust Architecture, and AI-Based Intrusion Detection Model`, `PROJECT BATCH NO. 34`, and `🔒 Explore Dashboard →`.
     - Bottom Academic Strip: 3 core project pillars (`01 Dataset Preparation`, `02 AI Model Training`, `03 Real-Time Zero Trust Detection`).
     - Cursor glides to `🔒 Explore Dashboard →` and clicks at `3.82s`.

2. **Scene 2 (`4.39s – 9.29s`) — Model Training Console (`TrainingView.jsx`)**
   - Left Column (`Training Configuration`):
     - `Target NIDS Dataset`: `UNSW-NB15 — unsw_nb15_raw.csv` (`Total Available Rows: 2,540,044`, `Training Rows Selected: 25,000`)
     - `Training Rows Count`: `25,000 Rows Subset`
     - `Random Seed`: `42` • `Epochs (5, 10, 20, 50)`: `10 Epochs (Standard)`
     - `Batch Size`: `32 Samples (Default)` • `Learning Rate`: `0.001`
     - `5-Stage Neural Architecture`: `Sequence Reshape` → `64-Unit LSTM` → `20% Dropout` → `Dense 32 (ReLU)` → `Softmax (7 Classes)` (`29,637 Parameters`)
   - Right Column (`Live Training Progress (UNSW-NB15)`):
     - Progress bar animates `10% → 100%` (`Model Trained` badge)
     - `CURRENT EPOCH`: animates `1 / 10 → 10 / 10`
     - `TRAINING LOSS (T_LOSS)`: animates `0.8420 → 0.1142`
     - `TRAINING ACCURACY (T_ACC)`: animates `74.20% → 96.00%`
     - **Calibrated Training Graph (`#070e22`)**: SVG polylines for `Training Accuracy (t_acc)` (blue) and `Training Loss (t_loss)` (amber) animate smoothly across `E1` through `E10`.

3. **Scene 3 (`9.29s – 13.64s`) — 7×7 Multi-Class Attack Confusion Matrix (`ModelDetailsView.jsx`)**
   - Full 7×7 Confusion Matrix with named attack classes (`Analysis`, `DoS`, `Exploits`, `Fuzzers`, `Generic`, `Normal`, `Reconnaissance`), `96.0%` UNSW-NB15 accuracy, `91.0%` NSL-KDD, `85.4%` CIC-IDS2017, and per-class F1 breakdown.

4. **Scene 4 (`13.64s – 17.47s`) — Real-Time Live Packet Capture (`LiveDetectionView.jsx`)**
   - Live flow inspection on `Loopback Pseudo-Interface 1 / Wi-Fi` classifying `Normal` flows and isolating `Exploits` and `DoS` flood attacks.

5. **Scene 5 (`17.47s – 20.00s`) — Official JNNCE Batch No. 34 Academic End Card**
   - Clean academic closing card with JNNCE Crest, ISE Department credits, project title, and 4 proof badges.
