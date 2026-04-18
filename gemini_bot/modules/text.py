from google import genai
import streamlit as st

def initialize_chat(api_key: str):
    try:
        client = genai.Client(api_key=api_key)
        chat = client.chats.create(model="gemini-2.0-flash")
        return client, chat
    except Exception as e:
        return None, None

def generate_text_stream(prompt: str, chat):
    try:
        response = chat.send_message_stream(prompt)
        return response
    except Exception as e:
        return [f"Text generation error: {str(e)}"]
