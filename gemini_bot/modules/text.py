import streamlit as st
from google import genai

def get_gemini_client(api_key: str):
    """
    Initializes and returns a Gemini client.
    """
    try:
        return genai.Client(api_key=api_key)
    except Exception as e:
        st.error(f"Ошибка инициализации Gemini: {e}")
        return None

def init_chat_session(client):
    """
    Initializes a new chat session with system instructions.
    """
    try:
        config = genai.types.GenerateContentConfig(
            system_instruction="Ты — полезный ИИ-ассистент. Отвечай всегда на русском языке."
        )
        return client.chats.create(model="gemini-2.0-flash", config=config)
    except Exception as e:
        st.error(f"Ошибка создания сессии чата: {e}")
        return None

def generate_text_stream(chat_session, prompt: str):
    """
    Generates text using the Gemini chat session as a stream.
    """
    try:
        response = chat_session.send_message_stream(prompt)
        for chunk in response:
            if chunk.text:
                yield chunk.text
    except Exception as e:
        yield f"\n\n**Ошибка при генерации текста:** {str(e)}"
