import streamlit as st
from gradio_client import Client

@st.cache_resource
def get_music_client():
    try:
        return Client("sanchit-gandhi/musicgen-streaming")
    except Exception as e:
        return str(e)

def generate_music(prompt: str) -> tuple[str | None, str | None]:
    """
    Generate music using sanchit-gandhi/musicgen-streaming space.
    Returns (audio_path, None) on success, or (None, error_message) on failure.
    """
    client = get_music_client()

    if isinstance(client, str):
        return None, f"Ошибка при подключении к сервису генерации музыки: {client}"

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
