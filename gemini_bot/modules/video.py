import streamlit as st
from gradio_client import Client

@st.cache_resource
def get_video_client_cached():
    return Client("damo-vilab/modelscope-text-to-video-synthesis")

def get_video_client():
    try:
        return get_video_client_cached()
    except Exception as e:
        return f"**Ошибка инициализации генератора видео:** {e}"

def generate_video(prompt):
    """Generates video using ModelScope Text-to-Video Synthesis."""
    try:
        client = get_video_client()

        # Checking if client initialization returned an error string
        if isinstance(client, str):
            # Clear cache if initialization failed to retry later
            get_video_client_cached.clear()
            return client

        result = client.predict(
            prompt,	# str in 'Prompt' Textbox component
            -1,	# int | float (numeric value between -1 and 2147483647) in 'Seed' Slider component
            25,	# int | float (numeric value between 10 and 50) in 'Num inference steps' Slider component
            16,	# int | float (numeric value between 8 and 32) in 'Num frames' Slider component
            api_name="/predict"
        )
        return result
    except Exception as e:
        return f"**Ошибка при генерации видео:** {e}"
