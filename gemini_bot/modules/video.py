import streamlit as st
from gradio_client import Client

@st.cache_resource
def get_video_client():
    try:
        return Client("damo-vilab/modelscope-text-to-video-synthesis")
    except Exception as e:
        return f"RUNTIME_ERROR: Ошибка инициализации клиента видео: {e}"

def generate_video(prompt):
    """
    Generates video using the damo-vilab/modelscope-text-to-video-synthesis Gradio Space.
    Returns (video_path, None) on success, or (None, error_message) on failure.
    """
    client = get_video_client()
    if isinstance(client, str) and client.startswith("RUNTIME_ERROR"):
        return None, client

    try:
        # Fixed positional parameters for the /generate_video API as specified
        result = client.predict(
            prompt,
            -1,  # seed
            16,  # num_frames
            25,  # num_inference_steps
            api_name="/generate_video"
        )

        # Gradio usually returns a file path for the video
        video_path = result[0] if isinstance(result, tuple) else result
        return video_path, None
    except Exception as e:
        return None, f"RUNTIME_ERROR: Ошибка при генерации видео: {e}"