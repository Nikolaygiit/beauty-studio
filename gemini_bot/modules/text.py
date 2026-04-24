import streamlit as st
from google import genai

def init_client(api_key):
    if not api_key:
        return None
    try:
        return genai.Client(api_key=api_key)
    except Exception as e:
        return None

def generate_text_stream(client, chat_session, prompt):
    try:
        response = chat_session.send_message_stream(prompt)
        for chunk in response:
            yield chunk.text
    except Exception as e:
        yield f"Error: {str(e)}"
