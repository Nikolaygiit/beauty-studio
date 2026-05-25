from google import genai
from google.genai import types
import streamlit as st

def init_gemini_client(api_key: str):
    """
    Initializes and returns the Gemini client and a new chat session.
    """
    try:
        client = genai.Client(api_key=api_key)
        config = types.GenerateContentConfig(
            system_instruction="Ты — дружелюбный и полезный ИИ-помощник. Всегда отвечай на русском языке."
        )
        chat = client.chats.create(model="gemini-2.0-flash", config=config)
        return client, chat
    except Exception as e:
        st.error(f"Ошибка инициализации Gemini: {str(e)}")
        return None, None
