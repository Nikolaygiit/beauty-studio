from google import genai
from google.genai import types

def get_gemini_client(api_key: str):
    """
    Initializes the Gemini client and chat session.
    Returns (client, error_message).
    """
    if not api_key:
        return None, "Пожалуйста, введите API ключ в боковой панели."

    try:
        client = genai.Client(api_key=api_key)

        # Test the connection or just return the client
        return client, None
    except Exception as e:
        return None, f"Ошибка инициализации Gemini: {str(e)}"

def start_chat_session(client):
    """
    Starts a new chat session with system instructions.
    Returns (chat_session, error_message).
    """
    if not client:
        return None, "Клиент Gemini не инициализирован."

    try:
        config = types.GenerateContentConfig(
            system_instruction="Ты — полезный ассистент Gemini Ultimate Bot. Всегда отвечай на русском языке.",
        )
        chat = client.chats.create(model="gemini-2.0-flash", config=config)
        return chat, None
    except Exception as e:
        return None, f"Ошибка создания чата: {str(e)}"
