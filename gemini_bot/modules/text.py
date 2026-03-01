import google.generativeai as genai

def generate_text(prompt: str, api_key: str, chat_session=None):
    """
    Generates text using Gemini model with history.
    """
    try:
        genai.configure(api_key=api_key)

        if chat_session is None:
            model = genai.GenerativeModel('gemini-1.5-flash')
            chat_session = model.start_chat(history=[])

        response = chat_session.send_message(prompt)
        return response.text, chat_session
    except Exception as e:
        return f"Произошла ошибка при генерации текста: {str(e)}", chat_session
