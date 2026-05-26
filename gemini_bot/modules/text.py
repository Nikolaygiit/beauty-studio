from google import genai
from google.genai import types
import streamlit as st

def get_gemini_client(api_key):
    """
    Initializes and returns the google-genai client.
    """
    try:
        client = genai.Client(api_key=api_key)
        return client, None
    except Exception as e:
        return None, f"Ошибка инициализации Gemini клиента: {str(e)}"

def initialize_chat(client):
    """
    Initializes a chat session with the gemini-2.0-flash model
    and system instructions to respond in Russian.
    """
    try:
        config = types.GenerateContentConfig(
            system_instruction="Ты — умный помощник. Всегда отвечай на русском языке."
        )
        chat = client.chats.create(model="gemini-2.0-flash", config=config)
        return chat, None
    except Exception as e:
        return None, f"Ошибка создания чата: {str(e)}"

def send_message_stream(chat, prompt):
    """
    Sends a message to the chat session and returns a stream.
    """
    try:
        response = chat.send_message_stream(prompt)
        return response, None
    except Exception as e:
        return None, f"Ошибка отправки сообщения: {str(e)}"
