import os
from google import genai
from google.genai import types

def get_chat_session(api_key):
    """Initializes and returns a chat session using Gemini 2.0 Flash."""
    try:
        client = genai.Client(api_key=api_key)
        # Using gemini-2.0-flash as it is the standard model for general text/chat tasks
        chat = client.chats.create(model="gemini-2.0-flash")
        return chat
    except Exception as e:
        return None

def generate_text(chat_session, prompt):
    """Generates text response from the chat session."""
    try:
        response = chat_session.send_message(prompt)
        return response.text
    except Exception as e:
        return f"Произошла ошибка при генерации текста: {e}"
