import streamlit as st
from gradio_client import Client

@st.cache_resource
def get_music_client():
    """Инициализация и кэширование клиента Gradio для музыки."""
    try:
        return Client("sanchit-gandhi/musicgen-streaming")
    except Exception as e:
        return f"Ошибка подключения к сервису генерации музыки: {str(e)}"

def generate_music(prompt: str):
    """
    Генерирует музыку с использованием sanchit-gandhi/musicgen-streaming.
    Возвращает (путь_к_аудио, None) или (None, сообщение_об_ошибке).
    """
    client = get_music_client()

    if isinstance(client, str):
        # Если client - это строка, значит при инициализации произошла ошибка
        return None, client

    try:
        # Убираем возможные префиксы
        clean_prompt = prompt.lower()
        for kw in ['создай музыку', 'сгенерируй музыку', 'напиши песню', 'песня']:
            clean_prompt = clean_prompt.replace(kw, "").strip()

        if not clean_prompt:
            clean_prompt = prompt

        # Согласно memory: /generate_audio endpoint с kwargs: text_prompt, audio_length_in_s=15, play_steps_in_s=1.5, seed=0
        result = client.predict(
            text_prompt=clean_prompt,
            audio_length_in_s=15,
            play_steps_in_s=1.5,
            seed=0,
            api_name="/generate_audio"
        )

        # Gradio возвращает путь к сохраненному файлу на диске
        return result, None
    except Exception as e:
        return None, f"Произошла ошибка при генерации музыки: {str(e)}"
