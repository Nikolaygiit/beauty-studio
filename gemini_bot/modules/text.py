import streamlit as st
from google import genai

def initialize_chat_session(api_key):
    """Initializes and returns the Gemini client and chat session."""
    try:
        client = genai.Client(api_key=api_key)
        chat_session = client.chats.create(model="gemini-2.0-flash")
        return client, chat_session
    except Exception as e:
        st.error(f"Error initializing Gemini client: {e}")
        return None, None

def generate_text_response(chat_session, prompt):
    """Generates text response using the initialized chat session."""
    try:
        response = chat_session.send_message(prompt)
        return response.text
    except Exception as e:
        st.error(f"Error generating text: {e}")
        return f"Произошла ошибка при генерации текста: {e}"
