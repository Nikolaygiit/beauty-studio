from google import genai
from google.genai import types

def init_gemini(api_key: str):
    """
    Initializes the Gemini client with the given API key.
    Sets system instructions to respond in Russian.
    """
    client = genai.Client(api_key=api_key)
    chat_session = client.chats.create(
        model="gemini-2.0-flash",
        config=types.GenerateContentConfig(
            system_instruction="Всегда отвечай на русском языке.",
            temperature=0.7,
        )
    )
    return client, chat_session

def generate_text_stream(chat_session, prompt: str):
    """
    Generates a streaming text response from Gemini.
    """
    try:
        response_stream = chat_session.send_message_stream(prompt)
        for chunk in response_stream:
            if chunk.text:
                yield chunk.text
    except Exception as e:
        yield f"Ошибка при генерации текста: {str(e)}"
