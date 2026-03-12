import streamlit as st
from google import genai

def initialize_chat(api_key):
    try:
        client = genai.Client(api_key=api_key)
        st.session_state.gemini_client = client
        if st.session_state.chat_session is None:
            st.session_state.chat_session = client.chats.create(model='gemini-2.5-flash')
        return True
    except Exception as e:
        st.error(f"Ошибка инициализации Gemini: {e}")
        return False

def generate_text(prompt):
    try:
        if "chat_session" not in st.session_state or st.session_state.chat_session is None:
            raise ValueError("Сессия чата не инициализирована.")
        response = st.session_state.chat_session.send_message_stream(prompt)
        return response
    except Exception as e:
        st.error(f"Ошибка генерации текста: {e}")
        raise e
