import streamlit as st
from gradio_client import Client

@st.cache_resource(show_spinner=False)
def get_music_client():
    try:
        return Client("sanchit-gandhi/musicgen-streaming")
    except Exception as e:
        print(f"Error initializing music client: {e}")
        return None

def generate_music(prompt):
    """
    Generates music using the sanchit-gandhi/musicgen-streaming space.
    """
    client = get_music_client()
    if not client:
        return None

    try:
        # Default settings: audio_length_in_s=15, play_steps_in_s=1.5, seed=5
        result = client.predict(
            text_prompt=prompt,
            audio_length_in_s=15,
            play_steps_in_s=1.5,
            seed=5,
            api_name="/generate_audio"
        )
        # The API returns the filepath to the generated audio
        return result
    except Exception as e:
        print(f"Error generating music: {e}")
        return None
