from gradio_client import Client
import streamlit as st

@st.cache_resource
def get_music_client():
    """Initializes and caches the Gradio client for music generation."""
    try:
        return Client("sanchit-gandhi/musicgen-streaming")
    except Exception as e:
        return f"Ошибка инициализации музыкального генератора: {e}"

def generate_music(prompt: str) -> tuple[str | None, str | None]:
    """
    Generates music using the Gradio Space 'sanchit-gandhi/musicgen-streaming'.
    Returns (path_to_audio, error_message).
    """
    client = get_music_client()

    if isinstance(client, str):
        # Client initialization failed and returned an error string
        return None, client

    try:
        result = client.predict(
            text_prompt=prompt,
            audio_length_in_s=15,
            play_steps_in_s=1.5,
            seed=0,
            api_name="/generate_audio"
        )
        # result is typically a tuple or path to the audio file
        audio_path = result[0] if isinstance(result, (list, tuple)) else result
        return audio_path, None
    except Exception as e:
        return None, f"Ошибка при генерации музыки: {e}"
