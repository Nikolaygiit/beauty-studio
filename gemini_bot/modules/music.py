import streamlit as st
from gradio_client import Client

@st.cache_resource(show_spinner=False)
def get_music_client():
    """
    Initializes and caches the gradio client for musicgen-streaming.
    """
    try:
        client = Client("sanchit-gandhi/musicgen-streaming")
        return client
    except Exception as e:
        return f"Error initializing music client: {e}"

def generate_music(client, prompt):
    """
    Generates music given a prompt using the /generate_audio endpoint.
    Returns the path to the audio file or an error message.
    """
    if isinstance(client, str):
        return None, client # Return error string

    try:
        result = client.predict(
            prompt=prompt,
            api_name="/generate_audio"
        )
        return result, None
    except Exception as e:
        return None, f"Runtime error generating music: {e}"
