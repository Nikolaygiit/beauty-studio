from google import genai
from google.genai import types

def get_text_client(api_key: str):
    """Initializes and returns the Gemini client for text generation."""
    return genai.Client(api_key=api_key)

def create_chat_session(client):
    """Creates a chat session with the instruction to always respond in Russian."""
    config = types.GenerateContentConfig(
        system_instruction="Ты — полезный AI ассистент. Всегда отвечай на русском языке.",
    )
    return client.chats.create(model='gemini-2.0-flash', config=config)

def generate_text_stream(chat_session, prompt: str):
    """Generates text from the prompt, yielding chunks of the response."""
    try:
        response = chat_session.send_message_stream(prompt)
        for chunk in response:
            if chunk.text:
                yield chunk.text
    except Exception as e:
        yield f"\n\nПроизошла ошибка при генерации текста: {e}"
