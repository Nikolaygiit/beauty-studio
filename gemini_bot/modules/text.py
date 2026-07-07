from google import genai
from google.genai import types
from typing import Tuple, Optional, Any

def get_gemini_client(api_key: str) -> Tuple[Optional[genai.Client], Optional[str]]:
    """
    Initializes the Gemini client and starts a chat session.
    Returns (client, error_message).
    """
    if not api_key:
        return None, "Пожалуйста, введите API ключ."

    try:
        client = genai.Client(api_key=api_key)
        return client, None
    except Exception as e:
        return None, f"Ошибка инициализации Gemini: {str(e)}"

def create_chat_session(client: genai.Client) -> Tuple[Optional[Any], Optional[str]]:
    """
    Creates a new chat session with the appropriate system instructions.
    Returns (chat_session, error_message).
    """
    try:
        config = types.GenerateContentConfig(
            system_instruction="Ты — дружелюбный и невероятно умный ИИ-помощник. Твоя задача — помогать пользователю. Всегда отвечай на русском языке.",
        )
        chat = client.chats.create(model="gemini-2.0-flash", config=config)
        return chat, None
    except Exception as e:
        return None, f"Ошибка создания сессии чата: {str(e)}"
