from google import genai
from google.genai import types
from typing import Tuple, Any, Optional

def get_gemini_client(api_key: str) -> Tuple[Optional[genai.Client], Optional[str]]:
    """
    Initializes the Gemini client.
    Returns (client, error_message).
    """
    if not api_key:
        return None, "API-ключ не предоставлен."

    try:
        client = genai.Client(api_key=api_key)
        return client, None
    except Exception as e:
        return None, f"Ошибка инициализации Gemini: {e}"

def get_chat_session(client: genai.Client) -> Any:
    """
    Creates and returns a new chat session with the instruction to respond in Russian.
    """
    config = types.GenerateContentConfig(
        system_instruction="Всегда отвечай на русском языке.",
    )
    return client.chats.create(model="gemini-2.0-flash", config=config)
