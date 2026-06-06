import streamlit as st
from gradio_client import Client

@st.cache_resource
def get_music_client():
    try:
        return Client("sanchit-gandhi/musicgen-streaming")
    except Exception as e:
        return f"Ошибка подключения к сервису генерации музыки: {str(e)}"

def generate_music(prompt: str) -> tuple[str | None, str | None]:
    """
    Generates music based on the prompt using the Gradio space.
    Returns the file path to the audio and an optional error message.
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
        # The Gradio client returns a tuple, usually the first item is the file path
        if isinstance(result, tuple) and len(result) > 0:
            return result[0], None
        return result, None
    except Exception as e:
        return None, f"Ошибка генерации музыки: {str(e)}"
