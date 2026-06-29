import streamlit as st
from gradio_client import Client
from typing import Tuple, Any

@st.cache_resource
def get_video_client() -> Tuple[Any, str]:
    """
    Initializes and caches the Gradio client for Video Generation.
    Returns (client, error_message).
    """
    try:
        client = Client("damo-vilab/modelscope-text-to-video-synthesis")
        return client, ""
    except Exception as e:
        return None, f"Ошибка подключения к сервису генерации видео: {str(e)}"

def generate_video(prompt: str) -> Tuple[str, str]:
    """
    Generates video using the Text-to-Video Gradio space.
    Returns (media_path, error_message).
    """
    client, error = get_video_client()
    if not client:
        return "", error

    try:
        # According to memory: fixed positional params prompt, -1 (seed), 16 (num_frames), 25 (num_inference_steps)
        result = client.predict(
            prompt,
            -1,
            16,
            25,
            api_name="/generate_video"
        )
        return result, ""
    except Exception as e:
        return "", f"Ошибка при генерации видео: {str(e)}"
