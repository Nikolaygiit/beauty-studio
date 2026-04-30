import streamlit as st
from gradio_client import Client

@st.cache_resource(show_spinner=False)
def get_music_client():
    try:
        return Client("sanchit-gandhi/musicgen-streaming")
    except Exception as e:
        return str(e)

def generate_music(prompt: str):
    client = get_music_client()
    if isinstance(client, str):
        return None, f"Ошибка инициализации генератора музыки: {client}"

    try:
        result = client.predict(
            text_prompt=prompt,
            audio_length_in_s=15,
            play_steps_in_s=1.5,
            seed=0,
            api_name="/generate_audio"
        )
        # result is typically (audio_path, video_path) or just audio_path depending on the space
        # the space sanchit-gandhi/musicgen-streaming returns a tuple where first element is audio
        if isinstance(result, tuple) and len(result) > 0:
            return result[0], None
        return result, None
    except Exception as e:
        return None, f"Ошибка при генерации музыки: {e}"
