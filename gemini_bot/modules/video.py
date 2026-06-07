from gradio_client import Client
import streamlit as st

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
        return None, f"Ошибка инициализации клиента для видео: {str(e)}"

def generate_video(prompt: str):
    """
    Generates video based on the prompt using the cached client.
    Returns (video_path, None) on success, or (None, error_message) on failure.
    """
    client, error = get_video_client()
    if error:
        return None, error

    try:
        result = client.predict(
            prompt,
            -1,
            16,
            25,
            api_name="/generate_video"
        )
        return result, None
    except Exception as e:
        return None, f"Ошибка при генерации видео: {str(e)}"
