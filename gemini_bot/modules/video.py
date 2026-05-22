import streamlit as st
from gradio_client import Client

@st.cache_resource
def get_video_client():
    """Initializes and caches the Gradio client for video generation."""
    try:
        return Client("damo-vilab/modelscope-text-to-video-synthesis")
    except Exception as e:
        return None

def generate_video(prompt: str) -> tuple[str | None, str | None]:
    """
    Generates video using the damo-vilab/modelscope-text-to-video-synthesis Gradio space.
    Returns (video_path, None) on success, or (None, error_message) on failure.
    """
    client = get_video_client()
    if not client:
        return None, "Не удалось инициализировать клиент для генерации видео."

    try:
        # The damo-vilab space takes positional arguments for /generate_video
        # 1. prompt (text), 2. seed (-1), 3. num_frames (16), 4. num_inference_steps (25)
        result = client.predict(
            prompt,
            -1,  # seed
            16,  # num_frames
            25,  # num_inference_steps
            api_name="/generate_video"
        )
        # The result is typically a dictionary containing 'video' key
        if isinstance(result, dict) and 'video' in result:
             return result['video'], None
        elif isinstance(result, str):
            # Sometimes it returns a string path directly
            return result, None
        elif isinstance(result, tuple) and len(result) > 0 and 'video' in result[0]:
            return result[0]['video'], None

        # Fallback if structure is unexpected
        return str(result), None

    except Exception as e:
        return None, f"Ошибка при генерации видео: {str(e)}"
