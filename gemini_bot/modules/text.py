import streamlit as st
from google import genai
from google.genai import types

def get_text_client(api_key):
    try:
        return genai.Client(api_key=api_key)
    except Exception as e:
        st.error(f"Error initializing text client: {e}")
        return None

def initialize_chat(client):
    try:
        return client.chats.create(model="gemini-2.5-flash")
    except Exception as e:
        st.error(f"Error initializing chat: {e}")
        return None

def generate_text_stream(chat_session, prompt):
    try:
        response = chat_session.send_message_stream(prompt)
        for chunk in response:
            yield chunk.text
    except Exception as e:
        yield f"\n\nОшибка: {e}"
