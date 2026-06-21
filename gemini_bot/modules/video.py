import streamlit as st
from gradio_client import Client

@st.cache_resource
def get_video_client():
    """Initializes and caches the Gradio client for video generation."""
    try:
        return Client("damo-vilab/modelscope-text-to-video-synthesis")
    except Exception as e:
        return f"Ошибка инициализации видео клиента: {str(e)}"

def generate_video(prompt: str) -> tuple[str | None, str | None]:
    """
    Generates video using the damo-vilab/modelscope-text-to-video-synthesis Gradio client.
    Returns (video_path, error_message).
    """
    client = get_video_client()
    if isinstance(client, str):
        return None, client

    try:
        # Fixed positional parameters for this specific space
        result = client.predict(
            prompt,
            -1, # seed
            16, # num_frames
            25, # num_inference_steps
            api_name="/generate_video"
        )
        return result, None
    except Exception as e:
        return None, f"Ошибка при генерации видео: {str(e)}"
