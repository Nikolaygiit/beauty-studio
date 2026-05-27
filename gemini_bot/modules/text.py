import streamlit as st
from google import genai
from google.genai import types

def init_gemini_client(api_key: str):
    """Initializes the Gemini client if not already present or if the API key has changed."""
    if "gemini_client" not in st.session_state or st.session_state.get("current_api_key") != api_key:
        client = genai.Client(api_key=api_key)
        st.session_state.gemini_client = client
        st.session_state.current_api_key = api_key
        st.session_state.chat_history = []
        st.session_state.chat_session = client.chats.create(
            model="gemini-2.0-flash",
            config=types.GenerateContentConfig(
                system_instruction="Всегда отвечай на русском языке.",
                temperature=0.7,
            )
        )
    return st.session_state.gemini_client

def generate_text_stream(prompt: str):
    """Generates text stream using the Gemini client's chat session."""
    try:
        response = st.session_state.chat_session.send_message_stream(prompt)
        for chunk in response:
            if chunk.text:
                yield chunk.text
    except Exception as e:
        yield f"Произошла ошибка при генерации текста: {e}"
