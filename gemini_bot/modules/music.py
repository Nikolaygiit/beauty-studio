import streamlit as st
from gradio_client import Client
from typing import Tuple, Optional, Any

@st.cache_resource
def get_music_client() -> Tuple[Optional[Client], Optional[str]]:
    """
    Initializes and caches the Gradio client for music generation.
    Returns (Client, error_message).
    """
    try:
        client = Client("sanchit-gandhi/musicgen-streaming")
        return client, None
    except Exception as e:
        return None, f"Ошибка подключения к сервису генерации музыки: {str(e)}"

def generate_music(client: Client, prompt: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Generates music using the specified text prompt.
    Returns (audio_path, error_message).
    """
    try:
        result = client.predict(
            text_prompt=prompt,
            audio_length_in_s=15,
            play_steps_in_s=1.5,
            seed=0,
            api_name="/generate_audio"
        )
        if isinstance(result, tuple) and len(result) > 0:
            return result[0], None
        return str(result), None
    except Exception as e:
        return None, f"Ошибка при генерации музыки: {str(e)}"
