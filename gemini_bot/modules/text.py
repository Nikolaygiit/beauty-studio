from google import genai
from google.genai import types
import streamlit as st

def get_chat_session(api_key):
    """
    Initializes a Gemini client and returns a chat session object.
    """
    try:
        client = genai.Client(api_key=api_key)
        chat = client.chats.create(model="gemini-2.0-flash")
        return client, chat
    except Exception as e:
        st.error(f"Ошибка при инициализации Gemini: {e}")
        return None, None

def generate_text_stream(chat, prompt):
    """
    Sends a message to the chat session and yields the text chunks as they arrive.
    Catches errors like blocked content or connection issues.
    """
    try:
        response = chat.send_message_stream(prompt)
        for chunk in response:
            if chunk.text:
                yield chunk.text
    except Exception as e:
        yield f"\n\n[Ошибка генерации текста: {e}]"