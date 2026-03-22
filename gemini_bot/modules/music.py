import streamlit as st
from gradio_client import Client
import random

@st.cache_resource(show_spinner=False)
def get_music_client():
    """Caches the Gradio Client for music generation to prevent re-initialization."""
    try:
        return Client("sanchit-gandhi/musicgen-streaming")
    except Exception as e:
        return f"Error loading music client: {e}"

def generate_music(prompt: str) -> str:
    """Generates music using the sanchit-gandhi/musicgen-streaming Gradio Space."""
    client = get_music_client()
    if isinstance(client, str):
         return client # Return the error message

    try:
        seed = float(random.randint(0, 10000))
        # Predict parameters: text_prompt, audio_length_in_s, play_steps_in_s, seed
        result = client.predict(
            text_prompt=prompt,
            audio_length_in_s=15.0,
            play_steps_in_s=1.5,
            seed=seed,
            api_name="/generate_audio"
        )
        # Returns a tuple or filepath string depending on the exact Gradio interface.
        # For this specific space, it returns the generated filepath.
        return result
    except Exception as e:
        return f"Произошла ошибка при генерации музыки: {e}"
