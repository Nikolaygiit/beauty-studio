import streamlit as st
from google import genai
import traceback

def initialize_chat(api_key):
    """Initializes the Gemini client and chat session."""
    try:
        if not api_key:
            return None, "Пожалуйста, введите API ключ Gemini в боковой панели."

        client = genai.Client(api_key=api_key)
        chat = client.chats.create(model="gemini-2.0-flash")
        return chat, client
    except Exception as e:
        return None, f"Ошибка инициализации Gemini: {e}"

def generate_text(prompt, chat_session):
    """Generates text response using Gemini chat session."""
    if not chat_session:
        return None, "Чат сессия не инициализирована."

    try:
        response = chat_session.send_message(prompt)
        return response.text, None
    except Exception as e:
        error_msg = f"Произошла ошибка при генерации текста: {str(e)}\n\n```python\n{traceback.format_exc()}\n```"
        return None, error_msg
