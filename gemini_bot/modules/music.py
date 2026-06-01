import streamlit as st
from gradio_client import Client

@st.cache_resource
def get_music_client():
    """
    Initializes and caches the Gradio client for music generation.
    Returns (client, None) or (None, error_message).
    """
    try:
        client = Client("sanchit-gandhi/musicgen-streaming")
        return client, None
    except Exception as e:
        return None, f"Failed to initialize music generation client: {str(e)}"

def generate_music(prompt: str):
    """
    Generates music using the sanchit-gandhi/musicgen-streaming space.
    Returns (audio_path, None) or (None, error_message).
    """
    client, err = get_music_client()
    if err:
        return None, err

    try:
        # Based on memory, use /generate_audio API endpoint with named args
        result = client.predict(
            text_prompt=prompt,
            audio_length_in_s=15,
            play_steps_in_s=1.5,
            seed=0,
            api_name="/generate_audio"
        )
        # Gradio usually returns a tuple of paths for audio (e.g. streaming chunks or final file)
        # If it's a file path string or tuple:
        if isinstance(result, tuple):
            return result[0], None
        return result, None
    except Exception as e:
        return None, f"Error generating music: {str(e)}"
