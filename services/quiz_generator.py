from utils.gemini import model


def generate_quiz(notes: str) -> str:

    prompt = f"""
    Generate 10 multiple choice questions.

    Provide answer key also.

    Notes:

    {notes}
    """

    response = model.generate_content(prompt)

    return response.text