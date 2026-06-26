import streamlit as st
from gradio_client import Client

@st.cache_resource
def get_music_client():
    """
    Initializes and caches the Gradio client for music generation.
    Returns (client, error_message).
    """
    try:
        client = Client("sanchit-gandhi/musicgen-streaming")
        return client, None
    except Exception as e:
        return None, f"Ошибка инициализации сервиса музыки: {str(e)}"

def generate_music(prompt: str, client: Client):
    """
    Generates music using the sanchit-gandhi/musicgen-streaming Space.
    Returns (audio_path, error_message).
    """
    if not client:
        return None, "Клиент музыки не инициализирован."

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
