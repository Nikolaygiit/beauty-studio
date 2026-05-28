import streamlit as st
from gradio_client import Client

@st.cache_resource(show_spinner=False)
def get_video_client():
    """Returns a cached Gradio Client for video generation."""
    try:
        return Client("damo-vilab/modelscope-text-to-video-synthesis", timeout=60), None
    except Exception as e:
        return None, f"Ошибка подключения к сервису генерации видео: {e}"

def generate_video(prompt: str):
    """Generates video using the damo-vilab/modelscope-text-to-video-synthesis space."""
    client, error = get_video_client()
    if error:
        return None, error

    try:
        # Fixed positional parameters for the /generate_video API: prompt, seed (-1), num_frames (16), num_inference_steps (25)
        result = client.predict(
            prompt,
            -1,
            16,
            25,
            api_name="/generate_video"
        )

        # The API usually returns a string with the file path or a dictionary containing it
        if isinstance(result, str):
            return result, None
        elif isinstance(result, dict) and "video" in result:
             return result["video"], None
        elif isinstance(result, list) and len(result) > 0 and isinstance(result[0], dict) and "video" in result[0]:
             return result[0]["video"], None
        else:
            return None, "Неизвестный формат ответа от сервиса генерации видео."
    except Exception as e:
        return None, f"Ошибка генерации видео: {e}"
