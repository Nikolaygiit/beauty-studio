import streamlit as st
from gradio_client import Client

@st.cache_resource(show_spinner=False)
def get_music_client():
    """Caches and returns the Gradio client for music generation."""
    try:
        return Client("sanchit-gandhi/musicgen-streaming")
    except Exception as e:
        return f"Ошибка инициализации музыкального клиента: {e}"

def generate_music(prompt):
    """
    Generates music using the sanchit-gandhi/musicgen-streaming space.
    """
    client = get_music_client()
    if isinstance(client, str):
        return None, client # Return error message

    try:
        # Based on memory, use /generate_audio API endpoint
        result = client.predict(
            prompt,
            api_name="/generate_audio"
        )
        return result, None
    except Exception as e:
        return None, f"Ошибка генерации музыки: {e}"
