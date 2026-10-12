# Brag Video Plan — JNNCE Academic Landing Page, Model Training & Zero Trust AI-NIDS (With Voiceover)

## 1. Nine-Question Rubric

1. **What does this project do, in one plain sentence?**
   An academic Zero Trust AI-Powered Network Intrusion Detection System developed at JNNCE (Department of Information Science & Engineering, Batch No. 34) that configures and trains deep neural models on benchmark intrusion datasets (`UNSW-NB15`, `NSL-KDD`, `CIC-IDS2017`), evaluates multi-class attack confusion matrices, and classifies live network packet flows in real time.

2. **Who is it for, and what problem does it solve?**
   Designed for academic evaluation (Final Year B.E. ISE 2023–2027, VTU Belagavi / AICTE) and network security analysts to overcome static perimeter firewall limitations by continuously training and applying AI-based Zero Trust flow inspection.

3. **What is the single strongest proof point in the codebase?**
   The complete **Academic Portal → Live Model Training → 7×7 Attack Evaluation → Real-Time Packet Detection** workflow: starting from the official JNNCE Academic Landing Page (`LandingPage.jsx`), into the interactive **Model Training Console** (`TrainingView.jsx` with configurable dataset rows, `Random Seed 42`, `10 Epochs`, `Batch Size 32`, `Learning Rate 0.001`, and live `t_acc` / `t_loss` convergence curves across `E1–E10`), followed by the **7×7 Multi-Class Confusion Matrix** (`96.0%` accuracy across `Analysis`, `DoS`, `Exploits`, `Fuzzers`, `Generic`, `Normal`, `Reconnaissance`) and real-time Scapy packet capture.

4. **What tone fits best?**
   **Polished launch** — clean, authoritative academic engineering presentation with live ML training, natural voiceover narration (`af_heart`, `18.43s`), and cybersecurity telemetry.

5. **What is the hook in the first 2 seconds?**
   The full-frame **JNNCE Academic Landing Page** (`JAWAHARLAL NEHRU NATIONAL COLLEGE OF ENGINEERING, SHIVAMOGGA • DEPARTMENT OF INFORMATION SCIENCE AND ENGINEERING • BATCH NO. 34`) accompanied by the opening voiceover: *"JNNCE Batch 34 presents our Zero Trust AI Network Intrusion Detection System."*

6. **What is the 5-beat story arc (Voiceover-Synced to `20.00s`)?**
   - **Beat 1 (`0.00s – 5.10s`) — Official JNNCE Academic Landing Page (`LandingPage.jsx`)**: Centered institutional layout on `#f4f7fc` featuring the JNNCE College Emblem (`/jnnce_logo.png`), VTU Belagavi & AICTE affiliation, `FINAL YEAR B.E. ACADEMIC PROJECT (2023–2027)`, `Zero Trust AI-Powered Network Intrusion Detection System`, `PROJECT BATCH NO. 34`, and an animated cursor clicking **`Explore Dashboard →`**.
   - **Beat 2 (`5.10s – 10.00s`) — Interactive Model Training Console & Convergence Curves (`TrainingView.jsx`)**: Two-column **Model Training Console** showing hyperparameter configuration (`UNSW-NB15`, `25,000` stratified rows, `Seed 42`, `10 Epochs`, `Batch Size 32`, `LR 0.001`) and live training progress (`Epoch 1/10 → 10/10`, `t_loss 0.8420 → 0.1142`, `t_acc 74.20% → 96.00%`, and live `E1–E10` convergence graph).
   - **Beat 3 (`10.00s – 14.20s`) — 7×7 Multi-Class Attack Confusion Matrix (`ModelDetailsView.jsx`)**: Displays the trained model's **7×7 Confusion Matrix** across all 7 real attack categories (`Analysis`, `DoS`, `Exploits`, `Fuzzers`, `Generic`, `Normal`, `Reconnaissance`) with `96.0%` accuracy alongside `NSL-KDD` (`91.0%`) and `CIC-IDS2017` (`85.4%`) benchmarks.
   - **Beat 4 (`14.20s – 17.80s`) — Real-Time Live Packet Capture (`LiveDetectionView.jsx`)**: Streams live bidirectional packet flows on `Loopback Pseudo-Interface 1 / Wi-Fi`, verifying `Normal` traffic and isolating `Exploits` and `DoS` flood attacks.
   - **Beat 5 (`17.80s – 20.00s`) — Official JNNCE Batch No. 34 Academic End Card**: Clean institutional closing frame with the JNNCE crest, ISE department title, project name, and 4 core proof metrics.

7. **What real UI, workflow, or artifact should stay on screen the longest?**
   The **Official JNNCE Academic Landing Page (`LandingPage.jsx`)** (`5.10s`) and the **Model Training Console (`TrainingView.jsx`)** (`4.90s`), followed by the **7×7 Multi-Class Confusion Matrix** (`4.20s`).

8. **What must NOT appear because it isn't backed by the codebase?**
   No Trojan Horse visuals or references, no fake SaaS pricing, and no invented metrics.

9. **What audio plan fits?**
   - **Voiceover (`af_heart` via Kokoro TTS)**: `assets/voiceover.wav` (`18.43s` duration, starting at `0.30s`) on `data-track-index="3"`, `data-volume="1.0"`.
   - **Music Track**: `happy-beats-business-moves-vol-12-by-ende-dot-app.mp3` ducked to `data-volume="0.14"` under narration, fadeIn `0.6s`, fadeOut `1.4s`.
   - **Sparse SFX Cues**: Soft reveal and UI click accents (`0.22–0.30` volume) supporting transitions without competing with the voiceover.

---

## Voiceover script

> "JNNCE Batch 34 presents our Zero Trust AI Network Intrusion Detection System. Train a five-stage neural classifier across ten live epochs. Achieve ninety-six percent accuracy across seven attack classes, and isolate live packet intrusions in real time."
