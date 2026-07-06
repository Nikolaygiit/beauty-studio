import streamlit as st
from gradio_client import Client
from typing import Tuple, Optional

@st.cache_resource
def get_video_client() -> Client:
    """
    Initializes and caches the Gradio client for video generation.
    """
    return Client("damo-vilab/modelscope-text-to-video-synthesis")

def generate_video(prompt: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Generates video using the Gradio client.
    Returns (path_to_video, error_message).
    """
    try:
        client = get_video_client()
        result = client.predict(
            prompt,   # text prompt
            -1,       # seed
            16,       # num_frames
            25,       # num_inference_steps
            api_name="/generate_video"
        )

        # The result is typically a tuple from Gradio API, where the first element is the path or dict
        if isinstance(result, tuple):
             path = result[0]
        else:
             path = result

        # Extract path if it's a dict
        if isinstance(path, dict) and 'video' in path:
            return path['video'], None
        elif isinstance(path, str):
            return path, None
        else:
            return None, "Неизвестный формат ответа от сервиса видео."
    except (ValueError, RuntimeError, Exception) as e:
        return None, f"Ошибка генерации видео: {e}"
