import streamlit as st
from gradio_client import Client

@st.cache_resource
def get_video_client():
    try:
        return Client("damo-vilab/modelscope-text-to-video-synthesis")
    except Exception as e:
        return f"Ошибка загрузки модели видео: {e}"

def generate_video(prompt, client):
    try:
        if isinstance(client, str):
            return client
        result = client.predict(
            prompt,
            -1, # seed
            16, # frames
            25, # inference steps
            api_name="/predict"
        )
        return result
    except Exception as e:
        return f"Ошибка генерации видео: {e}"
