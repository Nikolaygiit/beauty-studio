from google import genai
import streamlit as st

def get_client(api_key: str):
    return genai.Client(api_key=api_key)

def start_chat(client: genai.Client):
    return client.chats.create(model="gemini-2.0-flash")

def generate_text_stream(chat, prompt: str):
    try:
        response = chat.send_message_stream(prompt)
        for chunk in response:
            if chunk.text:
                yield chunk.text
    except Exception as e:
        yield f"Произошла ошибка при обращении к Gemini API: {str(e)}"
