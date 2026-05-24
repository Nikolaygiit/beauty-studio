import logging
from google import genai
from google.genai import types

logger = logging.getLogger(__name__)

def init_gemini_client_and_session(api_key: str):
    """
    Initializes and returns the Gemini client and a chat session.
    """
    try:
        client = genai.Client(api_key=api_key)
        config = types.GenerateContentConfig(
            system_instruction="Всегда отвечай на русском языке.",
        )
        chat_session = client.chats.create(
            model="gemini-2.0-flash",
            config=config
        )
        return client, chat_session
    except Exception as e:
        logger.error(f"Failed to initialize Gemini client: {e}")
        return None, None

def generate_text_stream(chat_session, prompt: str):
    """
    Generates a text response stream given a prompt and chat_session.
    """
    try:
        response = chat_session.send_message_stream(prompt)
        for chunk in response:
            if chunk.text:
                yield chunk.text
    except Exception as e:
        error_msg = f"\n\n[Ошибка при генерации текста: {str(e)}]"
        logger.error(error_msg)
        yield error_msg
