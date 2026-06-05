import streamlit as st
from gradio_client import Client

@st.cache_resource(show_spinner=False)
def get_video_client():
    """Returns a cached Gradio client for modelscope-text-to-video-synthesis."""
    try:
        return Client("damo-vilab/modelscope-text-to-video-synthesis")
    except Exception as e:
        return None

def generate_video(prompt: str) -> tuple[str | None, str | None]:
    """
    Generates video using the damo-vilab/modelscope-text-to-video-synthesis Gradio Space.
    Returns (video_path, error_message).
    """
    client = get_video_client()
    if not client:
        return None, "Не удалось инициализировать клиент для генерации видео."

    try:
        # Expected arguments: prompt, seed, num_frames, num_inference_steps
        result = client.predict(
            prompt,
            -1,
            16,
            25,
            api_name="/generate_video"
        )

        # The result is expected to be a tuple with the video path
        if isinstance(result, tuple) and len(result) > 0:
             return result[0]['video'], None
        elif isinstance(result, dict) and 'video' in result:
             return result['video'], None
        elif isinstance(result, str):
             return result, None
        else:
             return None, "Неизвестный формат ответа от сервера."
    except Exception as e:
        return None, f"Ошибка при генерации видео: {e}"
