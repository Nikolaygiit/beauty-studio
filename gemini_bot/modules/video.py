import streamlit as st
from gradio_client import Client

@st.cache_resource
def get_video_client():
    """Initializes and caches the Text-to-Video Gradio client."""
    try:
        return Client("damo-vilab/modelscope-text-to-video-synthesis")
    except Exception as e:
        return str(e) # Returning string error on init failure

def generate_video(prompt: str) -> tuple[str | None, str | None]:
    """
    Generates video based on the prompt using the cached Gradio client.
    Returns (media_path, None) on success, or (None, error_message) on failure.
    """
    client = get_video_client()
    if isinstance(client, str):
        return None, f"Не удалось инициализировать клиент для генерации видео: {client}"
    if client is None:
        return None, "Не удалось инициализировать клиент для генерации видео."

    try:
        # Fixed arguments per memory: prompt, seed, num_frames, num_inference_steps
        result = client.predict(
            prompt,
            -1,
            16,
            25,
            api_name="/generate_video"
        )
        # The result might be a dictionary or tuple depending on gradio output,
        # usually it returns a path to the generated video.
        if isinstance(result, dict) and 'video' in result:
            return result['video'], None
        elif isinstance(result, tuple):
             return result[0], None
        return result, None
    except Exception as e:
        return None, f"Ошибка при генерации видео: {str(e)}"
