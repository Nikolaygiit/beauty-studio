import streamlit as st
from google import genai
from google.genai import types

def get_text_response(prompt, api_key):
    """
    Generate text response using Gemini API with conversational history.
    """
    try:
        if not api_key:
            return "Пожалуйста, введите ваш Google API Key в боковой панели."

        # Initialize the client with the provided API key
        client = genai.Client(api_key=api_key)

        # Initialize chat session in streamlit state if not exists
        if "chat_session" not in st.session_state or st.session_state.chat_session is None:
            # Create a new chat session using gemini-2.0-flash
            st.session_state.chat_session = client.chats.create(
                model="gemini-2.0-flash"
            )

        # Stream the response
        response = st.session_state.chat_session.send_message_stream(prompt)
        return response

    except Exception as e:
        return f"Произошла ошибка при обращении к Gemini API: {str(e)}"

def reset_chat_session():
    """
    Clear the chat session to start fresh.
    """
    st.session_state.chat_session = None
