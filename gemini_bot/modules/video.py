import streamlit as st
from gradio_client import Client

@st.cache_resource
def get_video_client():
    try:
        return Client("damo-vilab/modelscope-text-to-video-synthesis")
    except Exception as e:
        return f"Ошибка инициализации клиента видео: {str(e)}"

def generate_video(prompt):
    client = get_video_client()
    if isinstance(client, str):
        return None, client

    try:
        result = client.predict(
            prompt,
            -1, # seed
            16, # num_frames
            25, # num_inference_steps
            api_name="/generate_video"
        )
        return result, None
    except ValueError as ve:
        return None, f"Ошибка значений видео генератора: {str(ve)}"
    except RuntimeError as re:
        return None, f"Ошибка среды выполнения видео: {str(re)}"
    except Exception as e:
        return None, f"Неизвестная ошибка при генерации видео: {str(e)}"
