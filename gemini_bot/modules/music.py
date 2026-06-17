import streamlit as st
from gradio_client import Client

@st.cache_resource
def get_music_client():
    try:
        return Client("sanchit-gandhi/musicgen-streaming")
    except Exception as e:
        return None

def generate_music(prompt: str) -> tuple[str | None, str | None]:
    if not prompt:
        return None, "Prompt is required for music generation"

    client = get_music_client()
    if not client:
        return None, "Failed to initialize music generation client"

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
        return None, f"Error generating music: {str(e)}"
