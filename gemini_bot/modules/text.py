import streamlit as st
from google import genai
from google.genai import types

def init_chat_session(api_key):
    """Initializes the chat session if it doesn't exist."""
    if 'chat_session' not in st.session_state:
        client = genai.Client(api_key=api_key)
        st.session_state.chat_session = client.chats.create(model='gemini-2.0-flash')

def generate_text_response(api_key, prompt):
    """Generates a text response using Gemini 2.0 Flash in a chat session."""
    init_chat_session(api_key)
    chat = st.session_state.chat_session

    try:
        response_stream = chat.send_message_stream(prompt)
        for chunk in response_stream:
            if chunk.text:
                yield chunk.text
    except Exception as e:
        yield f"Произошла ошибка при генерации текста: {e}"
