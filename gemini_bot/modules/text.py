from google import genai
from google.genai import types

def create_chat_session(api_key: str):
    """
    Initializes and returns a Gemini client and chat session.
    Configured to use gemini-2.0-flash and respond in Russian.
    """
    client = genai.Client(api_key=api_key)
    chat_session = client.chats.create(
        model="gemini-2.0-flash",
        config=types.GenerateContentConfig(
            system_instruction="Всегда отвечай на русском языке."
        )
    )
    return client, chat_session

def generate_text_stream(chat_session, prompt: str):
    """
    Generates text by sending a message to the chat session.
    Yields chunks for streaming.
    """
    try:
        response = chat_session.send_message_stream(prompt)
        for chunk in response:
            if chunk.text:
                yield chunk.text
    except Exception as e:
        yield f"\n[Ошибка генерации текста: {str(e)}]"
