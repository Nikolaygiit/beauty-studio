import streamlit as st
from gradio_client import Client

@st.cache_resource
def get_music_client():
    """
    Initializes and caches the Gradio client for music generation.
    """
    try:
        return Client("sanchit-gandhi/musicgen-streaming")
    except Exception as e:
        return f"Ошибка при подключении к сервису музыки: {str(e)}"

def generate_music(prompt: str) -> tuple[str | None, str | None]:
    """
    Generates music using the sanchit-gandhi/musicgen-streaming Gradio Space.
    Returns a tuple of (audio_path, error_message).
    """
    client = get_music_client()
    if isinstance(client, str):
        return None, client # Return the initialization error message

    try:
        result = client.predict(
            text_prompt=prompt,
            audio_length_in_s=15,
            play_steps_in_s=1.5,
            seed=0,
            api_name="/generate_audio"
        )
        # The API returns a tuple where the first element is the path to the audio file
        if result and isinstance(result, tuple) and len(result) > 0:
            return result[0], None
        else:
            return None, "Неизвестный формат ответа от сервиса музыки."
    except Exception as e:
        return None, f"Ошибка при генерации музыки: {str(e)}"
