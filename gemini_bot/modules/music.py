import streamlit as st
from gradio_client import Client

@st.cache_resource
def get_music_client() -> Client:
    """
    Initializes and caches the Gradio client for music generation.
    """
    return Client("sanchit-gandhi/musicgen-streaming")

def generate_music(prompt: str) -> tuple[str | None, str | None]:
    """
    Generates music using the Gradio client.
    Returns (audio_path, error_message)
    """
    try:
        client = get_music_client()
        result = client.predict(
            text_prompt=prompt,
            audio_length_in_s=15,
            play_steps_in_s=1.5,
            seed=0,
            api_name="/generate_audio"
        )
        # The result might be a tuple or string depending on the exact Gradio space output,
        # but typically the first element or the string itself is the path to the downloaded file.
        audio_path = result[0] if isinstance(result, tuple) else result
        return audio_path, None
    except Exception as e:
        return None, f"Ошибка генерации музыки: {str(e)}"
