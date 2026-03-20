import streamlit as st
from google import genai

def get_chat_session(api_key: str):
    try:
        client = genai.Client(api_key=api_key)
        # Using gemini-2.0-flash model as instructed
        return client.chats.create(model="gemini-2.0-flash")
    except Exception as e:
        st.error(f"Error initializing chat session: {e}")
        return None

def stream_text_response(chat_session, prompt: str):
    try:
        response_stream = chat_session.send_message_stream(prompt)
        for chunk in response_stream:
            yield chunk.text
    except Exception as e:
        yield f"\n\n[Error generating response: {e}]"
