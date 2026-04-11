import streamlit as st
from gradio_client import Client

@st.cache_resource
def get_video_client():
    """Initializes and caches the Gradio client for video generation. Returns an error message if it fails."""
    try:
        return Client("damo-vilab/modelscope-text-to-video-synthesis")
    except Exception as e:
        return f"Ошибка при инициализации видео-клиента: {str(e)}"

def generate_video(prompt):
    """Generates a video from the given prompt using the cached client."""
    client_or_error = get_video_client()
    if isinstance(client_or_error, str):
        # Initialisation failed
        return client_or_error

    try:
        result = client_or_error.predict(
            prompt,
            -1,
            16,
            25,
            api_name="/generate_video"
        )
        # The API usually returns a dict with 'video' containing the file path
        if isinstance(result, dict) and "video" in result:
             return result["video"]
        return result
    except Exception as e:
        return f"Ошибка при генерации видео: {str(e)}"
