import streamlit as st
from gradio_client import Client

@st.cache_resource
def get_music_client():
    """Caches the initialization of the Gradio music client."""
    try:
        return Client("sanchit-gandhi/musicgen-streaming")
    except Exception as e:
        return f"Error initializing music client: {e}"

def generate_music(prompt):
    """Generates music using the sanchit-gandhi/musicgen-streaming space."""
    client = get_music_client()

    if isinstance(client, str):
         return None, client # Return error string

    try:
        result = client.predict(
            text_prompt=prompt,
            audio_length_in_s=15,
            play_steps_in_s=1.5,
            seed=0,
            api_name="/generate_audio"
        )
        return result, None # Result is a path to the generated audio file
    except Exception as e:
        return None, f"Error generating music: {e}"
