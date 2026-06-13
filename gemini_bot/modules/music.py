import streamlit as st
from gradio_client import Client

@st.cache_resource
def get_music_client():
    """
    Returns a cached instance of the Gradio Client for music generation.
    """
    try:
        return Client("sanchit-gandhi/musicgen-streaming")
    except Exception as e:
        return f"Ошибка инициализации музыкального клиента: {str(e)}"

def generate_music(prompt: str) -> tuple[str | None, str | None]:
    """
    Generates music using the sanchit-gandhi/musicgen-streaming Gradio space.
    Passes named arguments: text_prompt, audio_length_in_s=15, play_steps_in_s=1.5, seed=0.
    Returns: (music_file_path, error_message)
    """
    client = get_music_client()
    if isinstance(client, str):
        return None, client

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
        return None, f"Ошибка генерации музыки: {str(e)}"
