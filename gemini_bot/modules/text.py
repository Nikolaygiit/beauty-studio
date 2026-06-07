from google import genai
import streamlit as st

def get_client(api_key: str):
    """Initializes the Google GenAI client."""
    try:
        return genai.Client(api_key=api_key)
    except Exception as e:
        return None

def generate_text_stream(client, chat_session, prompt: str):
    """Generates text stream using the provided chat session."""
    try:
        response_stream = chat_session.send_message_stream(prompt)
        for chunk in response_stream:
            if chunk.text:
                yield chunk.text
    except Exception as e:
        yield f"\n\n**Ошибка при генерации текста:** {str(e)}"

def create_chat_session(client):
    """Creates a new chat session with system instructions."""
    system_instruction = "Ты — умный и полезный бот-ассистент. Всегда отвечай на русском языке."
    config = genai.types.GenerateContentConfig(
        system_instruction=system_instruction,
    )
    return client.chats.create(model="gemini-2.0-flash", config=config)
