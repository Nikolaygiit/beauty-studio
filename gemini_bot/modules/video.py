import streamlit as st
from gradio_client import Client

@st.cache_resource
def get_video_client():
    try:
        return Client("damo-vilab/modelscope-text-to-video-synthesis")
    except Exception as e:
        return f"Ошибка инициализации видео-клиента: {str(e)}"

def generate_video(prompt):
    client = get_video_client()
    if isinstance(client, str): # Error handling
        return client

    try:
        result = client.predict(
                prompt,	# str in 'Input text' Textbox component
                -1,	# float (numeric value between -1 and 2147483647) in 'Seed' Slider component
                25,	# float (numeric value between 10 and 50) in 'Number of inference steps' Slider component
                16,	# float (numeric value between 1 and 30) in 'Number of frames' Slider component
                api_name="/predict"
        )
        return result
    except Exception as e:
        return f"Произошла ошибка при генерации видео: {str(e)}"
