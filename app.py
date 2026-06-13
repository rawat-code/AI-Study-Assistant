import streamlit as st

from services.pdf_reader import extract_text
from services.qa_engine import answer_question
from services.quiz_generator import generate_quiz
from services.summarizer import generate_summary

st.set_page_config(
    page_title="AI Study Assistant",
    page_icon="📚",
    layout="wide"
)

st.title("📚 AI Study Assistant")

uploaded_file = st.file_uploader(
    "Upload PDF Notes",
    type=["pdf"]
)

if uploaded_file:

    notes = extract_text(uploaded_file)
    st.subheader("Extracted Text Preview")

    with st.expander("View Extracted Text"):
        st.write(notes[:3000])

    if not notes:
        st.error(
            "No text found in PDF."
        )
        st.stop()

    st.success(
        "PDF uploaded successfully."
    )

    tab1, tab2, tab3 = st.tabs(
        [
            "Summary",
            "Q&A",
            "Quiz"
        ]
    )

    with tab1:

        if st.button(
            "Generate Summary"
        ):
            with st.spinner(
                "Generating..."
            ):
                summary = generate_summary(
                    notes
                )

            st.write(summary)

    with tab2:

        question = st.text_input(
            "Ask a Question"
        )

        if st.button(
            "Get Answer"
        ):

            if question:

                with st.spinner(
                    "Thinking..."
                ):
                    answer = answer_question(
                        notes,
                        question
                    )

                st.write(answer)

    with tab3:

        if st.button(
            "Generate Quiz"
        ):

            with st.spinner(
                "Creating Quiz..."
            ):
                quiz = generate_quiz(
                    notes
                )

            st.write(quiz)