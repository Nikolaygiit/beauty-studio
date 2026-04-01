import streamlit as st
from google import genai

def init_chat_session(api_key):
    if "chat_session" not in st.session_state or st.session_state.chat_session is None:
        try:
            client = genai.Client(api_key=api_key)
            st.session_state.chat_session = client.chats.create(model="gemini-2.0-flash")
        except Exception as e:
            st.error(f"Ошибка инициализации Gemini: {e}")
            return None
    return st.session_state.chat_session

def generate_text(prompt, api_key):
    chat = init_chat_session(api_key)
    if not chat:
        yield "Не удалось инициализировать сессию с Gemini."
        return

    try:
        response = chat.send_message_stream(prompt)
        for chunk in response:
            if chunk.text:
                yield chunk.text
    except Exception as e:
        yield f"\n\nОшибка при генерации текста: {str(e)}"
