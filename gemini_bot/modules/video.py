import streamlit as st
from gradio_client import Client

@st.cache_resource(show_spinner=False)
def get_video_client():
    """
    Initializes and caches the Gradio client for video generation.
    Handles RUNTIME_ERROR gracefully.
    """
    try:
        return Client("damo-vilab/modelscope-text-to-video-synthesis")
    except Exception as e:
        return str(e)

def generate_video(prompt):
    """
    Generates video based on a text prompt.
    Fixed parameters: seed -1, 16 frames, 25 inference steps.
    """
    client = get_video_client()
    if isinstance(client, str):
        return None, f"Ошибка подключения к сервису видео: {client}"

    try:
        result = client.predict(
            prompt,	# str in 'Prompt' Textbox component
            -1,	# int | float in 'Seed' Number component (-1 for random)
            16,	# int | float in 'Number of Frames' Number component
            25,	# int | float in 'Number of Inference Steps' Number component
            api_name="/generate_video"
        )
        # Gradio usually returns the path to the video file
        return result, None
    except Exception as e:
        return None, f"Ошибка генерации видео: {str(e)}"
