import streamlit as st
from gradio_client import Client
from typing import Tuple, Optional, Any

@st.cache_resource(show_spinner=False)
def get_video_client() -> Tuple[Optional[Client], Optional[str]]:
    """
    Initializes and caches the Gradio client for video generation.
    Returns:
        (client, error_message)
    """
    try:
        client = Client("damo-vilab/modelscope-text-to-video-synthesis")
        return client, None
    except Exception as e:
        return None, f"Ошибка при подключении к сервису генерации видео: {str(e)}"

def generate_video(client: Any, prompt: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Generates a video using the provided client.
    Returns:
        (media_path, error_message)
    """
    try:
        # fixed positional parameters for the /generate_video API: prompt, -1 (seed), 16 (num_frames), and 25 (num_inference_steps)
        result = client.predict(
            prompt,
            -1,  # seed
            16,  # num_frames
            25,  # num_inference_steps
            api_name="/generate_video"
        )
        if isinstance(result, tuple):
             media_path = result[1] if len(result) > 1 else result[0]
        elif isinstance(result, dict) and "video" in result:
             media_path = result["video"]
        else:
             media_path = result
        return media_path, None
    except Exception as e:
        return None, f"Ошибка при генерации видео: {str(e)}"
