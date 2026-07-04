import streamlit as st
from gradio_client import Client
from typing import Tuple, Optional, Any

@st.cache_resource
def get_music_client() -> Tuple[Optional[Any], Optional[str]]:
    """
    Initializes and caches the Gradio client for music generation.
    Returns a tuple of (client, error_message).
    """
    try:
        client = Client("sanchit-gandhi/musicgen-streaming")
        return client, None
    except Exception as e:
        return None, f"Ошибка при инициализации музыкального клиента: {str(e)}"

def generate_music(prompt: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Generates music using the Gradio music client based on the prompt.
    Returns a tuple of (audio_path, error_message).
    """
    client, error = get_music_client()
    if error:
        return None, error

    try:
        # Pass named arguments as specified in memory
        result = client.predict(
            text_prompt=prompt,
            audio_length_in_s=15,
            play_steps_in_s=1.5,
            seed=0,
            api_name="/generate_audio"
        )
        # result is typically a tuple where the first element is the path to the generated audio file
        if isinstance(result, tuple) and len(result) > 0:
            audio_path = result[0]
            return audio_path, None
        elif isinstance(result, str):
             # sometimes it might return just the path
             return result, None
        else:
             return None, f"Неожиданный формат ответа от музыкального клиента: {type(result)}"

    except Exception as e:
        return None, f"Ошибка при генерации музыки: {str(e)}"
