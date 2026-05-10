import streamlit as st
from gradio_client import Client

@st.cache_resource
def get_music_client():
    """Initializes and caches the gradio client for music generation."""
    try:
        return Client("sanchit-gandhi/musicgen-streaming")
    except Exception as e:
        return None

def generate_music(prompt):
    """
    Generates music using the sanchit-gandhi/musicgen-streaming space.
    Returns a tuple of (audio_path, error_message).
    """
    client = get_music_client()
    if not client:
        return None, "Failed to initialize music generation client."

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
        return None, f"Error generating music: {e}"
