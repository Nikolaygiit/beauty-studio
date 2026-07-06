import streamlit as st
from gradio_client import Client
from typing import Tuple, Optional

@st.cache_resource
def get_music_client() -> Client:
    """
    Initializes and caches the Gradio client for music generation.
    """
    return Client("sanchit-gandhi/musicgen-streaming")

def generate_music(prompt: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Generates music using the Gradio client.
    Returns (path_to_audio, error_message).
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
        # The result is typically a tuple from Gradio API, where the first element is the path
        if isinstance(result, tuple):
            return result[0], None
        return result, None
    except Exception as e:
        return None, f"Ошибка генерации музыки: {e}"
