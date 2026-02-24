import google.generativeai as genai
import streamlit as st

def configure_api(api_key):
    """Configures the Gemini API."""
    try:
        genai.configure(api_key=api_key)
        return True
    except Exception as e:
        st.error(f"Error configuring API: {e}")
        return False

def create_chat_session(model_name="gemini-1.5-flash", history=None):
    """Creates a chat session."""
    model = genai.GenerativeModel(model_name)
    chat = model.start_chat(history=history if history else [])
    return chat

def get_gemini_response(chat_session, prompt, image=None, stream=True):
    """
    Gets a response from the Gemini model.
    Handles both text-only and multimodal (text + image) inputs.
    """
    try:
        if image:
            # Multimodal input
            response = chat_session.send_message([prompt, image], stream=stream)
        else:
            # Text-only input
            response = chat_session.send_message(prompt, stream=stream)
        return response
    except Exception as e:
        return f"Error generating response: {str(e)}"
