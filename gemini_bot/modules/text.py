import streamlit as st
from google import genai
from google.genai import types

def get_gemini_client(api_key: str):
    """
    Initializes the Gemini client.
    """
    try:
        return genai.Client(api_key=api_key)
    except Exception as e:
        return str(e)

def init_chat_session(client):
    """
    Initializes a new chat session with system instructions to respond in Russian.
    """
    try:
        config = types.GenerateContentConfig(
            system_instruction="Всегда отвечай на русском языке. Будь полезным и вежливым ИИ-ассистентом."
        )
        return client.chats.create(model="gemini-2.0-flash", config=config)
    except Exception as e:
        return str(e)

def generate_text_stream(chat_session, prompt: str):
    """
    Generates text via streaming and yields the chunks.
    """
    try:
        response = chat_session.send_message_stream(prompt)
        for chunk in response:
            if chunk.text:
                yield chunk.text
    except Exception as e:
        yield f"\\n**Ошибка:** {str(e)}"
