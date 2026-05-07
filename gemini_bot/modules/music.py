import streamlit as st
from gradio_client import Client

@st.cache_resource
def get_music_client():
    """Initialize and cache the music generation client."""
    try:
        return Client("sanchit-gandhi/musicgen-streaming")
    except Exception as e:
        return str(e)

def generate_music(prompt: str):
    """
    Generates music using the sanchit-gandhi/musicgen-streaming space.
    Returns (audio_path, error_message).
    """
    client_or_error = get_music_client()
    if isinstance(client_or_error, str):
        return None, f"Error initializing music client: {client_or_error}"

    try:
        client = client_or_error
        result = client.predict(
            text_prompt=prompt,
            audio_length_in_s=15,
            play_steps_in_s=1.5,
            seed=0,
            api_name="/generate_audio"
        )
        return result, None
    except Exception as e:
        return None, f"Error generating music: {e}"
