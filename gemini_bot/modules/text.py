from google import genai
from google.genai import types

def get_gemini_client(api_key: str):
    """
    Initializes the Gemini client and creates a chat session.
    Returns (client, error_message). Memory dictates returning a tuple (client, error_message).
    We actually need to return (client, error_message) as per instructions.
    """
    try:
        client = genai.Client(api_key=api_key)
        return client, None
    except Exception as e:
        return None, f"Ошибка инициализации Gemini: {str(e)}"
