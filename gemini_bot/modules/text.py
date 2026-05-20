from google import genai
from google.genai import types

def get_gemini_client(api_key: str):
    """
    Initializes the Gemini client using the new google-genai package
    and creates a chat session with Russian system instructions.
    Returns (client, chat_session) or (None, None) if error.
    """
    try:
        client = genai.Client(api_key=api_key)

        # Configure model and system instructions
        config = types.GenerateContentConfig(
            system_instruction="Ты — полезный, умный и креативный ИИ-ассистент. Всегда отвечай только на русском языке. Твоя цель — помогать пользователю с любыми задачами: написанием текста, программированием, ответами на вопросы и генерацией идей."
        )

        chat_session = client.chats.create(
            model="gemini-2.0-flash",
            config=config
        )

        return client, chat_session
    except Exception as e:
        print(f"Error initializing Gemini client: {e}")
        return None, None
