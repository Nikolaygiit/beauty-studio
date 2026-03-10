import streamlit as st
from gradio_client import Client

@st.cache_resource
def get_music_client():
    return Client("sanchit-gandhi/musicgen-streaming")

def generate_music(prompt):
    try:
        client = get_music_client()
        # "model": "facebook/musicgen-small", "text": prompt
        result = client.predict(
                prompt,	# str in 'Describe your music!' Textbox component
                api_name="/generate_audio"
        )
        return result
    except Exception as e:
        return f"Произошла ошибка при генерации музыки: {str(e)}"
