import streamlit as st
from gradio_client import Client

@st.cache_resource(show_spinner=False)
def get_video_client():
    """
    Initializes and caches the Gradio Client for video generation.
    """
    return Client("damo-vilab/modelscope-text-to-video-synthesis")

def generate_video(prompt: str) -> tuple[str, str]:
    """
    Generates video using the damo-vilab/modelscope-text-to-video-synthesis Gradio Space.
    Returns (video_path, error_message).
    """
    try:
        client = get_video_client()
        result = client.predict(
            prompt,
            -1,  # seed
            16,  # num_frames
            25,  # num_inference_steps
            api_name="/generate_video"
        )
        return result, None
    except Exception as e:
        return None, f"Ошибка при генерации видео: {e}"
