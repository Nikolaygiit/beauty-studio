import streamlit as st
from gradio_client import Client
from typing import Tuple, Optional

@st.cache_resource
def get_video_client() -> Tuple[Optional[Client], Optional[str]]:
    """
    Initializes and caches the Gradio client for video generation.
    Returns (Client, error_message).
    """
    try:
        client = Client("damo-vilab/modelscope-text-to-video-synthesis")
        return client, None
    except Exception as e:
        return None, f"Ошибка подключения к сервису генерации видео: {str(e)}"

def generate_video(client: Client, prompt: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Generates a video based on a text prompt.
    Returns (video_path, error_message).
    """
    try:
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
