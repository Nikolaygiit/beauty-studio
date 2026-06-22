from gradio_client import Client
import streamlit as st

@st.cache_resource
def get_music_client():
    """Initializes and caches the Gradio client for music generation."""
    try:
        return Client("sanchit-gandhi/musicgen-streaming")
    except Exception as e:
        return None

def generate_music(prompt: str) -> tuple[str | None, str | None]:
    """
    Generates music using the sanchit-gandhi/musicgen-streaming Gradio client.
    Returns a tuple of (audio_path, error_message).
    """
    client = get_music_client()
    if not client:
        return None, "Ошибка инициализации клиента генерации музыки."

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
