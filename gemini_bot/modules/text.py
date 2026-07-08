from google import genai
from google.genai import types

def get_gemini_client(api_key: str):
    """
    Initializes and returns the Gemini client and an error message (if any).
    Uses the modern google-genai package.
    """
    if not api_key:
        return None, "API Key is required"

    try:
        client = genai.Client(api_key=api_key)

        # Test the connection/API key (optional but good practice)
        # However, to save time we will just create the chat session later
        return client, None
    except Exception as e:
        return None, str(e)

def init_chat_session(client):
    """
    Initializes a chat session with the specified system instructions.
    """
    try:
        chat = client.chats.create(
            model="gemini-2.0-flash",
            config=types.GenerateContentConfig(
                system_instruction="Всегда отвечай по-русски."
            )
        )
        return chat, None
    except Exception as e:
        return None, str(e)
