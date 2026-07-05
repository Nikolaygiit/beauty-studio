import streamlit as st
from gradio_client import Client

@st.cache_resource
def get_video_client():
    """
    Initializes and caches the Gradio client for video generation.
    Returns (client, None) on success, or (None, error_message) on failure.
    """
    try:
        client = Client("damo-vilab/modelscope-text-to-video-synthesis")
        return client, None
    except Exception as e:
        return None, f"Ошибка при подключении к сервису видео: {str(e)}"

def generate_video(prompt: str) -> tuple[str | None, str | None]:
    """
    Generates a video based on a prompt.
    Returns (path_to_video, None) on success, or (None, error_message) on failure.
    """
    client, error = get_video_client()
    if error:
        return None, error

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
