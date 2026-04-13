from google import genai
import streamlit as st

def init_gemini_client(api_key):
    """Initializes the Gemini client."""
    try:
        return genai.Client(api_key=api_key)
    except Exception as e:
        st.error(f"Error initializing Gemini Client: {e}")
        return None

def create_chat_session(client):
    """Creates a chat session."""
    try:
        return client.chats.create(model="gemini-2.0-flash")
    except Exception as e:
        st.error(f"Error creating chat session: {e}")
        return None

def generate_text_stream(chat_session, prompt):
    """Generates text from the chat session as a stream."""
    try:
        response = chat_session.send_message_stream(prompt)
        for chunk in response:
            if chunk.text:
                yield chunk.text
    except Exception as e:
        yield f"\n\n**Error during text generation:** {e}"
