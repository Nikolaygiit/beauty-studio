import streamlit as st
from gradio_client import Client
import logging

logger = logging.getLogger(__name__)

@st.cache_resource(show_spinner=False)
def get_music_client():
    """
    Initializes and caches the Gradio client for music generation.
    """
    try:
        return Client("sanchit-gandhi/musicgen-streaming")
    except Exception as e:
        logger.error(f"Failed to initialize music client: {e}")
        return None

def generate_music(prompt: str) -> tuple[str | None, str | None]:
    """
    Generates music using the sanchit-gandhi/musicgen-streaming Gradio space.
    Returns (audio_file_path, error_message).
    """
    client = get_music_client()
    if not client:
        return None, "Ошибка: Не удалось инициализировать клиент для генерации музыки."

    try:
        result = client.predict(
            text_prompt=prompt,
            audio_length_in_s=15,
            play_steps_in_s=1.5,
            seed=0,
            api_name="/generate_audio"
        )
        # client.predict for this space typically returns a tuple, where the first element is the file path
        if isinstance(result, tuple) and len(result) > 0:
            return result[0], None
        return result, None
    except Exception as e:
        error_msg = f"Ошибка генерации музыки: {str(e)}"
        logger.error(error_msg)
        return None, error_msg
