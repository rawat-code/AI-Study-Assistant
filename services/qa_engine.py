from utils.gemini import model


def answer_question(
    notes: str,
    question: str
) -> str:

    prompt = f"""
    Notes:

    {notes}

    Question:

    {question}

    Answer only from the notes.
    If not found, say:
    "Information not available in notes."
    """

    response = model.generate_content(prompt)

    return response.text