import streamlit as st

from services.pdf_reader import extract_text
from services.qa_engine import answer_question
from services.quiz_generator import generate_quiz
from services.summarizer import generate_summary

st.set_page_config(
    page_title="AI Study Assistant",
    page_icon="🤖",
    layout="wide"
)

st.markdown("""
<style>
.main {
    padding-top: 1rem;
}

h1 {
    text-align: center;
}

.stButton > button {
    width: 100%;
    border-radius: 12px;
    height: 3em;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

with st.sidebar:

    st.title("📚 AI Study Assistant")

    st.markdown("---")

    st.info("Summer Project 2026")

    st.success("Powered by Gemini AI")

    st.markdown("---")

    st.markdown("""
### Features

✅ PDF Upload

✅ Smart Summary

✅ RAG-Based Question Answering

✅ Quiz Generation

✅ Page Citations
""")

st.title("🤖 AI Study Assistant")

st.markdown("""
### Personalized Learning Using Generative AI + RAG

Upload your notes and let AI help you study smarter.
""")

uploaded_file = st.file_uploader(
    "📄 Upload PDF Notes",
    type=["pdf"]
)

if uploaded_file:

    with st.spinner("Reading PDF..."):
        notes = extract_text(uploaded_file)

    if not notes:

        st.error(
            "No text found in PDF."
        )

        st.stop()

    st.success(
        "PDF Uploaded Successfully 🎉"
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "AI Model",
            "Gemini"
        )

    with col2:
        st.metric(
            "Search",
            "RAG"
        )

    with col3:
        st.metric(
            "Words Extracted",
            len(notes.split())
        )

    st.markdown("---")

    with st.expander(
        "📖 View Extracted Notes"
    ):
        st.write(
            notes[:5000]
        )
    search_mode = st.radio(
        "Search Mode",
        [
            "🚀 Hybrid",
            "📄 PDF Only",
            "🌐 Web Only"
        ],
        horizontal=True)

    tab1, tab2, tab3 = st.tabs(
        [
            "📝 Summary",
            "❓ Q&A",
            "📚 Quiz"
        ]
    )

    with tab1:

        if st.button(
            "🚀 Generate Summary"
        ):

            with st.spinner(
                "Generating Summary using guardials..."
            ):

                summary = generate_summary(
                    notes
                )

            st.session_state.summary_text=summary
            if "summary_text" in st.session_state:
                st.markdown(st.session_state.summary_text)

            st.download_button(
                "📥 Download Summary",
                summary,
                file_name="summary.txt"
            )

    with tab2:

        question = st.text_input(
            "Ask a question from your notes"
        )

        if st.button(
            "🤖 Get Answer"
        ):

            if question:

                with st.spinner(
                    "Searching Notes..."
                ):

                    answer = answer_question(
                        uploaded_file,
                        question,search_mode
                    )

                st.write(
                    answer
                )

            else:

                st.warning(
                    "Please enter a question."
                )

    with tab3:

        if st.button(
            "📚 Generate Quiz"
        ):

            with st.spinner(
                "Creating a structured quiz..."
            ):
                

                quiz = generate_quiz(
                    notes,num_questions=10
                )

            if quiz:
                st.session_start.quiz_list=quiz
            else:
                st.error("failed to generate quiz!!,try again!!")
            if "quiz_list" in st.session_state and st.session_state.quiz_list:
                score=0
                for idx,item in enumerate(st.session_state.quiz_list):
                    st.markdown(f"**Q{idx+1}:{item['question']}**")
                    user_ans=st.radio(
                    "select your option:",
                    item['options'],
                    key=f"quiz_q_{idx}"
                    ) 
                    if user_ans==item['answer']:
                        score=+1

                st.metric(label="your current score",value=f"{score}/{len(st.session_state.quiz_list)}")

            st.download_button(
                "📥 Download Quiz",
                quiz,
                file_name="quiz.txt"
            )

else:

    st.info(
        "Upload a PDF to begin."
    )

st.markdown("---")

st.caption(
    "Developed by Himanshu Rawat and Aditya badatya | AI Study Assistant"
)