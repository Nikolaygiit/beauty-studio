import os
from google import genai
from google.genai import types

def init_chat_session(api_key):
    """Initializes the Gemini chat session using google-genai."""
    try:
        client = genai.Client(api_key=api_key)
        # Create a chat session with the gemini-2.0-flash model
        chat_session = client.chats.create(model="gemini-2.0-flash")
        return client, chat_session, None
    except Exception as e:
        return None, None, f"Ошибка инициализации Gemini: {str(e)}"

def generate_text_stream(chat_session, prompt):
    """Generates a text stream using the active chat session."""
    try:
        # We need to yield the chunks as they come
        response_stream = chat_session.send_message_stream(prompt)
        for chunk in response_stream:
            if chunk.text:
                yield chunk.text, None
    except Exception as e:
        yield None, f"Ошибка генерации текста: {str(e)}"
