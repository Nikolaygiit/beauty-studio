import streamlit as st
from gradio_client import Client
import time

@st.cache_resource(show_spinner=False)
def get_video_client():
    """Initializes and caches the video generation Gradio client."""
    try:
        return Client("damo-vilab/modelscope-text-to-video-synthesis")
    except Exception as e:
        if "RUNTIME_ERROR" in str(e):
            return "Ошибка RUNTIME_ERROR: Сервис видео временно недоступен. Попробуйте позже."
        return f"Ошибка подключения к сервису видео: {e}"

def generate_video(prompt):
    """
    Generates video using the damo-vilab/modelscope-text-to-video-synthesis Gradio Space.
    """
    client = get_video_client()

    if isinstance(client, str):
        return client # Return error message

    try:
        # According to memory: /generate_video API, prompt, -1 (seed), 16 (num_frames), 25 (num_inference_steps)
        result = client.predict(
            prompt,
            -1,  # seed
            16,  # num_frames
            25,  # num_inference_steps
            api_name="/generate_video"
        )
        # The result typically contains the path to the generated video file
        return result
    except Exception as e:
        if "RUNTIME_ERROR" in str(e):
            return "Ошибка RUNTIME_ERROR: Сервис видео временно недоступен. Попробуйте позже."
        return f"Произошла ошибка при генерации видео: {e}"
