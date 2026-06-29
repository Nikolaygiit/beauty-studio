import os
from typing import Tuple, Any
from google import genai
from google.genai import types

def get_gemini_client(api_key: str) -> Tuple[Any, str]:
    """
    Initializes the Gemini client and starts a chat session.
    Returns a tuple of (chat_session, error_message).
    """
    try:
        client = genai.Client(api_key=api_key)

        # Configure system instructions to always respond in Russian
        config = types.GenerateContentConfig(
            system_instruction="Всегда отвечай на русском языке.",
        )

        # We start a chat session with the configuration
        chat = client.chats.create(model="gemini-2.0-flash", config=config)
        return chat, ""
    except Exception as e:
        return None, f"Ошибка инициализации Gemini: {str(e)}"
