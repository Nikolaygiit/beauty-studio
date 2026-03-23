def generate_text(prompt, chat_session):
    """
    Generate text using Gemini 2.0 Flash chat session.
    Expects google-genai package object.
    """
    try:
        response = chat_session.send_message(prompt)
        return response.text
    except Exception as e:
        return f"Произошла ошибка при генерации текста: {str(e)}"

def init_chat_session(client):
    """
    Initialize chat session.
    """
    try:
        return client.chats.create(model="gemini-2.0-flash")
    except Exception as e:
        return None
