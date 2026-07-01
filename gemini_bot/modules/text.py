from google import genai
from google.genai import types
from typing import Tuple, Any, Optional

def get_gemini_client(api_key: str) -> Tuple[Optional[genai.Client], Optional[str]]:
    """
    Initializes and returns the Gemini client.
    Returns:
        (client, error_message): A tuple containing the client object and an error message string.
    """
    try:
        if not api_key:
            return None, "Не указан API ключ."
        client = genai.Client(api_key=api_key)
        return client, None
    except Exception as e:
        return None, f"Ошибка при инициализации клиента: {str(e)}"

def init_chat_session(client: genai.Client) -> Tuple[Any, Optional[str]]:
    """
    Initializes a new chat session with the Gemini client, configuring system instructions.
    Returns:
        (chat_session, error_message)
    """
    try:
        config = types.GenerateContentConfig(
            system_instruction="Всегда отвечай на русском языке.",
            temperature=0.7
        )
        chat = client.chats.create(model="gemini-2.0-flash", config=config)
        return chat, None
    except Exception as e:
        return None, f"Ошибка при создании сессии чата: {str(e)}"

def generate_text_stream(chat_session: Any, prompt: str):
    """
    Generates a text stream from the chat session.
    Yields text chunks or error message chunks.
    """
    try:
        response = chat_session.send_message_stream(prompt)
        for chunk in response:
            if chunk.text:
                yield chunk.text
    except Exception as e:
        yield f"\\n**Произошла ошибка при генерации ответа:** {str(e)}"
