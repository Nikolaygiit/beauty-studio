from google import genai
import streamlit as st

def generate_text(prompt, client, chat_session):
    try:
        response = chat_session.send_message_stream(prompt)
        return response
    except Exception as e:
        st.error(f"Error during text generation: {str(e)}")
        return None

def init_chat_session(client):
    try:
        chat = client.chats.create(
            model="gemini-2.0-flash",
            config={
                "system_instruction": "You are a helpful assistant. Always respond in Russian."
            }
        )
        return chat
    except Exception as e:
        st.error(f"Error initializing chat session: {str(e)}")
        return None
