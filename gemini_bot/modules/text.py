from google import genai
import streamlit as st

def initialize_chat(api_key):
    """Initializes the Gemini client and creates a chat session."""
    client = genai.Client(api_key=api_key)
    chat = client.chats.create(model='gemini-2.0-flash')
    return client, chat

def stream_text_response(chat, prompt):
    """Streams the text response from Gemini and yields chunks, with error handling."""
    try:
        response = chat.send_message_stream(prompt)
        for chunk in response:
            if chunk.text:
                yield chunk.text
    except Exception as e:
        yield f"⚠️ Ошибка при генерации текста: {e}"
