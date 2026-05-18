import streamlit as st
from google import genai
from google.genai import types

def init_client(api_key: str):
    """Initializes the Gemini client."""
    try:
        client = genai.Client(api_key=api_key)
        return client, None
    except Exception as e:
        return None, str(e)

def init_chat_session(client):
    """Initializes the chat session with system instructions enforcing Russian."""
    try:
        session = client.chats.create(
            model="gemini-2.0-flash",
            config=types.GenerateContentConfig(
                system_instruction="Всегда отвечай только на русском языке. Твои ответы должны быть вежливыми и информативными."
            )
        )
        return session, None
    except Exception as e:
        return None, str(e)

def generate_text_stream(session, prompt: str):
    """Generates text in a streaming manner."""
    try:
        response_stream = session.send_message_stream(prompt)
        return response_stream, None
    except Exception as e:
        return None, str(e)
