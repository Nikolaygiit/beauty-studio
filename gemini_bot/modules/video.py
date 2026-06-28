import streamlit as st
from gradio_client import Client

@st.cache_resource
def get_video_client():
    """
    Initializes and caches the Gradio client for video generation.
    Returns (client, error_message).
    """
    try:
        client = Client("damo-vilab/modelscope-text-to-video-synthesis")
        return client, None
    except Exception as e:
        return None, f"Ошибка при инициализации клиента видео: {str(e)}"

def generate_video(prompt: str):
    """
    Generates video using the damo-vilab/modelscope-text-to-video-synthesis Gradio client.
    Returns (video_path, error_message).
    """
    client, error = get_video_client()
    if error:
        return None, error

    try:
        result = client.predict(
            prompt,
            -1,   # seed
            16,   # num_frames
            25,   # num_inference_steps
            api_name="/generate_video"
        )
        # The result is typically a dictionary containing 'video' key with the path
        if isinstance(result, dict) and 'video' in result:
            return result['video'], None
        elif isinstance(result, str):
             # sometimes it returns just the file path
             return result, None
        elif isinstance(result, tuple) and len(result) > 0:
            return result[0], None
        return str(result), None
    except Exception as e:
        return None, f"Ошибка при генерации видео: {str(e)}"
