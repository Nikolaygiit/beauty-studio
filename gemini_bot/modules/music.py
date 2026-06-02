import streamlit as st
from gradio_client import Client

@st.cache_resource
def get_music_client():
    """Initializes and caches the MusicGen Gradio client."""
    try:
        return Client("sanchit-gandhi/musicgen-streaming")
    except Exception as e:
        return None

def generate_music(prompt: str) -> tuple[str | None, str | None]:
    """
    Generates music based on the prompt using the cached Gradio client.
    Returns (media_path, None) on success, or (None, error_message) on failure.
    """
    client = get_music_client()
    if client is None:
        return None, "Не удалось инициализировать клиент для генерации музыки."

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
