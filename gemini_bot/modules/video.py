import streamlit as st
from gradio_client import Client

@st.cache_resource
def get_video_client():
    try:
        return Client("damo-vilab/modelscope-text-to-video-synthesis")
    except Exception as e:
        return f"Error loading model: {str(e)}"

def generate_video(prompt: str):
    """
    Generate video using Gradio client for modelscope-text-to-video-synthesis.
    """
    client_or_err = get_video_client()

    if isinstance(client_or_err, str):
        return None, client_or_err

    try:
        result = client_or_err.predict(
            prompt,
            -1,  # seed
            16,  # num_frames
            25,  # num_inference_steps
            api_name="/generate_video"
        )
        return result, None
    except Exception as e:
        return None, f"Ошибка при генерации видео: {str(e)}"
