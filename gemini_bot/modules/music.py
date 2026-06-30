import streamlit as st
from gradio_client import Client
import traceback

@st.cache_resource
def get_music_client():
    """
    Initializes and returns the Gradio Client for musicgen.
    Returns (client, error_message).
    """
    try:
        client = Client("sanchit-gandhi/musicgen-streaming")
        return client, None
    except Exception as e:
        return None, f"Error initializing music client: {e}"

def generate_music(prompt: str) -> tuple[str, str]:
    """
    Generates music based on the prompt using Gradio musicgen-streaming space.
    Returns (media_path, error_message).
    """
    client, error = get_music_client()
    if error:
        return None, error

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
        traceback.print_exc()
        return None, f"Error generating music: {e}"
