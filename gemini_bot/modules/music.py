import streamlit as st
from gradio_client import Client
import tempfile

@st.cache_resource
def get_music_client():
    try:
        return Client("sanchit-gandhi/musicgen-streaming")
    except Exception as e:
        return None

def generate_music(prompt):
    """
    Generates music using the sanchit-gandhi/musicgen-streaming Gradio Space.
    Returns (audio_path, None) on success, or (None, error_message) on failure.
    """
    client = get_music_client()
    if not client:
        return None, "Ошибка инициализации клиента для генерации музыки."

    try:
        result = client.predict(
            text_prompt=prompt,
            audio_length_in_s=15,
            play_steps_in_s=1.5,
            seed=0,
            api_name="/generate_audio"
        )
        # The result might be a tuple or a direct string path depending on the gradio endpoint output
        # Usually it returns a path to the generated audio file
        audio_path = result[0] if isinstance(result, tuple) else result
        return audio_path, None
    except Exception as e:
        return None, f"Ошибка при генерации музыки: {e}"