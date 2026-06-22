from gradio_client import Client
import streamlit as st

@st.cache_resource
def get_video_client():
    """Initializes and caches the Gradio client for video generation."""
    try:
        return Client("damo-vilab/modelscope-text-to-video-synthesis")
    except Exception as e:
        return None

def generate_video(prompt: str) -> tuple[str | None, str | None]:
    """
    Generates video using the damo-vilab/modelscope-text-to-video-synthesis Gradio client.
    Returns a tuple of (video_path, error_message).
    """
    client = get_video_client()
    if not client:
        return None, "Ошибка инициализации клиента генерации видео."

    try:
        result = client.predict(
            prompt,
            -1,  # seed
            16,  # num_frames
            25,  # num_inference_steps
            api_name="/generate_video"
        )
        return result, None
    except Exception as e:
        return None, f"Ошибка при генерации видео: {str(e)}"
