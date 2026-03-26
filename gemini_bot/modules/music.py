import streamlit as st
from gradio_client import Client

@st.cache_resource
def get_music_client():
    """Initialize and cache the music generation client."""
    try:
        return Client("sanchit-gandhi/musicgen-streaming")
    except Exception as e:
        return f"Ошибка подключения к сервису генерации музыки: {e}"

def generate_music(prompt: str):
    """Generates music using MusicGen Streaming via Gradio."""
    client = get_music_client()
    if isinstance(client, str):
        return client # Return error message

    try:
        # Based on typical MusicGen Gradio space API
        # The /generate_audio endpoint takes prompt as text
        result = client.predict(
                text=prompt,
                api_name="/predict"
        )
        return result
    except Exception as e:
        return f"Произошла ошибка при генерации музыки: {e}"
