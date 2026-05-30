import streamlit as st
from google import genai
from google.genai import types

def init_gemini(api_key: str):
    """
    Инициализирует клиент Gemini и создает новую сессию чата,
    если она еще не создана.
    """
    # Если изменился API-ключ или клиент не существует, пересоздаем
    if 'gemini_client' not in st.session_state or st.session_state.get('current_api_key') != api_key:
        client = genai.Client(api_key=api_key)
        st.session_state.gemini_client = client
        st.session_state.current_api_key = api_key

        # Настройка системной инструкции
        config = types.GenerateContentConfig(
            system_instruction="Ты - полезный AI-помощник. Твоя задача - отвечать на вопросы пользователя и помогать ему. Всегда отвечай только на русском языке, независимо от языка запроса."
        )

        # Создание сессии чата
        st.session_state.chat_session = client.chats.create(
            model="gemini-2.0-flash",
            config=config
        )

def generate_text_stream(prompt: str):
    """
    Генерирует потоковый текстовый ответ от Gemini.
    """
    chat_session = st.session_state.chat_session
    try:
        response = chat_session.send_message_stream(prompt)
        for chunk in response:
            if chunk.text:
                yield chunk.text
    except Exception as e:
        yield f"\n\n**Ошибка при генерации текста:** {str(e)}"
