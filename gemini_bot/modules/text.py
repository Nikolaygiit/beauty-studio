from google import genai
from google.genai import types

def create_chat_session(api_key: str):
    """
    Initializes a Gemini client and creates a chat session with Russian system instructions.
    Returns (client, chat_session)
    """
    client = genai.Client(api_key=api_key)

    config = types.GenerateContentConfig(
        system_instruction="Ты — полезный ИИ-помощник. Всегда отвечай на русском языке."
    )

    chat_session = client.chats.create(
        model='gemini-2.0-flash',
        config=config
    )
    return client, chat_session
