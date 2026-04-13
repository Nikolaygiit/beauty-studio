import streamlit as st
from gradio_client import Client
import shutil

@st.cache_resource
def get_music_client():
    """Initializes and caches the Gradio client for music generation."""
    try:
        return Client("sanchit-gandhi/musicgen-streaming")
    except Exception as e:
        return f"Client Init Error: {e}"

def generate_music(prompt):
    """
    Generates music using the sanchit-gandhi/musicgen-streaming space.
    """
    client = get_music_client()
    if isinstance(client, str): # Error during initialization
        return None, client

    try:
        result = client.predict(
            text_prompt=prompt,
            audio_length_in_s=15,
            play_steps_in_s=1.5,
            seed=0,
            api_name="/generate_audio"
        )
        # result is a tuple, first element might be the audio file path
        if isinstance(result, tuple) and len(result) > 0:
            return result[0], None
        return result, None
    except Exception as e:
        return None, f"Prediction Error: {e}"
