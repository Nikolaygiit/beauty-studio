import streamlit as st
from gradio_client import Client

@st.cache_resource
def get_music_client():
    """
    Инициализирует и кэширует Gradio клиент для генерации музыки.
    """
    try:
        client = Client("sanchit-gandhi/musicgen-streaming")
        return client, ""
    except Exception as e:
        return None, f"Ошибка инициализации музыкального клиента: {str(e)}"

def generate_music(prompt: str) -> tuple[str, str]:
    """
    Генерирует музыку через sanchit-gandhi/musicgen-streaming Gradio Space.
    Возвращает (audio_path, error_message).
    """
    client, err = get_music_client()
    if err:
        return None, err

    try:
        result = client.predict(
            text_prompt=prompt,
            audio_length_in_s=15,
            play_steps_in_s=1.5,
            seed=0,
            api_name="/generate_audio"
        )
        return result, ""
    except Exception as e:
        return None, f"Ошибка при генерации музыки: {str(e)}"
