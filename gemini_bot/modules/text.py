import streamlit as st
from google import genai
from google.genai import types

def init_gemini_client(api_key: str):
    """Инициализирует и возвращает клиент Gemini и сессию чата."""
    try:
        # Инициализация клиента
        client = genai.Client(api_key=api_key)

        # Настройка системных инструкций
        config = types.GenerateContentConfig(
            system_instruction="Ты — умный и дружелюбный AI-ассистент. Всегда отвечай на русском языке.",
            temperature=0.7
        )

        # Создание сессии чата с моделью gemini-2.0-flash (согласно memory)
        chat = client.chats.create(
            model="gemini-2.0-flash",
            config=config
        )

        return client, chat, None
    except Exception as e:
        return None, None, f"Ошибка инициализации Gemini: {str(e)}"

def generate_text_stream(chat_session, prompt: str):
    """
    Генерирует потоковый ответ текста.
    Возвращает генератор или бросает исключение, которое должно быть обработано в app.py
    """
    return chat_session.send_message_stream(prompt)
