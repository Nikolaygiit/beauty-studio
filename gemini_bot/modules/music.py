import streamlit as st
from gradio_client import Client

@st.cache_resource
def get_music_client():
    try:
        return Client("sanchit-gandhi/musicgen-streaming")
    except Exception as e:
        return f"Ошибка инициализации Musicgen: {str(e)}"

def generate_music(prompt: str) -> tuple[str, str]:
    """
    Generates music using Gradio client.
    Returns (path_to_audio_file, error_message).
    """
    client_or_error = get_music_client()
    if isinstance(client_or_error, str):
        return None, client_or_error

    try:
        result = client_or_error.predict(
            text_prompt=prompt,
            audio_length_in_s=15,
            play_steps_in_s=1.5,
            seed=0,
            api_name="/generate_audio"
        )
        # result is typically a path to the downloaded audio file
        return result, None
    except Exception as e:
        return None, f"Ошибка при генерации музыки: {str(e)}"
