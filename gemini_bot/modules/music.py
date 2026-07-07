import streamlit as st
from gradio_client import Client
from typing import Tuple, Optional

@st.cache_resource
def get_music_client() -> Tuple[Optional[Client], Optional[str]]:
    """
    Initializes and caches the Gradio client for music generation.
    Returns (client, error_message).
    """
    try:
        client = Client("sanchit-gandhi/musicgen-streaming")
        return client, None
    except Exception as e:
        return None, f"Ошибка инициализации музыкального клиента: {str(e)}"

def generate_music(prompt: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Generates music based on the prompt using the cached Gradio client.
    Returns (media_path, error_message).
    """
    client, error = get_music_client()
    if error:
        return None, error

    try:
        result = client.predict(
            text_prompt=prompt,
            audio_length_in_s=15,
            play_steps_in_s=1.5,
            seed=0,
            api_name="/generate_audio"
        )
        # `result` is expected to be a tuple where the first element is the path to the audio file
        if isinstance(result, tuple) and len(result) > 0:
            return result[0], None
        return result, None # Sometimes it might just be the string path directly
    except Exception as e:
        return None, f"Ошибка генерации музыки: {str(e)}"
