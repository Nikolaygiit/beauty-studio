import streamlit as st
from google import genai
from google.genai import types

def init_chat_session(api_key):
    """Initializes the Gemini chat session."""
    if not api_key:
        return None, None

    try:
        client = genai.Client(api_key=api_key)
        chat = client.chats.create(model="gemini-2.0-flash")
        return client, chat
    except Exception as e:
        st.error(f"Failed to initialize Gemini client: {e}")
        return None, None

def generate_text_stream(chat_session, prompt):
    """Generates a streaming text response from Gemini."""
    if not chat_session:
        yield "API key not set or session not initialized."
        return

    try:
        response = chat_session.send_message_stream(prompt)
        for chunk in response:
            if chunk.text:
                yield chunk.text
    except Exception as e:
        yield f"\n\n**Error:** {str(e)}"
