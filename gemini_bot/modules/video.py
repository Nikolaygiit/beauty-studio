from gradio_client import Client
import streamlit as st

@st.cache_resource
def get_video_client():
    """Initializes and caches the Gradio client for video generation."""
    try:
        return Client("damo-vilab/modelscope-text-to-video-synthesis")
    except Exception as e:
        return f"Ошибка инициализации видео-генератора: {e}"

def generate_video(prompt: str) -> tuple[str | None, str | None]:
    """
    Generates video using the Gradio Space 'damo-vilab/modelscope-text-to-video-synthesis'.
    Returns (path_to_video, error_message).
    """
    client = get_video_client()

    if isinstance(client, str):
        # Client initialization failed and returned an error string
        return None, client

    try:
        # Note: Using positional arguments based on memory constraints.
        result = client.predict(
            prompt, # prompt
            -1,     # seed
            16,     # num_frames
            25,     # num_inference_steps
            api_name="/generate_video"
        )
        # result is typically a tuple or path to the video file
        video_path = result[0] if isinstance(result, (list, tuple)) else result

        # sometimes gradio returns dict with video structure
        if isinstance(video_path, dict) and 'video' in video_path:
             video_path = video_path['video']

        return video_path, None
    except Exception as e:
        return None, f"Ошибка при генерации видео: {e}"
