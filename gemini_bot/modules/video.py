from gradio_client import Client
import streamlit as st

@st.cache_resource
def get_video_client():
    try:
        return Client("damo-vilab/modelscope-text-to-video-synthesis")
    except Exception as e:
        return None

def generate_video(prompt):
    """
    Generates video using damo-vilab/modelscope-text-to-video-synthesis space.
    Returns (video_path, error_message).
    """
    client = get_video_client()
    if client is None:
        return None, "Ошибка: Не удалось инициализировать клиент для генерации видео. Возможно, сервис недоступен (RUNTIME_ERROR)."

    try:
        # fixed positional parameters
        result = client.predict(
            prompt,  # prompt
            -1,      # seed
            16,      # num_frames
            25,      # num_inference_steps
            api_name="/generate_video"
        )
        if isinstance(result, tuple):
             return result[0], None
        return result, None
    except Exception as e:
        if "RUNTIME_ERROR" in str(e):
            return None, "Ошибка выполнения на сервере генерации видео (RUNTIME_ERROR). Пожалуйста, попробуйте позже."
        return None, f"Ошибка генерации видео: {str(e)}"
