import streamlit as st
from google import genai

def init_chat_session(api_key):
    try:
        client = genai.Client(api_key=api_key)
        # Using gemini-2.0-flash as specified in memory
        chat = client.chats.create(model="gemini-2.0-flash")
        return client, chat
    except Exception as e:
        st.error(f"Failed to initialize Gemini client: {e}")
        return None, None

def generate_text_stream(chat, prompt):
    try:
        response = chat.send_message_stream(prompt)
        for chunk in response:
            if chunk.text:
                yield chunk.text
    except Exception as e:
        yield f"Произошла ошибка при генерации ответа: {e}"