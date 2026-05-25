import streamlit as st
from gradio_client import Client

@st.cache_resource
def get_music_client():
    """
    Returns a cached Gradio client for music generation.
    """
    try:
        return Client("sanchit-gandhi/musicgen-streaming")
    except Exception as e:
        return f"Error initializing music client: {str(e)}"

def generate_music(prompt: str) -> tuple[str | None, str | None]:
    """
    Generates music using the Gradio API.
    Returns a tuple (audio_path, error_message).
    """
    client = get_music_client()
    if isinstance(client, str):
        return None, client

    try:
        result = client.predict(
            text_prompt=prompt,
            audio_length_in_s=15,
            play_steps_in_s=1.5,
            seed=0,
            api_name="/generate_audio"
        )
        return result, None
    except Exception as e:
        return None, f"Ошибка генерации музыки: {str(e)}"
