from google import genai
from google.genai import types

def create_client(api_key: str):
    return genai.Client(api_key=api_key)

def create_chat_session(client):
    return client.chats.create(
        model="gemini-2.0-flash",
        config=types.GenerateContentConfig(
            system_instruction="Всегда отвечай на русском языке.",
        )
    )

def generate_text_stream(chat_session, prompt: str):
    """
    Yields chunks of generated text.
    Handles general exceptions during API calls.
    """
    try:
        response = chat_session.send_message_stream(prompt)
        for chunk in response:
            if chunk.text:
                yield chunk.text
    except Exception as e:
        yield f"\n\nПроизошла ошибка при генерации текста: {str(e)}"
