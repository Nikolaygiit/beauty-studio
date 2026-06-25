import streamlit as st
from gradio_client import Client

@st.cache_resource(show_spinner=False)
def get_video_client():
    """
    Initializes and caches the Video Gradio client.
    Returns (client, error_message).
    """
    try:
        client = Client("damo-vilab/modelscope-text-to-video-synthesis")
        return client, None
    except Exception as e:
        return None, f"Ошибка инициализации видео-клиента: {str(e)}"

def generate_video(prompt: str):
    """
    Generates video using the ModelScope client.
    Returns (media_path, error_message).
    """
    client, error = get_video_client()
    if error:
        return None, error

    try:
        result = client.predict(
            prompt,   # prompt
            -1,       # seed
            16,       # num_frames
            25,       # num_inference_steps
            api_name="/generate_video"
        )
        if isinstance(result, tuple) or isinstance(result, list):
             return result[0], None
        return result, None
    except Exception as e:
        # Gracefully handle string errors
        return None, f"Ошибка генерации видео: {str(e)}"
