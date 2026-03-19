import streamlit as st
from gradio_client import Client

@st.cache_resource
def get_video_client():
    try:
        return Client("damo-vilab/modelscope-text-to-video-synthesis")
    except Exception as e:
        return f"Не удалось инициализировать сервис видео: {e}"

def generate_video(prompt: str) -> str:
    """
    Generates video using damo-vilab/modelscope-text-to-video-synthesis space.
    """
    client_or_error = get_video_client()
    if isinstance(client_or_error, str):
        # It's an error message
        return client_or_error

    try:
        # fixed parameters: seed -1, 16 frames, 25 inference steps based on memory
        result = client_or_error.predict(
            prompt=prompt,
            video_length=16,
            num_inference_steps=25,
            guidance_scale=7.5,
            seed=-1,
            api_name="/generate_video"
        )
        # return path to generated video
        if isinstance(result, tuple) and len(result) > 0:
            return result[0] # Usually the first element is the video file path in output
        return result
    except Exception as e:
        if 'RUNTIME_ERROR' in str(e):
            return "Сервис видео временно недоступен (RUNTIME_ERROR). Пожалуйста, попробуйте позже."
        return f"Ошибка генерации видео: {e}"
