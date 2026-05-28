import streamlit as st
from google import genai
from google.genai import types

def init_gemini_client(api_key: str):
    """Initializes the Gemini client."""
    try:
        client = genai.Client(api_key=api_key)
        return client, None
    except Exception as e:
        return None, f"Ошибка инициализации Gemini: {e}"

def start_chat_session(client):
    """Starts a new chat session with system instructions."""
    try:
        config = types.GenerateContentConfig(
            system_instruction="Ты — полезный и дружелюбный помощник. Всегда отвечай на русском языке.",
            temperature=0.7,
        )
        chat = client.chats.create(model="gemini-2.0-flash", config=config)
        return chat, None
    except Exception as e:
        return None, f"Ошибка создания чата: {e}"

def generate_text_stream(chat, prompt: str):
    """Generates a text response stream."""
    try:
        response = chat.send_message_stream(prompt)
        for chunk in response:
            if chunk.text:
                yield chunk.text
    except Exception as e:
        yield f"\\n\\n**Ошибка генерации текста:** {e}"
