from typing import Tuple, Optional
from google import genai
from google.genai import types

def get_gemini_client(api_key: str) -> Tuple[Optional[genai.Client], Optional[str]]:
    """
    Initializes and returns the Gemini client using google-genai.
    Returns a tuple of (client, error_message).
    """
    if not api_key:
        return None, "API-ключ не предоставлен."

    try:
        client = genai.Client(api_key=api_key)
        return client, None
    except Exception as e:
        return None, f"Ошибка инициализации Gemini клиента: {str(e)}"

def get_chat_config() -> types.GenerateContentConfig:
    """
    Returns the configuration for the Gemini 2.0 Flash model,
    setting system instructions to always respond in Russian.
    """
    return types.GenerateContentConfig(
        system_instruction="Ты — полезный ИИ-ассистент, лучший бот на базе Gemini. Всегда отвечай на русском языке.",
    )
