import streamlit as st
from gradio_client import Client

@st.cache_resource(show_spinner=False)
def get_video_client():
    try:
        return Client("damo-vilab/modelscope-text-to-video-synthesis")
    except Exception as e:
        return str(e)

def generate_video(prompt: str):
    client = get_video_client()
    if isinstance(client, str):
        return None, f"Ошибка инициализации генератора видео: {client}"

    try:
        # fixed positional parameters: prompt, seed, num_frames, num_inference_steps
        result = client.predict(
            prompt,
            -1,
            16,
            25,
            api_name="/generate_video"
        )
        # return result path (video_path)
        if isinstance(result, tuple) and len(result) > 0:
            return result[0], None
        return result, None
    except Exception as e:
        return None, f"Ошибка при генерации видео: {e}"
