from google import genai
import streamlit as st

def get_gemini_client(api_key):
    """Initializes the Gemini client using the given API key."""
    try:
        return genai.Client(api_key=api_key)
    except Exception as e:
        st.error(f"Failed to initialize Gemini Client: {e}")
        return None

def initialize_chat_session(client):
    """Initializes a new chat session with the gemini-2.0-flash model."""
    try:
        return client.chats.create(model="gemini-2.0-flash")
    except Exception as e:
        st.error(f"Failed to create chat session: {e}")
        return None

def generate_text_stream(chat_session, prompt):
    """Generates text from the prompt, yielding chunks of the stream."""
    try:
        response = chat_session.send_message_stream(prompt)
        for chunk in response:
            yield chunk.text
    except Exception as e:
        yield f"\n\n**Ошибка при генерации текста:** {e}"
