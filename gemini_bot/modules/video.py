import streamlit as st
from gradio_client import Client

@st.cache_resource
def get_video_client():
    """
    Инициализирует и кэширует Gradio клиент для генерации видео.
    """
    try:
        client = Client("damo-vilab/modelscope-text-to-video-synthesis")
        return client, ""
    except Exception as e:
        return None, f"Ошибка инициализации видео-клиента: {str(e)}"

def generate_video(prompt: str) -> tuple[str, str]:
    """
    Генерирует видео через damo-vilab/modelscope-text-to-video-synthesis Gradio Space.
    Возвращает (video_path, error_message).
    """
    client, err = get_video_client()
    if err:
        return None, err

    try:
        # Для damo-vilab/modelscope-text-to-video-synthesis используем позиционные аргументы
        # param 0: prompt (str)
        # param 1: seed (int), -1 for random
        # param 2: num_frames (int), 16
        # param 3: num_inference_steps (int), 25
        result = client.predict(
            prompt,
            -1,
            16,
            25,
            api_name="/generate_video"
        )
        # result - кортеж или словарь, в зависимости от API. Обычно строка с путем
        if isinstance(result, dict) and 'video' in result:
            return result['video'], ""
        elif isinstance(result, tuple) and len(result) > 0:
            return result[0], ""
        return result, ""
    except Exception as e:
        return None, f"Ошибка при генерации видео: {str(e)}"
