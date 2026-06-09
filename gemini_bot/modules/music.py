import streamlit as st
from gradio_client import Client

@st.cache_resource
def get_music_client():
    try:
        return Client("sanchit-gandhi/musicgen-streaming")
    except Exception as e:
        return f"Client error: {str(e)}"

def generate_music(prompt: str) -> tuple[str | None, str | None]:
    client = get_music_client()
    if isinstance(client, str):
        return None, f"Ошибка инициализации: {client}"

    try:
        result = client.predict(
            text_prompt=prompt,
            audio_length_in_s=15,
            play_steps_in_s=1.5,
            seed=0,
            api_name="/generate_audio"
        )
        # The API returns a tuple where the first element is the path
        if isinstance(result, tuple) and len(result) > 0:
            return result[0], None
        return result, None
    except Exception as e:
        return None, f"Ошибка при генерации музыки: {str(e)}"
