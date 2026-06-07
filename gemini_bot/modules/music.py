from gradio_client import Client
import streamlit as st

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
        return None, f"Ошибка инициализации клиента для музыки: {str(e)}"

def generate_music(prompt: str):
    """
    Generates music based on the prompt using the cached client.
    Returns (audio_path, None) on success, or (None, error_message) on failure.
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
        # The result is a tuple, we usually want the file path.
        if isinstance(result, tuple) and len(result) > 0:
             return result[0], None
        return result, None
    except Exception as e:
        return None, f"Ошибка при генерации музыки: {str(e)}"
