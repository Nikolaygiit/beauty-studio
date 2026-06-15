import streamlit as st
from gradio_client import Client

@st.cache_resource
def get_video_client():
    """
    Initializes and caches the Gradio client for video generation.
    """
    try:
        return Client("damo-vilab/modelscope-text-to-video-synthesis")
    except Exception as e:
        return f"Ошибка при подключении к сервису видео: {str(e)}"

def generate_video(prompt: str) -> tuple[str | None, str | None]:
    """
    Generates video using the damo-vilab/modelscope-text-to-video-synthesis Gradio Space.
    Returns a tuple of (video_path, error_message).
    """
    client = get_video_client()
    if isinstance(client, str):
        return None, client # Return the initialization error message

    try:
        # The API requires positional arguments: prompt, seed, num_frames, num_inference_steps
        result = client.predict(
            prompt,
            -1,
            16,
            25,
            api_name="/generate_video"
        )

        # The API returns a dictionary containing a 'video' key with the path
        if result and isinstance(result, dict) and 'video' in result:
            return result['video'], None
        elif isinstance(result, str):
            # Sometimes it might return the path directly depending on client version
            return result, None
        else:
            return None, "Неизвестный формат ответа от сервиса видео."

    except Exception as e:
        return None, f"Ошибка при генерации видео: {str(e)}"
