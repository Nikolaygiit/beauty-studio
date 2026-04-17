from google import genai
import streamlit as st

def get_client(api_key):
    """Initializes and returns the Gemini client."""
    return genai.Client(api_key=api_key)

def init_chat(client):
    """Initializes the chat session."""
    try:
        return client.chats.create(model="gemini-2.0-flash")
    except Exception as e:
        return None

def generate_text_stream(chat_session, prompt):
    """Generates a text response stream using the chat session."""
    try:
        response = chat_session.send_message_stream(prompt)
        for chunk in response:
            if chunk.text:
                yield chunk.text
    except Exception as e:
        yield f"\n\nПроизошла ошибка при генерации ответа: {str(e)}"
