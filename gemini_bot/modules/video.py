import streamlit as st
from gradio_client import Client

@st.cache_resource
def get_video_client():
    try:
        return Client("damo-vilab/modelscope-text-to-video-synthesis")
    except Exception as e:
        return f"Client error: {str(e)}"

def generate_video(prompt: str) -> tuple[str | None, str | None]:
    client = get_video_client()
    if isinstance(client, str):
        return None, f"Ошибка инициализации: {client}"

    try:
        # damo-vilab space expects positional args
        result = client.predict(
            prompt,
            -1,  # seed
            16,  # num_frames
            25,  # num_inference_steps
            api_name="/generate_video"
        )
        # Assuming the first element contains the path, or it's a string
        if isinstance(result, tuple) and len(result) > 0:
            return result[0], None
        elif isinstance(result, dict) and 'video' in result:
             return result['video'], None
        return result, None
    except Exception as e:
        return None, f"Ошибка при генерации видео: {str(e)}"
