import streamlit as st
from google import genai
from google.genai import types

def init_chat_session(api_key: str):
    """
    Initializes and returns the Gemini client and a new chat session.
    """
    client = genai.Client(api_key=api_key)
    chat = client.chats.create(
        model="gemini-2.0-flash",
        config=types.GenerateContentConfig(
            system_instruction="Ты — полезный ИИ-ассистент. Всегда отвечай на русском языке.",
            temperature=0.7
        )
    )
    return client, chat
