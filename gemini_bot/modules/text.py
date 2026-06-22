from google import genai
from google.genai import types
import streamlit as st

def get_gemini_client(api_key: str):
    """Initializes and returns the Gemini client."""
    try:
        client = genai.Client(api_key=api_key)
        return client, None
    except Exception as e:
        return None, str(e)

def create_chat_session(client):
    """Creates a new chat session with the appropriate system instructions."""
    config = types.GenerateContentConfig(
        system_instruction="Всегда отвечай на русском языке.",
    )
    try:
        chat = client.chats.create(
            model="gemini-2.0-flash",
            config=config
        )
        return chat
    except Exception as e:
        return None
