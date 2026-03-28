import streamlit as st
from gradio_client import Client

@st.cache_resource
def get_video_client():
    """
    Initialize and cache the Gradio client for Text-to-Video.
    """
    try:
        return Client("damo-vilab/modelscope-text-to-video-synthesis")
    except Exception as e:
        return f"Ошибка при инициализации VideoGen клиента: {str(e)}"

def generate_video(prompt):
    """
    Generate video using Damo ViLab's text-to-video synthesis.
    Fixed parameters: seed=-1, num_frames=16, num_inference_steps=25.
    """
    client = get_video_client()

    if isinstance(client, str):
        # Client initialization failed and returned error string
        return client

    try:
        # Generate video using the gradio API endpoint
        result = client.predict(
            prompt,	# str in 'text' Textbox component
            -1,	# float (numeric value between -1 and 2147483647) in 'Seed' Slider component
            16,	# float (numeric value between 16 and 16) in 'Number of Frames' Slider component
            25,	# float (numeric value between 10 and 50) in 'Number of Inference Steps' Slider component
            api_name="/generate"
        )
        return result
    except Exception as e:
        return f"Ошибка при генерации видео: {str(e)}"
