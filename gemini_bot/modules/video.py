import streamlit as st
from gradio_client import Client

@st.cache_resource
def get_video_client():
    try:
        return Client("damo-vilab/modelscope-text-to-video-synthesis")
    except Exception as e:
        return f"Ошибка инициализации клиента: {str(e)}"

def generate_video(prompt: str) -> tuple[str | None, str | None]:
    """Generates video using the Gradio client and returns (file_path, error_message)."""
    try:
        client = get_video_client()
        if isinstance(client, str):
            return None, client

        result = client.predict(
            prompt,
            -1,
            16,
            25,
            api_name="/generate_video"
        )
        return result, None
    except Exception as e:
        return None, f"Ошибка при генерации видео: {str(e)}"
