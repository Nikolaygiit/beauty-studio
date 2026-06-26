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
        return None, f"Ошибка инициализации сервиса видео: {str(e)}"

def generate_video(prompt: str, client: Client):
    """
    Generates video using the damo-vilab/modelscope-text-to-video-synthesis Space.
    Returns (video_path, error_message).
    """
    if not client:
        return None, "Клиент видео не инициализирован."

    try:
        result = client.predict(
            prompt,
            -1,  # seed
            16,  # num_frames
            25,  # num_inference_steps
            api_name="/generate_video"
        )
        return result, None
    except ValueError as e:
        return None, f"Ошибка параметров видео: {str(e)}"
    except RuntimeError as e:
        return None, f"Ошибка выполнения видео: {str(e)}"
    except Exception as e:
        return None, f"Неизвестная ошибка при генерации видео: {str(e)}"
