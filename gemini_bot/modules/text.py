import streamlit as st
from google import genai
from google.genai import types

def init_chat_session(api_key: str):
    """
    Initializes a chat session using the provided API key.
    Stores the client and the chat session in st.session_state.
    """
    try:
        client = genai.Client(api_key=api_key)

        # We define system instructions to always respond in Russian
        config = types.GenerateContentConfig(
            system_instruction="Always respond in Russian.",
        )

        # Create chat session using gemini-2.0-flash model
        chat = client.chats.create(
            model="gemini-2.0-flash",
            config=config
        )

        st.session_state.gemini_client = client
        st.session_state.chat_session = chat
        st.session_state.current_api_key = api_key
        return chat
    except Exception as e:
        return None, str(e)

def generate_text_stream(prompt: str, chat_session):
    """
    Generates text by streaming it from the Gemini chat session.
    Yields chunks of text.
    """
    try:
        response = chat_session.send_message_stream(prompt)
        for chunk in response:
            if chunk.text:
                yield chunk.text
    except Exception as e:
        yield f"Error generating text: {str(e)}"
