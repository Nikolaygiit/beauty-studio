import streamlit as st
from gradio_client import Client

@st.cache_resource(show_spinner=False)
def get_video_client():
    try:
        return Client("damo-vilab/modelscope-text-to-video-synthesis")
    except Exception as e:
        error_msg = str(e)
        if "RUNTIME_ERROR" in error_msg:
            return "Генерация видео недоступна: сервис временно не работает (RUNTIME_ERROR)."
        print(f"Error initializing video client: {e}")
        return f"Ошибка инициализации видео-сервиса: {e}"

def generate_video(prompt):
    """
    Generates video using the damo-vilab/modelscope-text-to-video-synthesis space.
    """
    client = get_video_client()

    if isinstance(client, str):
        # This means an error occurred during initialization (e.g. RUNTIME_ERROR)
        return client

    if not client:
        return "Не удалось подключиться к видео-сервису."

    try:
        # Configuration: seed=-1, num_frames=16, num_inference_steps=25
        result = client.predict(
            prompt,
            -1,  # seed
            16,  # num_frames
            25,  # num_inference_steps
            api_name="/video_synthesis"
        )
        # Assuming result contains the filepath to the video
        return result
    except Exception as e:
        error_msg = str(e)
        if "RUNTIME_ERROR" in error_msg:
            return "Генерация видео недоступна: сервис временно не работает (RUNTIME_ERROR)."
        print(f"Error generating video: {e}")
        return f"Ошибка генерации видео: {e}"
