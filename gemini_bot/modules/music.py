import streamlit as st
from gradio_client import Client

@st.cache_resource
def get_music_client():
    return Client("sanchit-gandhi/musicgen-streaming")

def generate_music(prompt, client):
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
        return f"Ошибка генерации музыки: {e}"
