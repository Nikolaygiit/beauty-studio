import streamlit as st
from google import genai
from google.genai import types

def get_gemini_client(api_key: str):
    """
    Initializes and returns the Gemini client and a chat session.
    It caches the client and chat session in the st.session_state.
    If the API key changes, it re-initializes the client.
    """
    if "current_api_key" not in st.session_state or st.session_state.current_api_key != api_key:
        client = genai.Client(api_key=api_key)
        st.session_state.gemini_client = client
        st.session_state.chat_session = client.chats.create(model="gemini-2.0-flash")
        st.session_state.current_api_key = api_key
    elif "gemini_client" not in st.session_state or "chat_session" not in st.session_state:
        client = genai.Client(api_key=api_key)
        st.session_state.gemini_client = client
        st.session_state.chat_session = client.chats.create(model="gemini-2.0-flash")
        st.session_state.current_api_key = api_key
    return st.session_state.chat_session

def generate_text_stream(prompt: str, api_key: str):
    """
    Yields chunks of text from the Gemini model.
    """
    chat_session = get_gemini_client(api_key)

    try:
        response = chat_session.send_message_stream(prompt)
        for chunk in response:
            yield chunk.text
    except Exception as e:
        yield f"\n\n**Error during text generation:** {str(e)}"
