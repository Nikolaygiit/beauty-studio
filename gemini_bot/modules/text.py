import streamlit as st
from google import genai

def init_chat_session(api_key):
    """Initializes the Gemini chat session."""
    try:
        client = genai.Client(api_key=api_key)
        chat = client.chats.create(model="gemini-2.0-flash")
        return chat
    except Exception as e:
        st.error(f"Ошибка инициализации Gemini API: {e}")
        return None

def generate_text_stream(chat_session, prompt):
    """Generates a text response stream using the chat session."""
    try:
        response = chat_session.send_message_stream(prompt)
        for chunk in response:
            if chunk.text:
                yield chunk.text
    except Exception as e:
        yield f"\n\n[Ошибка при генерации текста: {str(e)}]"
