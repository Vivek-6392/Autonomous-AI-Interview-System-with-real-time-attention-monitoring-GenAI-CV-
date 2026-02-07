# 🔥 Autonomous AI Viva Examiner with Attention Monitoring

An end-to-end **Autonomous AI Interview System** that conducts resume-grounded technical vivas, dynamically adapts questions, monitors candidate attention in real time using computer vision, and produces a structured evaluation report.

This project mirrors real-world systems like **Neurema / NemAI** and demonstrates strong skills across **Generative AI, Prompt Engineering, Computer Vision, and System Design**.

---

## 🚀 Key Features

### 🎓 NemAI – Autonomous AI Examiner
- Resume-aware, role-specific technical questioning
- Supports roles:
  - ML Intern
  - SDE
  - Data Scientist
  - MERN Stack Developer
- Dynamic difficulty adjustment
- Follow-up questions based strictly on candidate answers
- Hallucination control via:
  - Resume grounding
  - Role constraints
  - State-aware prompts

---

### 🧠 Prompt Engineering
- Strict system prompts (examiner persona)
- One-time greeting enforcement
- Context-only answering
- Follow-up logic without topic drift
- No chain-of-thought leakage

---

### 👁️ Attention Monitoring (Computer Vision)
- Real-time webcam processing using **WebRTC**
- MediaPipe Face Landmarks
- Blink detection (EAR-based)
- Gaze estimation (vector geometry)
- Pupil size approximation
- Multi-face cheating detection
- Continuous logging to CSV

---

### ⏱️ Timed Viva Session
- Configurable viva duration
- Live countdown timer
- Auto-termination on timeout
- Manual “End Viva” option

---

### 📊 Evaluation Pipeline
- Attention score computation
- Confidence estimation
- Cheating flag
- Final grade generation
- Outputs:
  - `final_report.csv`
  - `session_logs.csv`
  - `attention_metrics.csv`

---

## 🏗️ Tech Stack

| Layer | Tools |
|-----|------|
| Frontend | Streamlit |
| Real-Time Video | streamlit-webrtc |
| LLM | OpenRouter (Mistral / Llama) |
| Backend | Python |
| CV | OpenCV + MediaPipe |
| Math | NumPy (vector geometry) |
| Data | Pandas, CSV |
| State | Custom conversation engine |

---

## 🧩 Project Structure
```bash
autonomous-viva-examiner/
│
├── app.py
├── README.md
│
├── nemai/
│ ├── examiner.py
│ └── prompts.py
│
├── vision/
│ ├── face_mesh.py
│ ├── webrtc_processor.py
│ ├── blink_detector.py
│ ├── gaze_estimator.py
│ └── pupil_tracker.py
│
├── state_engine/
│ └── state_tracker.py
│
├── evaluation/
│ ├── metrics.py
│ ├── scorer.py
│ └── report_generator.py
│
├── resume/
│ └── parser.py
│
├── backend/
│ ├── config.py
│ └── data_logger.py
│
└── data/
├── session_logs.csv
├── attention_metrics.csv
└── final_report.csv
```

---

## 🧠 System Architecture

### High-Level Flow

1. Candidate logs in and uploads resume
2. NemAI initializes interview state
3. First question is generated (with greeting)
4. WebRTC starts live attention monitoring
5. Candidate answers → state updated → follow-up question
6. CV metrics logged continuously
7. Timer expires or session ends
8. Final report generated and saved

---

## 📐 Architecture Diagram
```bash
┌────────────┐
│ Resume │
└─────┬──────┘
│
▼
┌───────────────┐
│ NemAI LLM │◄───────────────┐
│ (OpenRouter) │ │
└─────┬─────────┘ │
│ │
▼ │
┌───────────────┐ │
│ State Engine │ │
│ (Conversation)│ │
└─────┬─────────┘ │
│ │
▼ │
┌───────────────┐ │
│ Streamlit UI │ │
└─────┬─────────┘ │
│ │
▼ │
┌───────────────┐ ┌─────────┴────────┐
│ WebRTC Camera │────► │ Vision Pipeline │
└───────────────┘ │ (MediaPipe + CV) │
└─────────┬────────┘
▼
┌──────────────────┐
│ Evaluation Logic │
└─────────┬────────┘
▼
┌──────────────────┐
│ CSV / Reports │
└──────────────────┘
```
---

## ▶️ How to Run

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```
# 👤 Author

Vivek Yadav

Bachelor of Technology – CSE (AI & ML)
