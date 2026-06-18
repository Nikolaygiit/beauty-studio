from google import genai
from google.genai import types
import streamlit as st

def get_client(api_key: str):
    if not api_key:
        return None
    try:
        return genai.Client(api_key=api_key)
    except Exception as e:
        return None

def initialize_chat_session(client):
    if not client:
        return None

    try:
        config = types.GenerateContentConfig(
            system_instruction="Ты — полезный ИИ-ассистент. Отвечай всегда на русском языке."
        )
        return client.chats.create(model="gemini-2.0-flash", config=config)
    except Exception as e:
        st.error(f"Error initializing chat: {str(e)}")
        return None

def generate_text_stream(chat_session, prompt: str):
    if not chat_session:
        yield "Ошибка: Сессия чата не инициализирована."
        return

    try:
        response_stream = chat_session.send_message_stream(prompt)
        for chunk in response_stream:
            if chunk.text:
                yield chunk.text
    except Exception as e:
        yield f"\n\nПроизошла ошибка при генерации ответа: {str(e)}"
