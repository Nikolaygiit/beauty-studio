from google import genai
import streamlit as st

def init_chat_session(api_key: str):
    """Initializes the Gemini chat session using the provided API key."""
    if not api_key:
        return None
    try:
        client = genai.Client(api_key=api_key)
        # Using the gemini-2.0-flash model as requested
        chat_session = client.chats.create(model="gemini-2.0-flash")
        return chat_session
    except Exception as e:
        st.error(f"Failed to initialize Gemini Client: {e}")
        return None

def generate_text_stream(prompt: str, chat_session):
    """Generates a text stream from Gemini."""
    if not chat_session:
        yield "Ошибка: Сессия чата не инициализирована. Проверьте API ключ."
        return

    try:
        response_stream = chat_session.send_message_stream(prompt)
        for chunk in response_stream:
            yield chunk.text
    except Exception as e:
        yield f"Произошла ошибка при генерации текста: {e}"
