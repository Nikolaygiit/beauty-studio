import streamlit as st
from google import genai

def generate_text(prompt, client):
    """Generates text using the Gemini 2.0 Flash model via Google GenAI SDK."""
    try:
        if 'chat_session' not in st.session_state:
            st.session_state.chat_session = client.chats.create(
                model="gemini-2.0-flash"
            )

        chat_session = st.session_state.chat_session
        response = chat_session.send_message_stream(prompt)

        for chunk in response:
            if chunk.text:
                yield chunk.text

    except Exception as e:
        yield f"\n\n**Ошибка при генерации текста:** {e}"
