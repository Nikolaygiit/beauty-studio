import streamlit as st
from gradio_client import Client
from typing import Tuple, Optional

@st.cache_resource
def get_video_client() -> Tuple[Optional[Client], Optional[str]]:
    """
    Initializes and caches the Gradio client for video generation.
    Returns (client, error_message).
    """
    try:
        client = Client("damo-vilab/modelscope-text-to-video-synthesis")
        return client, None
    except Exception as e:
        return None, f"Ошибка инициализации видео клиента: {str(e)}"

def generate_video(prompt: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Generates video based on the prompt using the cached Gradio client.
    Returns (media_path, error_message).
    """
    client, error = get_video_client()
    if error:
        return None, error

    try:
        # According to memory: fixed positional parameters: prompt, -1 (seed), 16 (num_frames), 25 (num_inference_steps)
        result = client.predict(
            prompt,
            -1,
            16,
            25,
            api_name="/generate_video"
        )

        # `result` may be a tuple or string containing the path
        if isinstance(result, tuple) and len(result) > 0:
            return result[0], None
        elif isinstance(result, dict) and 'video' in result:
             return result['video'], None
        return result, None
    except Exception as e:
        return None, f"Ошибка генерации видео: {str(e)}"
