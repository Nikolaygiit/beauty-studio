import streamlit as st
from gradio_client import Client

@st.cache_resource
def get_music_client():
    try:
        return Client("sanchit-gandhi/musicgen-streaming")
    except Exception as e:
        return f"Error loading model: {str(e)}"

def generate_music(prompt: str):
    """
    Generate music using Gradio client for musicgen-streaming.
    """
    client_or_err = get_music_client()

    if isinstance(client_or_err, str):
        return None, client_or_err

    try:
        result = client_or_err.predict(
            text_prompt=prompt,
            audio_length_in_s=15,
            play_steps_in_s=1.5,
            seed=0,
            api_name="/generate_audio"
        )
        return result, None
    except Exception as e:
        return None, f"Ошибка при генерации музыки: {str(e)}"
