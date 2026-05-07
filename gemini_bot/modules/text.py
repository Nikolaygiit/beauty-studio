import streamlit as st
from google import genai

def init_gemini_client(api_key: str):
    """Initializes the Gemini client."""
    if not api_key:
        return None
    try:
        client = genai.Client(api_key=api_key)
        return client
    except Exception as e:
        st.error(f"Error initializing Gemini client: {e}")
        return None

def init_chat_session(client):
    """Initializes a new chat session."""
    if not client:
        return None
    try:
        # Use gemini-2.0-flash as per memory
        chat = client.chats.create(model="gemini-2.0-flash")
        return chat
    except Exception as e:
        st.error(f"Error initializing chat session: {e}")
        return None

def generate_text(prompt: str, chat_session):
    """Generates text response using the active chat session."""
    if not chat_session:
        return None, "Chat session not initialized. Please provide a valid API key."
    try:
        response = chat_session.send_message_stream(prompt)
        return response, None
    except Exception as e:
        return None, f"Error generating text: {e}"
