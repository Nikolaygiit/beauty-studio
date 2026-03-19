import streamlit as st
from gradio_client import Client

@st.cache_resource
def get_musicgen_client():
    return Client("sanchit-gandhi/musicgen-streaming")

def generate_music(prompt: str) -> str:
    """
    Generates music using sanchit-gandhi/musicgen-streaming space.
    """
    try:
        client = get_musicgen_client()
        result = client.predict(
            text_prompt=prompt,
            audio_length_in_s=15,
            play_steps_in_s=1.5,
            seed=-1,
            api_name="/generate_audio"
        )
        return result
    except Exception as e:
        print(f"Music generation error: {e}")
        return None
