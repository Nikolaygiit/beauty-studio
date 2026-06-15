import streamlit as st
from google import genai
from google.genai import types

def get_gemini_client(api_key: str):
    """
    Initializes and returns the Gemini client using the given API key.
    """
    return genai.Client(api_key=api_key)

def create_chat_session(client: genai.Client):
    """
    Creates a new chat session with the gemini-2.0-flash model,
    setting system instructions to respond in Russian.
    """
    return client.chats.create(
        model="gemini-2.0-flash",
        config=types.GenerateContentConfig(
            system_instruction="Всегда отвечай на русском языке.",
            temperature=0.7,
        )
    )

def generate_text_stream(chat_session, prompt: str):
    """
    Generates text from the chat session as a stream, yielding text chunks.
    Yields chunks of text and error message if any.
    Returns an iterator yielding (chunk_text, error).
    """
    try:
        response = chat_session.send_message_stream(prompt)
        for chunk in response:
            if chunk.text:
                yield chunk.text, None
    except Exception as e:
        yield None, f"Ошибка при генерации текста: {str(e)}"
