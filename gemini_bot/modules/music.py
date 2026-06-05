import streamlit as st
from gradio_client import Client

@st.cache_resource(show_spinner=False)
def get_music_client():
    """Returns a cached Gradio client for musicgen-streaming."""
    try:
        return Client("sanchit-gandhi/musicgen-streaming")
    except Exception as e:
        return None

def generate_music(prompt: str) -> tuple[str | None, str | None]:
    """
    Generates music using the sanchit-gandhi/musicgen-streaming Gradio Space.
    Returns (audio_path, error_message).
    """
    client = get_music_client()
    if not client:
        return None, "Не удалось инициализировать клиент для генерации музыки."

    try:
        result = client.predict(
            text_prompt=prompt,
            audio_length_in_s=15,
            play_steps_in_s=1.5,
            seed=0,
            api_name="/generate_audio"
        )
        # The API returns a tuple where the first element is the path to the generated audio
        if isinstance(result, tuple) and len(result) > 0:
            return result[0], None
        elif isinstance(result, str):
            return result, None
        else:
            return None, "Неизвестный формат ответа от сервера."
    except Exception as e:
        return None, f"Ошибка при генерации музыки: {e}"
