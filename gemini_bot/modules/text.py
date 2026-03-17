import streamlit as st
from google import genai
from google.genai import types

def init_chat_session(api_key):
    """Инициализирует сессию чата Gemini."""
    try:
        client = genai.Client(api_key=api_key)
        # Создаем сессию с моделью gemini-2.0-flash
        chat = client.chats.create(model="gemini-2.0-flash")
        return chat
    except Exception as e:
        st.error(f"Ошибка инициализации Gemini: {str(e)}")
        return None

def generate_text_stream(chat_session, prompt):
    """Генерирует текст (потоковый ответ) через Gemini."""
    try:
        response_stream = chat_session.send_message_stream(prompt)
        for chunk in response_stream:
            yield chunk.text
    except Exception as e:
        yield f"Произошла ошибка при обращении к Gemini API: {str(e)}"
