from google import genai
from google.genai import types
import streamlit as st

def get_gemini_client(api_key):
    """Initializes and returns the Gemini client."""
    try:
        client = genai.Client(api_key=api_key)
        return client
    except Exception as e:
        st.error(f"Failed to initialize Gemini Client: {e}")
        return None

def initialize_chat_session(client):
    """Initializes a new chat session."""
    try:
        # Create a new chat session using gemini-2.0-flash
        chat = client.chats.create(model="gemini-2.0-flash")
        return chat
    except Exception as e:
        st.error(f"Failed to create chat session: {e}")
        return None

def generate_text_stream(chat_session, prompt):
    """Streams text generation from the active chat session."""
    try:
        response_stream = chat_session.send_message_stream(prompt)
        return response_stream
    except Exception as e:
        return f"Произошла ошибка при генерации текста: {e}"
