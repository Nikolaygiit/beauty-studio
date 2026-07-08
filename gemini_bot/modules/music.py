import streamlit as st
from gradio_client import Client

@st.cache_resource
def get_music_client():
    """
    Initializes and caches the Gradio client for music generation.
    Returns (client, error_message).
    """
    try:
        client = Client("sanchit-gandhi/musicgen-streaming")
        return client, None
    except Exception as e:
        return None, f"Failed to initialize music client: {e}"

def generate_music(prompt: str):
    """
    Generates music using the cached musicgen-streaming model.
    Returns (media_path, error_message).
    """
    if not prompt:
        return None, "Prompt cannot be empty"

    client, err = get_music_client()
    if err:
        return None, err

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
        return None, str(e)
