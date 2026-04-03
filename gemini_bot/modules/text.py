from google import genai
from google.genai import types

def init_chat_session(api_key):
    """Initializes the Gemini chat session."""
    client = genai.Client(api_key=api_key)
    chat = client.chats.create(model="gemini-2.0-flash")
    return chat

def generate_text_stream(chat_session, prompt):
    """Generates text using the Gemini model with streaming."""
    try:
        response = chat_session.send_message_stream(prompt)
        for chunk in response:
            if chunk.text:
                yield chunk.text
    except Exception as e:
        yield f"\n\n[Ошибка генерации текста: {e}]"
