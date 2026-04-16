import streamlit as st
from gradio_client import Client

@st.cache_resource
def get_music_client():
    """Initializes and caches the MusicGen Gradio client."""
    try:
        return Client("sanchit-gandhi/musicgen-streaming")
    except Exception as e:
        return f"Error initializing music client: {e}"

def generate_music(client, prompt):
    """Generates music using the MusicGen client."""
    if isinstance(client, str): # Error during initialization
        return client

    try:
        result = client.predict(
            text_prompt=prompt,
            audio_length_in_s=15,
            play_steps_in_s=1.5,
            seed=0,
            api_name="/generate_audio"
        )
        return result
    except Exception as e:
        return f"Error generating music: {e}"
