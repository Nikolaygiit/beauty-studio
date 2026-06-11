import streamlit as st
from gradio_client import Client

@st.cache_resource
def get_video_client() -> Client | str:
    """
    Initializes and caches the Gradio client for video generation.
    Returns the client or an error string if initialization fails.
    """
    try:
        return Client("damo-vilab/modelscope-text-to-video-synthesis")
    except Exception as e:
        return f"Ошибка инициализации видео-клиента: {str(e)}"

def generate_video(prompt: str) -> tuple[str | None, str | None]:
    """
    Generates video using the Gradio client.
    Returns (video_path, error_message)
    """
    client = get_video_client()
    if isinstance(client, str):
        return None, client

    try:
        result = client.predict(
            prompt,
            -1,  # seed
            16,  # num_frames
            25,  # num_inference_steps
            api_name="/generate_video"
        )

        # Gradio usually returns a dictionary with 'video' key for the filepath
        # or the direct filepath depending on the space version.
        video_path = result.get('video') if isinstance(result, dict) else result
        # if the result is a tuple, the video is likely the first element
        if isinstance(result, tuple):
            video_path = result[0].get('video') if isinstance(result[0], dict) else result[0]

        return video_path, None
    except Exception as e:
        return None, f"Ошибка генерации видео: {str(e)}"
