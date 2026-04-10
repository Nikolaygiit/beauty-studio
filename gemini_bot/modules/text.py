import streamlit as st
from google import genai
from google.genai import errors

def init_chat_session(api_key):
    """Initializes the Gemini chat session and stores it in session state."""
    try:
        if not api_key:
            st.error("Пожалуйста, введите ваш Google API Key в боковой панели.")
            return False

        # Use google-genai
        client = genai.Client(api_key=api_key)
        # Store the client in session state to prevent HTTP connection closure
        st.session_state.gemini_client = client

        # Create a chat session
        chat_session = client.chats.create(model="gemini-2.0-flash")
        st.session_state.chat_session = chat_session

        return True
    except errors.APIError as e:
        st.error(f"Ошибка API: {e}")
        return False
    except Exception as e:
        st.error(f"Ошибка инициализации чата: {e}")
        return False

def generate_text_response(prompt):
    """Generates a text response using the active chat session."""
    if 'chat_session' not in st.session_state or 'gemini_client' not in st.session_state:
        st.error("Сессия чата не инициализирована.")
        return None

    try:
        # Stream response
        chat = st.session_state.chat_session
        response = chat.send_message_stream(prompt)
        for chunk in response:
            if chunk.text:
                yield chunk.text
    except Exception as e:
        st.error(f"Произошла ошибка при генерации ответа: {e}")
        return None
