import streamlit as st
from gradio_client import Client

@st.cache_resource
def get_video_client():
    try:
        return Client("damo-vilab/modelscope-text-to-video-synthesis")
    except Exception as e:
        if "RUNTIME_ERROR" in str(e):
            return "ОШИБКА: Пространство временно недоступно (RUNTIME_ERROR)."
        return str(e)

def generate_video(prompt):
    client = get_video_client()
    if isinstance(client, str):
        return None, client
    if not client:
        return None, "Не удалось подключиться к сервису генерации видео."

    try:
        # damo-vilab/modelscope-text-to-video-synthesis uses positional arguments
        # The exact order: prompt, seed, num_frames, num_inference_steps
        result = client.predict(
            prompt,
            -1,  # seed
            16,  # num_frames
            25,  # num_inference_steps
            api_name="/generate_video"
        )
        return result, None
    except Exception as e:
        if "RUNTIME_ERROR" in str(e):
            return None, "ОШИБКА: Пространство временно недоступно (RUNTIME_ERROR)."
        return None, f"Ошибка при генерации видео: {str(e)}"
