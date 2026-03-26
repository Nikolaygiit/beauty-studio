import streamlit as st
from gradio_client import Client

@st.cache_resource
def get_video_client():
    """Initialize and cache the video generation client."""
    try:
        return Client("damo-vilab/modelscope-text-to-video-synthesis")
    except Exception as e:
        return f"Ошибка подключения к сервису генерации видео: {e}"

def generate_video(prompt: str):
    """Generates video using ModelScope via Gradio."""
    client = get_video_client()
    if isinstance(client, str):
        return client # Return error string

    try:
        # Based on damo-vilab/modelscope-text-to-video-synthesis API
        result = client.predict(
                prompt=prompt,
                video_length=16, # Typically translates to num_frames
                fps=8,
                num_inference_steps=25,
                seed=-1,
                api_name="/generate_video"
        )
        return result
    except Exception as e:
        return f"Произошла ошибка при генерации видео: {e}"
