import streamlit as st
from gradio_client import Client

@st.cache_resource
def get_video_client():
    """
    Returns a cached Gradio client for video generation.
    """
    try:
        return Client("damo-vilab/modelscope-text-to-video-synthesis")
    except Exception as e:
        return f"Error initializing video client: {str(e)}"

def generate_video(prompt: str) -> tuple[str | None, str | None]:
    """
    Generates video using the Gradio API.
    Returns a tuple (video_path, error_message).
    """
    client = get_video_client()
    if isinstance(client, str):
        return None, client

    try:
        result = client.predict(
            prompt,
            -1, # seed
            16, # num_frames
            25, # num_inference_steps
            api_name="/generate_video"
        )
        return result, None
    except ValueError as e:
        return None, f"Ошибка данных генерации видео: {str(e)}"
    except RuntimeError as e:
        return None, f"Ошибка выполнения генерации видео: {str(e)}"
    except Exception as e:
        return None, f"Неизвестная ошибка генерации видео: {str(e)}"
