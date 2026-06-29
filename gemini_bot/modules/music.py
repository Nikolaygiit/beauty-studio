import streamlit as st
from gradio_client import Client
from typing import Tuple, Any

@st.cache_resource
def get_music_client() -> Tuple[Any, str]:
    """
    Initializes and caches the Gradio client for MusicGen.
    Returns (client, error_message).
    """
    try:
        client = Client("sanchit-gandhi/musicgen-streaming")
        return client, ""
    except Exception as e:
        return None, f"Ошибка подключения к сервису генерации музыки: {str(e)}"

def generate_music(prompt: str) -> Tuple[str, str]:
    """
    Generates music using the MusicGen Gradio space.
    Returns (media_path, error_message).
    """
    client, error = get_music_client()
    if not client:
        return "", error

    try:
        result = client.predict(
            text_prompt=prompt,
            audio_length_in_s=15,
            play_steps_in_s=1.5,
            seed=0,
            api_name="/generate_audio"
        )
        return result, ""
    except Exception as e:
        return "", f"Ошибка при генерации музыки: {str(e)}"
