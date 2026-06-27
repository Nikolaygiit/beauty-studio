import streamlit as st
from gradio_client import Client

@st.cache_resource
def get_video_client():
    """
    Initializes and caches the Video Generation Gradio client.
    Returns (client, error_message).
    """
    try:
        client = Client("damo-vilab/modelscope-text-to-video-synthesis")
        return client, None
    except (ValueError, RuntimeError, Exception) as e:
        return None, f"Ошибка инициализации видео клиента: {str(e)}"

def generate_video(prompt: str):
    """
    Generates video using the ModelScope client.
    Returns (media_path, error_message).
    """
    client, error = get_video_client()
    if error:
        return None, error

    try:
        # Use positional arguments for the prediction
        # prompt, seed, num_frames, num_inference_steps
        result = client.predict(
            prompt,
            -1,  # seed
            16,  # num_frames
            25,  # num_inference_steps
            api_name="/generate_video"
        )
        # result is typically a dictionary containing 'video' key with the path
        # depending on gradio_client version, it might be a string path directly
        if isinstance(result, dict) and 'video' in result:
             return result['video'], None
        return result, None
    except (ValueError, RuntimeError, Exception) as e:
        return None, f"Ошибка при создании видео: {str(e)}"
