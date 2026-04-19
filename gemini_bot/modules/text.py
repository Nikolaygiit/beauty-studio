from google import genai
from google.genai import types

def generate_text_stream(prompt, api_key, chat_session):
    """
    Generates text using gemini-2.0-flash model with streaming response.
    Returns a generator yielding the text chunks or error messages.
    """
    try:
        if chat_session is None:
            # Note: The chat_session should be initialized and stored in app.py
            # but if it isn't passed, we yield an error.
            yield "Ошибка: Сессия чата не инициализирована."
            return

        response = chat_session.send_message_stream(prompt)
        for chunk in response:
            if chunk.text:
                yield chunk.text
    except Exception as e:
        yield f"Произошла ошибка при генерации текста: {e}"

def init_chat_session(api_key):
    """
    Initializes a chat session using the gemini-2.0-flash model.
    Returns (client, chat_session) or (None, None) on failure.
    """
    try:
        client = genai.Client(api_key=api_key)
        chat = client.chats.create(model="gemini-2.0-flash")
        return client, chat
    except Exception as e:
        print(f"Error initializing Gemini chat session: {e}")
        return None, None
