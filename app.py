import streamlit as st

st.set_page_config(
    page_title="AI Study Assistant",
    page_icon="🤖",
    layout="wide"
)

st.write("✅ App Started")

from services.pdf_reader import extract_text
st.write("✅ PDF Reader Loaded")

from services.qa_engine import answer_question
st.write("✅ QA Engine Loaded")

from services.quiz_generator import generate_quiz
st.write("✅ Quiz Generator Loaded")

from services.summarizer import generate_summary
st.write("✅ Summarizer Loaded")

st.title("🤖 AI Study Assistant")

st.success("All imports successful.")