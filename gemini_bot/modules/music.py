import streamlit as st
from gradio_client import Client
from typing import Tuple, Optional

@st.cache_resource
def get_music_client() -> Optional[Client]:
    """
    Initializes and caches the Gradio client for music generation.
    """
    try:
        return Client("sanchit-gandhi/musicgen-streaming")
    except Exception as e:
        return None

def generate_music(prompt: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Generates music using the sanchit-gandhi/musicgen-streaming space.
    Returns a tuple of (file_path, error_message).
    """
    client = get_music_client()
    if client is None:
        return None, "Ошибка инициализации клиента для генерации музыки."

    try:
        result = client.predict(
            text_prompt=prompt,
            audio_length_in_s=15,
            play_steps_in_s=1.5,
            seed=0,
            api_name="/generate_audio"
        )
        # The result typically contains a path or a tuple containing the path
        if isinstance(result, tuple) and len(result) > 0:
            return result[0], None
        return result, None
    except Exception as e:
        return None, f"Ошибка при генерации музыки: {str(e)}"
