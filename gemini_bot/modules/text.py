from google import genai
import streamlit as st

def get_client(api_key):
    """Initializes the genai client."""
    return genai.Client(api_key=api_key)

def init_chat_session(client):
    """Initializes a chat session using gemini-2.0-flash."""
    return client.chats.create(model="gemini-2.0-flash")

def stream_text_response(chat_session, prompt):
    """Streams the response from the gemini model."""
    try:
        response = chat_session.send_message_stream(prompt)
        return response
    except Exception as e:
        st.error(f"Error during text generation: {e}")
        return None
