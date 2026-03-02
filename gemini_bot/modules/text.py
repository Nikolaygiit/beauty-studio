import streamlit as st
import google.generativeai as genai
import traceback

def get_gemini_model():
    """Initializes and returns the Gemini model."""
    return genai.GenerativeModel("gemini-1.5-flash")

def get_chat_session(model):
    """Initializes or retrieves the chat session from Streamlit state."""
    if st.session_state.get("gemini_chat_session") is None:
        st.session_state.gemini_chat_session = model.start_chat(history=[])
    return st.session_state.gemini_chat_session

def generate_text_response(prompt):
    """Generates a text response using the Gemini chat session and streams it."""
    model = get_gemini_model()
    chat_session = get_chat_session(model)

    try:
        response = chat_session.send_message(prompt, stream=True)
        for chunk in response:
            if chunk.text:
                yield chunk.text
    except Exception as e:
        error_msg = f"An error occurred during text generation. Details: {str(e)}\n\n"
        error_msg += "This might be due to safety filters or an API issue."
        yield error_msg
        print(f"Gemini API Error: {traceback.format_exc()}")
