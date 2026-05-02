from gradio_client import Client
import streamlit as st

@st.cache_resource
def get_music_client():
    """Caches the Gradio Client initialization to prevent doing it repeatedly."""
    try:
        return Client("sanchit-gandhi/musicgen-streaming")
    except Exception as e:
        return str(e)

def generate_music(prompt: str) -> tuple[str, str]:
    """
    Generates music using the sanchit-gandhi/musicgen-streaming space.
    Returns a tuple of (audio_file_path, error_message).
    """
    client = get_music_client()

    if isinstance(client, str):
         return None, f"Ошибка инициализации MusicGen: {client}"

    try:
        # Based on typical usage for this model:
        # predict uses named parameters text_prompt, audio_length_in_s, play_steps_in_s, seed
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
