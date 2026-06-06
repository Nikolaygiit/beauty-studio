import streamlit as st
from gradio_client import Client

@st.cache_resource
def get_video_client():
    try:
        return Client("damo-vilab/modelscope-text-to-video-synthesis")
    except Exception as e:
        return f"Ошибка подключения к сервису генерации видео: {str(e)}"

def generate_video(prompt: str) -> tuple[str | None, str | None]:
    """
    Generates video based on the prompt using the Gradio space.
    Returns the file path to the video and an optional error message.
    """
    client = get_video_client()
    if isinstance(client, str):
        return None, client

    try:
        # According to memory, the API expects fixed positional parameters:
        # prompt, seed(-1), num_frames(16), num_inference_steps(25)
        result = client.predict(
            prompt,
            -1,
            16,
            25,
            api_name="/generate_video"
        )

        # Result might be a string (file path) or a tuple
        if isinstance(result, tuple) and len(result) > 0:
            return result[0]['video'] if isinstance(result[0], dict) and 'video' in result[0] else result[0], None
        elif isinstance(result, dict) and 'video' in result:
             return result['video'], None
        return result, None
    except Exception as e:
        return None, f"Ошибка генерации видео: {str(e)}"
