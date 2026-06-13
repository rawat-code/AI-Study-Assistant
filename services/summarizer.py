from utils.gemini import model


def generate_summary(notes):

    prompt = f"""
    Summarize these notes in simple language.

    Notes:
    {notes}
    """

    response = model.generate_content(prompt)

    return response.text