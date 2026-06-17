from google import genai
from google.genai import types
import streamlit as st

def get_gemini_client(api_key: str):
    if not api_key:
        return None, "API key is required"
    try:
        client = genai.Client(api_key=api_key)
        # Create a chat session with Russian language instructions
        config = types.GenerateContentConfig(
            system_instruction="Ты — полезный ИИ-ассистент. Всегда отвечай на русском языке.",
            temperature=0.7,
        )
        chat = client.chats.create(model="gemini-2.0-flash", config=config)
        return client, chat
    except Exception as e:
        return None, f"Failed to initialize Gemini client: {str(e)}"
