import streamlit as st
import PyPDF2

@st.cache_data(show_spinner=False)
def extract_resume_text(pdf_file):
    """
    Extract resume text from PDF.
    Cached to avoid repeated heavy parsing on reruns.
    """
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text.strip()
