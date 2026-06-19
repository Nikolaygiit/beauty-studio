import streamlit as st
from gradio_client import Client

@st.cache_resource
def get_music_client():
    return Client("sanchit-gandhi/musicgen-streaming")

def generate_music(prompt: str) -> tuple[str | None, str | None]:
    """
    Generates music using MusicGen Gradio space.
    Returns (audio_path, error_message).
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
        return result, None
    except Exception as e:
        return None, f"Error generating music: {str(e)}"
