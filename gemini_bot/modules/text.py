from google import genai
from google.genai import types

def get_gemini_client(api_key: str) -> tuple[genai.Client | None, str | None]:
    """
    Initializes the Gemini client.
    Returns (client, None) on success, or (None, error_message) on failure.
    """
    try:
        client = genai.Client(api_key=api_key)
        return client, None
    except Exception as e:
        return None, f"Ошибка авторизации Gemini API: {str(e)}"

def init_chat_session(client: genai.Client):
    """
    Initializes a new chat session with Russian system instructions.
    Returns the chat session object, or None if error occurs.
    """
    try:
        config = types.GenerateContentConfig(
            system_instruction="Ты — полезный ИИ-ассистент. Отвечай всегда на русском языке."
        )
        return client.chats.create(
            model="gemini-2.0-flash",
            config=config
        )
    except Exception as e:
        # Expected error handling would be implemented at the caller level
        return None

def stream_text(chat_session, prompt: str):
    """
    Streams the text response from the Gemini API.
    Yields chunks of text or error messages.
    """
    try:
        response_stream = chat_session.send_message_stream(prompt)
        for chunk in response_stream:
            if chunk.text:
                yield chunk.text
    except Exception as e:
        yield f"\n[Ошибка при генерации текста: {str(e)}]"
