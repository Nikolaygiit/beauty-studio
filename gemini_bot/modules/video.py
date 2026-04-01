import streamlit as st
from gradio_client import Client

@st.cache_resource
def get_video_client():
    try:
         return Client("damo-vilab/modelscope-text-to-video-synthesis")
    except Exception as e:
         return f"Ошибка инициализации: {str(e)}"

def generate_video(prompt):
    client = get_video_client()
    if isinstance(client, str):
         return client

    try:
         # damo-vilab space expects prompt, seed, num_frames, num_inference_steps
         result = client.predict(
            prompt,
            -1,  # seed
            16,  # num_frames
            25,  # num_inference_steps
            api_name="/video"
         )
         return result
    except Exception as e:
         return f"Ошибка при генерации видео: {str(e)}"
