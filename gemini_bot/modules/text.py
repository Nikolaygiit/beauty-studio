import streamlit as st
from google import genai

def get_gemini_client_and_chat(api_key: str):
    """
    Initializes the Gemini client and creates a chat session.

    Args:
        api_key: The Google API key.

    Returns:
        A tuple of (client, chat_session) or (None, None) if error.
    """
    try:
        client = genai.Client(api_key=api_key)
        chat = client.chats.create(model="gemini-2.0-flash")
        return client, chat
    except Exception as e:
        st.error(f"Ошибка инициализации Gemini: {str(e)}")
        return None, None

def generate_text_stream(chat_session, prompt: str):
    """
    Generates text using the Gemini chat session as a stream.

    Args:
        chat_session: The active Gemini chat session.
        prompt: The user prompt.

    Yields:
        Text chunks as they arrive.
    """
    try:
        response = chat_session.send_message_stream(prompt)
        for chunk in response:
            if chunk.text:
                yield chunk.text
    except Exception as e:
        yield f"\n\n**Ошибка при генерации текста:** {str(e)}"
