import streamlit as st
from google import genai
from typing import Tuple, Optional, Any

def get_gemini_client(api_key: str) -> Tuple[Optional[genai.Client], Optional[str]]:
    """
    Initializes the Gemini client.
    Returns a tuple of (client, error_message).
    """
    if not api_key:
         return None, "Пожалуйста, введите API ключ в боковой панели."
    try:
        client = genai.Client(api_key=api_key)
        return client, None
    except Exception as e:
        return None, f"Ошибка при инициализации Gemini клиента: {str(e)}"

def get_chat_session(client: genai.Client) -> Tuple[Optional[Any], Optional[str]]:
    """
    Creates a new chat session with the specified system instructions.
    Returns a tuple of (chat_session, error_message).
    """
    try:
        chat = client.chats.create(
            model="gemini-2.0-flash",
            config=genai.types.GenerateContentConfig(
                system_instruction="Всегда отвечай на русском языке."
            )
        )
        return chat, None
    except Exception as e:
        return None, f"Ошибка при создании сессии: {str(e)}"

def generate_text_stream(chat_session: Any, prompt: str):
    """
    Generates a streaming text response from the Gemini chat session.
    Yields chunks of text or an error message dict.
    """
    try:
        response_stream = chat_session.send_message_stream(prompt)
        for chunk in response_stream:
             yield chunk
    except Exception as e:
         yield {"error": f"Ошибка генерации текста: {str(e)}"}
