import streamlit as st
from gradio_client import Client

@st.cache_resource
def get_music_client():
    """
    Initializes and caches the MusicGen Gradio client.
    Returns (client, error_message).
    """
    try:
        client = Client("sanchit-gandhi/musicgen-streaming")
        return client, None
    except Exception as e:
        return None, f"Ошибка инициализации музыкального клиента: {str(e)}"

def generate_music(prompt: str):
    """
    Generates music using the MusicGen client.
    Returns (media_path, error_message).
    """
    client, error = get_music_client()
    if error:
        return None, error

    try:
        # Use named arguments for the prediction
        result = client.predict(
            text_prompt=prompt,
            audio_length_in_s=15,
            play_steps_in_s=1.5,
            seed=0,
            api_name="/generate_audio"
        )
        return result, None
    except Exception as e:
        return None, f"Ошибка при создании музыки: {str(e)}"
