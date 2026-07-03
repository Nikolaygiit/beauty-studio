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
    Generates music based on the given prompt.
    Returns (audio_path, error_message).
    """
    client, err = get_music_client()
    if err:
        return None, err
    if not client:
        return None, "Музыкальный клиент не инициализирован."

    try:
        result = client.predict(
            text_prompt=prompt,
            audio_length_in_s=15,
            play_steps_in_s=1.5,
            seed=0,
            api_name="/generate_audio"
        )
        # The Gradio client returns a tuple for this endpoint, the first element is the path to the audio file
        if isinstance(result, tuple) and len(result) > 0:
            audio_path = result[0]
            return audio_path, None
        elif isinstance(result, str):
            return result, None
        else:
            return None, "Неизвестный формат ответа от музыкального клиента."
    except Exception as e:
        return None, f"Ошибка при генерации музыки: {str(e)}"
