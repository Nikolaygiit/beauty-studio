import streamlit as st
from gradio_client import Client
import time

@st.cache_resource(show_spinner=False)
def get_music_client():
    """Initializes and caches the music generation Gradio client."""
    try:
        return Client("sanchit-gandhi/musicgen-streaming")
    except Exception as e:
        return f"Ошибка подключения к сервису музыки: {e}"

def generate_music(prompt):
    """
    Generates music using the sanchit-gandhi/musicgen-streaming Gradio Space.
    """
    client = get_music_client()

    if isinstance(client, str):
        return client # Return error message

    try:
        # According to memory: /generate_audio endpoint, text_prompt, audio_length_in_s=15, play_steps_in_s=1.5, seed=0
        result = client.predict(
            text_prompt=prompt,
            audio_length_in_s=15,
            play_steps_in_s=1.5,
            seed=int(time.time()),
            api_name="/generate_audio"
        )
        return result
    except Exception as e:
        return f"Произошла ошибка при генерации музыки: {e}"
