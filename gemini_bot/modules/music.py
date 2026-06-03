import streamlit as st
from gradio_client import Client

@st.cache_resource
def get_music_client():
    """
    Initializes and caches the Gradio client for MusicGen.
    """
    try:
        return Client("sanchit-gandhi/musicgen-streaming")
    except Exception as e:
        return f"Ошибка инициализации MusicGen: {str(e)}"

def generate_music(prompt: str) -> tuple[str | None, str | None]:
    """
    Generates music using the sanchit-gandhi/musicgen-streaming Gradio Space.
    Returns (audio_path, error_message).
    """
    client = get_music_client()
    if isinstance(client, str): # Error message returned
        return None, client

    try:
        result = client.predict(
            text_prompt=prompt,
            audio_length_in_s=15,
            play_steps_in_s=1.5,
            seed=0,
            api_name="/generate_audio"
        )
        # The result is a tuple, we want the path (first element typically)
        if isinstance(result, tuple):
            audio_path = result[0]
        else:
            audio_path = result

        return audio_path, None
    except Exception as e:
        return None, f"Ошибка генерации музыки: {str(e)}"
