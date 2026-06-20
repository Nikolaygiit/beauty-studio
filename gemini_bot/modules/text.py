from google import genai
from google.genai import types

def create_client_and_chat(api_key: str):
    """
    Initializes the Gemini client and creates a new chat session.
    """
    try:
        client = genai.Client(api_key=api_key)
        chat = client.chats.create(
            model="gemini-2.0-flash",
            config=types.GenerateContentConfig(
                system_instruction="Ты — умный и полезный ассистент. Всегда отвечай на русском языке."
            )
        )
        return client, chat
    except Exception as e:
        return None, None

def generate_text_stream(chat_session, prompt: str):
    """
    Generates a streaming text response from the Gemini chat session.
    Yields text chunks or error messages.
    """
    try:
        response_stream = chat_session.send_message_stream(prompt)
        for chunk in response_stream:
            if chunk.text:
                yield chunk.text
    except Exception as e:
        yield f"Произошла ошибка при генерации текста: {str(e)}"
