import streamlit as st
from gradio_client import Client

@st.cache_resource(show_spinner=False)
def get_music_client():
    """Returns a cached Gradio Client for music generation."""
    try:
        return Client("sanchit-gandhi/musicgen-streaming", timeout=60), None
    except Exception as e:
        return None, f"Ошибка подключения к сервису генерации музыки: {e}"

def generate_music(prompt: str):
    """Generates music using the sanchit-gandhi/musicgen-streaming space."""
    client, error = get_music_client()
    if error:
        return None, error

    try:
        result = client.predict(
            text_prompt=prompt,
            audio_length_in_s=15,
            play_steps_in_s=1.5,
            seed=0,
            api_name="/generate_audio"
        )
        # The API might return different formats, usually a tuple where the first element is the filepath or a string filepath
        if isinstance(result, tuple) and len(result) > 0:
            return result[0], None
        elif isinstance(result, str):
            return result, None
        else:
             return None, "Неизвестный формат ответа от сервиса генерации музыки."
    except Exception as e:
        return None, f"Ошибка генерации музыки: {e}"
