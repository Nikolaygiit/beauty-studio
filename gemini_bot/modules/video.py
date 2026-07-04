import streamlit as st
from gradio_client import Client
from typing import Tuple, Optional, Any

@st.cache_resource
def get_video_client() -> Tuple[Optional[Any], Optional[str]]:
    """
    Initializes and caches the Gradio client for video generation.
    Returns a tuple of (client, error_message).
    """
    try:
        client = Client("damo-vilab/modelscope-text-to-video-synthesis")
        return client, None
    except Exception as e:
        return None, f"Ошибка при инициализации видео-клиента: {str(e)}"

def generate_video(prompt: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Generates a video using the Gradio video client based on the prompt.
    Returns a tuple of (video_path, error_message).
    """
    client, error = get_video_client()
    if error:
        return None, error

    try:
        # Pass fixed positional arguments: prompt, -1 (seed), 16 (num_frames), 25 (num_inference_steps)
        result = client.predict(
            prompt,
            -1,
            16,
            25,
            api_name="/generate_video"
        )

        # Expecting string or list containing dict with path
        if isinstance(result, str):
             return result, None
        elif isinstance(result, list) and len(result) > 0 and 'video' in result[0]:
             # Just in case format differs
             return result[0]['video'], None
        elif isinstance(result, tuple) and len(result) > 0:
             return result[0], None
        elif isinstance(result, dict) and 'video' in result:
             return result['video'], None
        else:
             # Assume result is the file path or contains it
             return str(result), None

    except (ValueError, RuntimeError, Exception) as e:
        return None, f"Ошибка при генерации видео: {str(e)}"
