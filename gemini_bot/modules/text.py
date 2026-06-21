from google import genai
import streamlit as st

def get_gemini_client(api_key: str):
    """Returns a Gemini client initialized with the given API key."""
    return genai.Client(api_key=api_key)

def init_chat_session(client, history=None):
    """Initializes a chat session with system instructions."""
    config = genai.types.GenerateContentConfig(
        system_instruction="Ты — дружелюбный и полезный ассистент. Всегда отвечай на русском языке.",
    )
    if history is None:
        history = []

    return client.chats.create(model="gemini-2.0-flash", config=config)

def generate_text_stream(chat_session, prompt: str):
    """Yields text chunks from the Gemini API stream."""
    try:
        response = chat_session.send_message_stream(prompt)
        for chunk in response:
            if chunk.text:
                yield chunk.text
    except Exception as e:
        yield f"\n\n**Ошибка при генерации текста:** {str(e)}"
