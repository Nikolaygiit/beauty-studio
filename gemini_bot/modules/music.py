import streamlit as st
from gradio_client import Client

@st.cache_resource(show_spinner="Инициализация модели музыки...")
def get_music_client():
    """
    Initializes and caches the Gradio client for music generation.
    """
    try:
        return Client("sanchit-gandhi/musicgen-streaming")
    except Exception as e:
        return str(e)

def generate_music(prompt: str) -> tuple[str | None, str | None]:
    """
    Generates music using the sanchit-gandhi/musicgen-streaming space.
    Returns (audio_path, error_message).
    """
    client = get_music_client()
    if isinstance(client, str):
        return None, f"Ошибка инициализации клиента: {client}"

    try:
        result = client.predict(
            text_prompt=prompt,
            audio_length_in_s=15,
            play_steps_in_s=1.5,
            seed=0,
            api_name="/generate_audio"
        )
        # The result from Gradio might be a path or tuple/list.
        # Typically for audio streams, it might return a path.
        if isinstance(result, tuple) or isinstance(result, list):
            return result[0], None
        return result, None
    except Exception as e:
        return None, f"Ошибка генерации музыки: {str(e)}"
