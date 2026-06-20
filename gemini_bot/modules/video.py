import streamlit as st
from gradio_client import Client
from typing import Tuple, Optional

@st.cache_resource
def get_video_client() -> Optional[Client]:
    """
    Initializes and caches the Gradio client for video generation.
    """
    try:
        return Client("damo-vilab/modelscope-text-to-video-synthesis")
    except Exception as e:
        return None

def generate_video(prompt: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Generates video using the damo-vilab/modelscope-text-to-video-synthesis space.
    Returns a tuple of (file_path, error_message).
    """
    client = get_video_client()
    if client is None:
        return None, "Ошибка инициализации клиента для генерации видео."

    try:
        # The /generate_video endpoint takes positional arguments: prompt, seed, num_frames, num_inference_steps
        result = client.predict(
            prompt,
            -1,  # seed
            16,  # num_frames
            25,  # num_inference_steps
            api_name="/generate_video"
        )
        return result, None
    except Exception as e:
        return None, f"Ошибка при генерации видео: {str(e)}"
