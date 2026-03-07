import streamlit as st
from gradio_client import Client

@st.cache_resource
def get_video_client():
    try:
        return Client("damo-vilab/modelscope-text-to-video-synthesis")
    except Exception as e:
        return str(e)

def generate_video(prompt, client):
    if isinstance(client, str):
         return f"Ошибка инициализации Video API: {client}"

    try:
        # Expected parameters based on typical implementations, handling RUNTIME_ERROR gracefully.
        result = client.predict(
            prompt,
            -1,  # seed
            16,  # num frames
            25,  # num inference steps
            api_name="/predict"
        )
        return result
    except Exception as e:
        return f"Ошибка генерации видео: {e}"
