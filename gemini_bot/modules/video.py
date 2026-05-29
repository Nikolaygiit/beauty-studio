import streamlit as st
from gradio_client import Client

@st.cache_resource
def get_video_client():
    try:
        return Client("damo-vilab/modelscope-text-to-video-synthesis")
    except Exception as e:
        return f"Ошибка инициализации видео-клиента: {str(e)}"

def generate_video(prompt: str) -> tuple[str | None, str | None]:
    """
    Generates video using Gradio Client.
    Returns: (media_path, error_message)
    """
    client = get_video_client()

    if isinstance(client, str):
        return None, client

    try:
        # According to memory: prompt, -1 (seed), 16 (num_frames), and 25 (num_inference_steps)
        result = client.predict(
            prompt,
            -1,
            16,
            25,
            api_name="/generate_video"
        )
        # The API returns a dictionary with 'video' as key to a tuple of (path, name)
        # Or just a path depending on gradio client version.
        # Usually it returns the file path.
        if isinstance(result, dict) and 'video' in result:
             return result['video'], None
        return result, None
    except Exception as e:
        return None, f"Ошибка при генерации видео: {str(e)}"
