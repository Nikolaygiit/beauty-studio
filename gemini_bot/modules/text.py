from google import genai
import streamlit as st

def initialize_chat(api_key):
    """Initializes the Gemini client and chat session."""
    try:
        client = genai.Client(api_key=api_key)
        chat = client.chats.create(model='gemini-2.0-flash')
        return client, chat
    except Exception as e:
        st.error(f"Error initializing chat: {e}")
        return None, None

def generate_text(chat, prompt):
    """Generates text from the chat session and streams the response."""
    try:
        response_stream = chat.send_message_stream(prompt)
        return response_stream
    except Exception as e:
        st.error(f"Error generating text: {e}")
        return None
