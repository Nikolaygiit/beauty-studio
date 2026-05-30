import streamlit as st
from gradio_client import Client

@st.cache_resource
def get_music_client():
    """
    Инициализирует и кэширует Gradio-клиент для генерации музыки.
    """
    try:
        return Client("sanchit-gandhi/musicgen-streaming")
    except Exception as e:
        return f"Ошибка инициализации клиента: {str(e)}"

def generate_music(prompt: str) -> tuple[str | None, str | None]:
    """
    Генерирует музыку через модель MusicGen.
    Возвращает: (путь_к_аудиофайлу, сообщение_об_ошибке)
    """
    client = get_music_client()

    if isinstance(client, str): # Ошибка при инициализации
        return None, client

    try:
        # Вызываем API модели MusicGen
        result = client.predict(
            text_prompt=prompt,
            audio_length_in_s=15,
            play_steps_in_s=1.5,
            seed=0,
            api_name="/generate_audio"
        )
        return result, None
    except Exception as e:
        return None, f"Ошибка при генерации музыки: {str(e)}"
