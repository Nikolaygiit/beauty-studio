import streamlit as st
from gradio_client import Client

@st.cache_resource
def get_music_client():
    """Initializes and caches the MusicGen Gradio client."""
    try:
        return Client("sanchit-gandhi/musicgen-streaming")
    except Exception as e:
        return None, f"Failed to initialize Music client: {e}"

def generate_music(prompt):
    """Generates music from a text prompt using MusicGen."""
    client = get_music_client()

    # If get_music_client returned a tuple, it means an error occurred
    if isinstance(client, tuple):
        return None, client[1]

    try:
        result = client.predict(
            text_prompt=prompt,
            audio_length_in_s=15,
            play_steps_in_s=1.5,
            seed=0,
            api_name="/generate_audio"
        )
        # The result from Gradio for an audio file is usually the local file path
        return result, None
    except Exception as e:
        return None, f"Error generating music: {e}"
