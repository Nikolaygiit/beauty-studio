import streamlit as st
from google import genai

def get_chat_session(api_key):
    """
    Initializes and returns a Google GenAI chat session.
    It expects the API key to be passed.
    """
    client = genai.Client(api_key=api_key)
    # Using the gemini-2.0-flash model as requested
    chat = client.chats.create(model="gemini-2.0-flash")
    return chat

def stream_text_response(chat_session, prompt):
    """
    Sends a message to the chat session and yields the response in chunks.
    Handles potential exceptions during generation.
    """
    try:
        response = chat_session.send_message_stream(prompt)
        for chunk in response:
            yield chunk.text
    except Exception as e:
        yield f"\n\n[Ошибка при генерации текста: {e}]"
