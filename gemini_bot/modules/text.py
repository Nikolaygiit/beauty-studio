from google import genai
from google.genai import types

def init_chat_session(api_key):
    """Initializes and returns a Gemini chat session."""
    try:
        client = genai.Client(api_key=api_key)
        # Using gemini-2.5-flash as specified
        chat = client.chats.create(model="gemini-2.5-flash")
        return chat
    except Exception as e:
        return f"Ошибка инициализации чата: {e}"

def generate_text_stream(chat_session, prompt):
    """Generates text as a stream using the provided chat session."""
    try:
        response_stream = chat_session.send_message_stream(prompt)
        for chunk in response_stream:
            yield chunk.text
    except Exception as e:
        yield f"\n\n**Ошибка генерации текста:** {e}"
