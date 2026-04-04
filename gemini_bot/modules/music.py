import streamlit as st
from gradio_client import Client

@st.cache_resource
def get_music_client():
    return Client("sanchit-gandhi/musicgen-streaming")

def generate_music(prompt: str) -> str:
    try:
        client = get_music_client()
        result = client.predict(
            prompt,
            api_name="/generate_audio"
        )
        return result
    except Exception as e:
        return f"Ошибка генерации музыки: {str(e)}"
