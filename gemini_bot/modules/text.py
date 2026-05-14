import streamlit as st
from google import genai
from google.genai import types

def init_gemini_client(api_key: str):
    """Initializes the Gemini client."""
    try:
        client = genai.Client(api_key=api_key)
        return client, None
    except Exception as e:
        return None, str(e)

def init_chat_session(client, history=None):
    """Initializes the chat session with the given client and history."""
    try:
        # Convert history to Gemini types if necessary, though genai can handle simple dicts.
        # Here we assume history is properly formatted or we just start fresh if None.
        chat = client.chats.create(
            model="gemini-2.0-flash",
        )
        return chat, None
    except Exception as e:
        return None, str(e)

def stream_gemini_response(chat_session, prompt: str):
    """Streams the response from Gemini for the given prompt."""
    try:
        response = chat_session.send_message_stream(prompt)
        for chunk in response:
            if chunk.text:
                yield chunk.text
    except Exception as e:
        yield f"\n[Ошибка при получении ответа от Gemini: {str(e)}]"
