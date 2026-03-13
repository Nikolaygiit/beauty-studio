from gradio_client import Client
import streamlit as st

@st.cache_resource
def get_music_client():
    try:
        return Client("sanchit-gandhi/musicgen-streaming")
    except Exception as e:
        return f"Error initializing music client: {e}"

def generate_music(prompt):
    client = get_music_client()
    if isinstance(client, str):
        return client

    try:
        result = client.predict(
            text_prompt=prompt,
            audio_length_in_s=15,
            play_steps_in_s=1.5,
            seed=5,
            api_name="/generate_audio"
        )
        return result
    except Exception as e:
        return f"Error generating music: {e}"
