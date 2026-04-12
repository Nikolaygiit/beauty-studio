import streamlit as st
from gradio_client import Client

@st.cache_resource
def get_music_client():
    """Initializes and caches the gradio client for music generation."""
    try:
        return Client("sanchit-gandhi/musicgen-streaming")
    except Exception as e:
        return f"Error initializing music client: {e}"

def generate_music(prompt):
    """
    Generates music using the sanchit-gandhi/musicgen-streaming space.
    Uses the /generate_audio API endpoint.
    """
    client = get_music_client()
    if isinstance(client, str):
        return client, None # return error message

    try:
        result = client.predict(
            text_prompt=prompt,
            audio_length_in_s=15,
            play_steps_in_s=1.5,
            seed=0,
            api_name="/generate_audio"
        )
        return None, result # return None error, result audio path
    except Exception as e:
        return f"Error generating music: {e}", None
