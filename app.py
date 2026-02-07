import streamlit as st
import time
from streamlit_webrtc import webrtc_streamer

from vision.webrtc_processor import VisionWebRTCProcessor
from resume.parser import extract_resume_text
from backend.data_logger import init_user_csvs, get_user_dir
from nemai.examiner import NemAIExaminer
from state_engine.state_tracker import ConversationState, log_session
from evaluation.report_generator import generate_report

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(layout="wide", page_title="Autonomous AI Viva Examiner")

# -------------------------------------------------
# VIDEO CSS (FIXED SIZE + STABLE)
# -------------------------------------------------
st.markdown(
    """
    <style>
    video {
        width: 100% !important;
        height: 360px !important;
        border-radius: 12px;
        border: 2px solid #4A4A4A;
        object-fit: cover;
        object-position: center;
        transform: scale(1.2); /* 👈 ZOOM IN */
        background: black;
    }
    </style>
    """,
    unsafe_allow_html=True
)


VIVA_DURATION_MINUTES = 10
VIVA_DURATION_SECONDS = VIVA_DURATION_MINUTES * 60

# -------------------------------------------------
# LOGIN
# -------------------------------------------------
if "username" not in st.session_state:
    st.session_state.username = None

if st.session_state.username is None:
    st.title("🔐 Login")
    username = st.text_input("Username")
    if st.button("Login") and username.strip():
        st.session_state.username = username.strip()
        st.rerun()
    st.stop()

# -------------------------------------------------
# ROLE + RESUME
# -------------------------------------------------
st.title("🎯 Interview Configuration")

role_type = st.selectbox("Apply as", ["Intern", "Job"])
job_role = st.selectbox(
    "Target Role",
    ["SDE", "ML Intern", "Data Scientist", "MERN Stack Developer"]
)

resume_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
if not resume_file:
    st.stop()

with st.spinner("📄 Parsing resume and preparing interview..."):
    resume_text = extract_resume_text(resume_file)
    init_user_csvs(st.session_state.username)

# -------------------------------------------------
# SESSION INIT
# -------------------------------------------------
if "init" not in st.session_state:
    st.session_state.init = True
    st.session_state.started = True
    st.session_state.finished = False
    st.session_state.start_time = time.time()
    st.session_state.chat = []
    st.session_state.current_question = None
    st.session_state.pending_question = False

    st.session_state.state = ConversationState(role_type)
    st.session_state.examiner = NemAIExaminer(
        role_type, job_role, resume_text
    )

# -------------------------------------------------
# TIMER
# -------------------------------------------------
elapsed = int(time.time() - st.session_state.start_time)
remaining = max(0, VIVA_DURATION_SECONDS - elapsed)

if remaining == 0:
    st.session_state.finished = True

# -------------------------------------------------
# FIRST QUESTION
# -------------------------------------------------
if st.session_state.started and not st.session_state.chat:
    with st.spinner("🧠 Generating first question..."):
        q = st.session_state.examiner.ask_question(
            st.session_state.state
        )
    st.session_state.current_question = q
    st.session_state.chat.append(("Examiner", q))

# -------------------------------------------------
# HEADER
# -------------------------------------------------
st.title("🎓 Autonomous AI Viva Examiner")

mins, secs = divmod(remaining, 60)
st.info(f"⏱️ Time Remaining: **{mins:02d}:{secs:02d}**")

col1, col2 = st.columns([2, 1])

# -------------------------------------------------
# CHAT
# -------------------------------------------------
with col1:
    for role, msg in st.session_state.chat:
        st.markdown(f"**{role}:** {msg}")

    if not st.session_state.finished:
        with st.form("answer_form", clear_on_submit=True):
            answer = st.text_input("Your Answer")
            submitted = st.form_submit_button("Submit Answer")

        if submitted and answer.strip():
            st.session_state.chat.append(("Student", answer))
            st.session_state.state.update(answer)

            log_session(
                st.session_state.state,
                st.session_state.current_question,
                answer,
                st.session_state.username
            )

            if st.session_state.state.state != "WRAP_UP":
                st.session_state.pending_question = True
            else:
                st.session_state.finished = True

    if st.button("🛑 End Viva"):
        st.session_state.finished = True

# -------------------------------------------------
# NEXT QUESTION (NO DOUBLE CLICK)
# -------------------------------------------------
if (
    st.session_state.pending_question
    and not st.session_state.finished
):
    with st.spinner("🧠 Generating next question..."):
        q = st.session_state.examiner.ask_question(
            st.session_state.state
        )
    st.session_state.current_question = q
    st.session_state.chat.append(("Examiner", q))
    st.session_state.pending_question = False

# -------------------------------------------------
# CAMERA (ADJUSTED FRAME)
# -------------------------------------------------
with col2:
    st.subheader("👁️ Live Attention Monitoring")

    if not st.session_state.finished:
        ctx = webrtc_streamer(
            key="vision",
            video_processor_factory=VisionWebRTCProcessor,
            media_stream_constraints={"video": True, "audio": False},
            async_processing=True,
            video_html_attrs={
                "autoPlay": True,
                "controls": False,
                "muted": True,
            },
        )

        if ctx.video_processor:
            ctx.video_processor.set_user(st.session_state.username)

# -------------------------------------------------
# FINAL REPORT
# -------------------------------------------------
if st.session_state.finished:

    if "final_report" not in st.session_state:
        metrics = {
            "blinks": 0,
            "gaze": [],
            "pupil": [],
            "multiple_face_frames": 0
        }

        if "ctx" in locals() and ctx and ctx.video_processor:
            if ctx.video_processor.vision:
                metrics = ctx.video_processor.vision.metrics

        st.session_state.final_report = generate_report(
            st.session_state.state,
            metrics,
            st.session_state.username
        )

    st.markdown("---")
    st.title("✅ Viva Session Ended")

    total_m, total_s = divmod(elapsed, 60)
    st.success(f"⏱️ Duration: {total_m} min {total_s} sec")

    st.subheader("📊 Final Evaluation")
    st.json(st.session_state.final_report)

    user_dir = get_user_dir(st.session_state.username)

    st.download_button(
        "⬇️ Download Final Report",
        open(f"{user_dir}/final_report.csv", "rb"),
        file_name="final_report.csv"
    )

    st.download_button(
        "⬇️ Session Logs",
        open(f"{user_dir}/session_logs.csv", "rb"),
        file_name="session_logs.csv"
    )

    st.download_button(
        "⬇️ Attention Metrics",
        open(f"{user_dir}/attention_metrics.csv", "rb"),
        file_name="attention_metrics.csv"
    )

    st.markdown("### 🎉 Thank you for attending the viva!")
