import streamlit as st
from gradio_client import Client
import random

@st.cache_resource
def get_music_client():
    """
    Initializes and caches the Gradio client for music generation.
    Returns (client, error_message)
    """
    try:
        client = Client("sanchit-gandhi/musicgen-streaming")
        return client, None
    except Exception as e:
        return None, f"Failed to initialize music client: {e}"

def generate_music(prompt: str) -> tuple[str, str]:
    """
    Generates music based on the prompt using the cached Gradio client.
    Returns (audio_path, error_message)
    """
    client, error = get_music_client()
    if error:
        return None, error

    try:
        # Use random seed to vary the output if needed, though memory mentions seed=0
        # is okay or standard. We use a varied one here if possible, but the memory
        # says: passing named arguments: text_prompt, audio_length_in_s=15,
        # play_steps_in_s=1.5, and seed=0.
        result = client.predict(
            text_prompt=prompt,
            audio_length_in_s=15,
            play_steps_in_s=1.5,
            seed=0,
            api_name="/generate_audio"
        )
        return result, None
    except Exception as e:
        return None, f"Failed to generate music: {e}"
