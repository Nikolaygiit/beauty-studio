import streamlit as st
from gradio_client import Client

@st.cache_resource
def get_music_client():
    """
    Initializes and caches the Gradio client for music generation.
    Returns (client, None) on success, or (None, error_message) on failure.
    """
    try:
        client = Client("sanchit-gandhi/musicgen-streaming")
        return client, None
    except Exception as e:
        return None, f"Ошибка при подключении к сервису музыки: {str(e)}"

def generate_music(prompt: str) -> tuple[str | None, str | None]:
    """
    Generates music based on a prompt.
    Returns (path_to_audio, None) on success, or (None, error_message) on failure.
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
        return result, None
    except Exception as e:
        return None, f"Ошибка при генерации музыки: {str(e)}"
