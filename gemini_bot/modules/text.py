import streamlit as st
from google import genai
from google.genai import types

def get_gemini_client(api_key: str):
    """
    Initializes and returns the Gemini client and an error message (if any).
    """
    try:
        client = genai.Client(api_key=api_key)
        return client, None
    except Exception as e:
        return None, f"Ошибка инициализации Gemini: {str(e)}"

def get_chat_session(client, chat_history=None):
    """
    Initializes a chat session with system instructions.
    """
    if chat_history is None:
        chat_history = []

    config = types.GenerateContentConfig(
        system_instruction="Ты — полезный ИИ-помощник. Всегда отвечай на русском языке.",
    )

    # We create a new chat. We can pass history if supported, but here we just return the session
    chat_session = client.chats.create(
        model="gemini-2.0-flash",
        config=config
    )

    # If there's an existing history, we might need to manually set it up
    # In google-genai, you might need to handle history differently, but for now we create a fresh chat
    return chat_session
