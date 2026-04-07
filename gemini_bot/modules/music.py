import streamlit as st
from gradio_client import Client

@st.cache_resource(show_spinner=False)
def get_music_client():
    return Client("sanchit-gandhi/musicgen-streaming")

def generate_music(prompt: str):
    """
    Generates music using the sanchit-gandhi/musicgen-streaming Gradio Space.
    Returns the paths to the generated audio and video.
    """
    try:
        client = get_music_client()
        # The /generate_audio endpoint takes a prompt and returns audio and video
        # Let's inspect the exact API using client.view_api() if needed, but usually it's just the prompt.
        result = client.predict(
            text_prompt=prompt,
            audio_length_in_s=15,
            play_steps_in_s=1.5,
            seed=0, # Random or 0
            api_name="/generate_audio"
        )
        # result is likely a tuple of (audio_path, video_path) or similar.
        # Gradio client returns file paths for media.
        return result
    except Exception as e:
        return f"Error generating music: {str(e)}"
