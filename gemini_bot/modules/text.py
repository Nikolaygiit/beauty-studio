from google import genai
from google.genai import types

def get_gemini_client(api_key: str):
    """
    Initializes the Gemini client.
    Returns (client, error_message)
    """
    if not api_key:
        return None, "API Key is required to initialize the Gemini client."

    try:
        client = genai.Client(api_key=api_key)
        return client, None
    except Exception as e:
        return None, f"Failed to initialize Gemini client: {e}"

def get_chat_session(client):
    """
    Creates a new chat session with system instructions to always reply in Russian.
    """
    try:
        chat = client.chats.create(
            model="gemini-2.0-flash",
            config=types.GenerateContentConfig(
                system_instruction="Всегда отвечай на русском языке."
            )
        )
        return chat, None
    except Exception as e:
        return None, f"Failed to start chat session: {e}"
