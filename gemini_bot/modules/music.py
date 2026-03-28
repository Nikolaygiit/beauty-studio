import streamlit as st
from gradio_client import Client

@st.cache_resource
def get_music_client():
    """
    Initialize and cache the Gradio client for MusicGen.
    Uses @st.cache_resource to prevent re-initialization on Streamlit reruns.
    """
    try:
        return Client("sanchit-gandhi/musicgen-streaming")
    except Exception as e:
        return f"Ошибка при инициализации MusicGen клиента: {str(e)}"

def generate_music(prompt):
    """
    Generate music audio file using MusicGen streaming API.
    """
    client = get_music_client()

    if isinstance(client, str):
        # Client initialization failed and returned error string
        return client

    try:
        # Generate music using the gradio API endpoint
        result = client.predict(
            prompt,	# str in 'text' Textbox component
            api_name="/generate_audio"
        )
        return result
    except Exception as e:
        return f"Ошибка при генерации музыки: {str(e)}"
