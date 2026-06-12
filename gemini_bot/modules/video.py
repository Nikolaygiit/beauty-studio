import streamlit as st
from gradio_client import Client

@st.cache_resource
def get_video_client():
    try:
        return Client("damo-vilab/modelscope-text-to-video-synthesis")
    except Exception as e:
        return f"Ошибка инициализации Video: {str(e)}"

def generate_video(prompt: str) -> tuple[str, str]:
    """
    Generates video using Gradio client.
    Returns (path_to_video_file, error_message).
    """
    client_or_error = get_video_client()
    if isinstance(client_or_error, str):
        return None, client_or_error

    try:
        result = client_or_error.predict(
            prompt,
            -1,  # seed
            16,  # num_frames
            25,  # num_inference_steps
            api_name="/generate_video"
        )
        # result typically contains path to the video
        # grad_client might return a dict or string based on version, let's assume dict or string path
        video_path = result.get('video') if isinstance(result, dict) else result
        return video_path, None
    except Exception as e:
        return None, f"Ошибка при генерации видео: {str(e)}"
