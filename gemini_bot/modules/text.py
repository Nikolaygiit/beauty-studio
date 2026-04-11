import streamlit as st
from google import genai

def initialize_chat(api_key):
    """Initializes or re-initializes the Gemini chat session."""
    if "gemini_client" not in st.session_state or st.session_state.get("current_api_key") != api_key:
        client = genai.Client(api_key=api_key)
        st.session_state.gemini_client = client
        st.session_state.current_api_key = api_key
        st.session_state.chat_session = client.chats.create(model="gemini-2.0-flash")
    return st.session_state.chat_session

def generate_text(prompt, api_key):
    """Generates text from Gemini, streaming the response."""
    try:
        chat_session = initialize_chat(api_key)
        response = chat_session.send_message_stream(prompt)
        for chunk in response:
            if chunk.text:
                yield chunk.text
    except Exception as e:
        yield f"\n\nОшибка при генерации текста: {str(e)}"
