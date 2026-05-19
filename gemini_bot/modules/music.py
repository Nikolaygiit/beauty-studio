import streamlit as st
from gradio_client import Client

@st.cache_resource(show_spinner=False)
def get_music_client():
    return Client("sanchit-gandhi/musicgen-streaming")

def generate_music(prompt):
    try:
        # Connect to the Hugging Face Space for music generation
        client = get_music_client()

        # Call the generate_audio endpoint with the required parameters
        result = client.predict(
            text_prompt=prompt,
            audio_length_in_s=15,
            play_steps_in_s=1.5,
            seed=0,
            api_name="/generate_audio"
        )

        # Ensure result is correctly captured as the audio URL/path
        return result, None
    except Exception as e:
        return None, f"Ошибка при генерации музыки: {e}"
