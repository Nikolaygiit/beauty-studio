import os
from google import genai
from google.genai import types

def init_gemini_client(api_key):
    """
    Initializes and returns the Gemini client with the given API key.
    """
    if not api_key:
        return None, "API Key is missing."
    try:
        client = genai.Client(api_key=api_key)
        return client, None
    except Exception as e:
        return None, f"Failed to initialize Gemini client: {str(e)}"

def init_chat_session(client):
    """
    Initializes a new chat session using the gemini-2.0-flash model.
    """
    if not client:
        return None, "Gemini client is not initialized."
    try:
        chat = client.chats.create(model="gemini-2.0-flash")
        return chat, None
    except Exception as e:
        return None, f"Failed to create chat session: {str(e)}"
