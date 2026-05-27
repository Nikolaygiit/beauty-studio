import streamlit as st
from gradio_client import Client

@st.cache_resource(show_spinner=False)
def get_music_client():
    """
    Initializes and caches the Gradio Client for music generation.
    Returns the client instance or raises an exception.
    """
    return Client("sanchit-gandhi/musicgen-streaming")

def generate_music(prompt: str) -> tuple[str, str]:
    """
    Generates music using the sanchit-gandhi/musicgen-streaming Gradio Space.
    Returns (audio_path, error_message).
    """
    try:
        client = get_music_client()
        result = client.predict(
            text_prompt=prompt,
            audio_length_in_s=15,
            play_steps_in_s=1.5,
            seed=0,
            api_name="/generate_audio"
        )
        return result, None
    except Exception as e:
        return None, f"Ошибка при генерации музыки: {e}"
