import streamlit as st
from gradio_client import Client

@st.cache_resource(show_spinner="Инициализация модели видео...")
def get_video_client():
    """
    Initializes and caches the Gradio client for video generation.
    """
    try:
        return Client("damo-vilab/modelscope-text-to-video-synthesis")
    except Exception as e:
        return str(e)

def generate_video(prompt: str) -> tuple[str | None, str | None]:
    """
    Generates video using the damo-vilab/modelscope-text-to-video-synthesis space.
    Returns (video_path, error_message).
    """
    client = get_video_client()
    if isinstance(client, str):
        return None, f"Ошибка инициализации клиента: {client}"

    try:
        result = client.predict(
            prompt,
            -1,  # seed
            16,  # num_frames
            25,  # num_inference_steps
            api_name="/generate_video"
        )

        # Result typically contains a path or dictionary with the path
        if isinstance(result, tuple) or isinstance(result, list):
            return result[0], None
        elif isinstance(result, dict) and 'video' in result:
            return result['video'], None
        return result, None
    except (ValueError, RuntimeError, Exception) as e:
        return None, f"Ошибка генерации видео: {str(e)}"
