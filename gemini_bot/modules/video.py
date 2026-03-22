import streamlit as st
from gradio_client import Client

@st.cache_resource(show_spinner=False)
def get_video_client():
    """
    Caches the Gradio Client for video generation.
    Gracefully handles RUNTIME_ERROR and standard exceptions.
    """
    try:
        # Default space: damo-vilab/modelscope-text-to-video-synthesis
        return Client("damo-vilab/modelscope-text-to-video-synthesis")
    except ValueError as ve:
        # Happens if space is in RUNTIME_ERROR
        return f"Сервис видео генерации временно недоступен: {ve}"
    except Exception as e:
        return f"Ошибка загрузки клиента видео: {e}"

def generate_video(prompt: str) -> str:
    """Generates a video given a text prompt."""
    client = get_video_client()
    if isinstance(client, str):
        return client # Return the error message string

    try:
        # Hardcoded parameters according to memory context:
        # seed=-1, num_frames=16, num_inference_steps=25
        result = client.predict(
            prompt,	# str in 'text' Textbox component
            -1,	# float (numeric value between -1 and 2147483647) in 'Seed' Slider component
            16,	# float (numeric value between 16 and 16) in 'Number of Frames' Slider component
            25,	# float (numeric value between 10 and 50) in 'Number of Inference Steps' Slider component
            api_name="/video_synthesis"
        )
        # Returns the filepath
        return result
    except Exception as e:
        return f"Произошла ошибка при генерации видео: {e}"
