import streamlit as st
from google import genai
from google.genai import types

def get_gemini_client(api_key: str):
    """
    Initializes the Gemini client.
    Returns (client, error_message).
    """
    try:
        if not api_key:
            return None, "Пожалуйста, введите API ключ в боковой панели."
        client = genai.Client(api_key=api_key)
        return client, None
    except Exception as e:
        return None, f"Ошибка при инициализации Gemini клиента: {str(e)}"

def initialize_chat(client):
    """
    Initializes a new chat session with system instructions in Russian.
    """
    return client.chats.create(
        model="gemini-2.0-flash",
        config=types.GenerateContentConfig(
            system_instruction="Ты — полезный ИИ-помощник. Всегда отвечай на русском языке.",
            temperature=0.7,
        )
    )

def generate_text_stream(chat_session, prompt: str):
    """
    Generates a streaming text response using the active chat session.
    Yields text chunks as they arrive.
    """
    try:
        response = chat_session.send_message_stream(prompt)
        for chunk in response:
            if chunk.text:
                yield chunk.text
    except Exception as e:
        yield f"\n\n**Ошибка при генерации текста:** {str(e)}"
