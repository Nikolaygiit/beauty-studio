import streamlit as st
from gradio_client import Client

@st.cache_resource(show_spinner=False)
def get_music_client():
    """Initializes and caches the Gradio client for music generation."""
    try:
        return Client("sanchit-gandhi/musicgen-streaming")
    except Exception as e:
        return str(e)

def generate_music(prompt):
    """
    Generates music based on a text prompt using musicgen-streaming.
    """
    client = get_music_client()
    if isinstance(client, str):
        return None, f"Ошибка подключения к сервису музыки: {client}"

    try:
        # The endpoint structure for sanchit-gandhi/musicgen-streaming
        # is typically /generate_audio or similar
        # Based on memory, use '/generate_audio'
        result = client.predict(
            prompt,	# str in 'Describe your music' Textbox component
            api_name="/generate_audio"
        )
        return result, None
    except Exception as e:
        return None, f"Ошибка генерации музыки: {str(e)}"
