import streamlit as st
from google import genai

def init_gemini_client(api_key):
    """
    Initializes the Gemini client and chat session.
    """
    try:
        client = genai.Client(api_key=api_key)
        chat_session = client.chats.create(model="gemini-2.0-flash")
        st.session_state.gemini_client = client
        st.session_state.chat_session = chat_session
        return True, None
    except Exception as e:
        return False, str(e)

def generate_text_stream(prompt):
    """
    Generates text from Gemini model and yields chunks.
    """
    if 'chat_session' not in st.session_state or st.session_state.chat_session is None:
        yield "Ошибка: Сессия чата не инициализирована. Проверьте API ключ."
        return

    chat = st.session_state.chat_session
    try:
        response = chat.send_message_stream(prompt)
        for chunk in response:
            if chunk.text:
                yield chunk.text
    except Exception as e:
        yield f"\n[Ошибка генерации текста: {str(e)}]"
