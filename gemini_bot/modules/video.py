import streamlit as st
from gradio_client import Client
from typing import Tuple, Optional

@st.cache_resource
def get_video_client() -> Tuple[Optional[Client], Optional[str]]:
    """
    Initializes and caches the Gradio client for video generation.
    Returns (client, error_message).
    """
    try:
        client = Client("damo-vilab/modelscope-text-to-video-synthesis")
        return client, None
    except Exception as e:
        return None, f"Ошибка инициализации видео-клиента: {str(e)}"

def generate_video(prompt: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Generates video based on the given prompt.
    Returns (video_path, error_message).
    """
    client, err = get_video_client()
    if err:
        return None, err
    if not client:
        return None, "Видео-клиент не инициализирован."

    try:
        # damo-vilab uses fixed positional parameters: prompt, seed, num_frames, num_inference_steps
        result = client.predict(
            prompt,
            -1,  # seed
            16,  # num_frames
            25,  # num_inference_steps
            api_name="/generate_video"
        )

        # Result typically contains the path to the generated video file
        if isinstance(result, tuple) and len(result) > 0:
            video_path = result[0]
            if isinstance(video_path, dict) and 'video' in video_path:
                return video_path['video'], None
            return video_path, None
        elif isinstance(result, dict) and 'video' in result:
             return result['video'], None
        elif isinstance(result, str):
            return result, None
        else:
            return None, "Неизвестный формат ответа от видео-клиента."
    except Exception as e:
        return None, f"Ошибка при генерации видео: {str(e)}"
