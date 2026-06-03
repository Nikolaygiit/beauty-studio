import streamlit as st
from gradio_client import Client

@st.cache_resource
def get_video_client():
    """
    Initializes and caches the Gradio client for Video Generation.
    """
    try:
        return Client("damo-vilab/modelscope-text-to-video-synthesis")
    except Exception as e:
        return f"Ошибка инициализации генератора видео: {str(e)}"

def generate_video(prompt: str) -> tuple[str | None, str | None]:
    """
    Generates video using the damo-vilab/modelscope-text-to-video-synthesis Gradio Space.
    Returns (video_path, error_message).
    """
    client = get_video_client()
    if isinstance(client, str): # Error message returned
        return None, client

    try:
        # Expected positional parameters: prompt, seed, num_frames, num_inference_steps
        result = client.predict(
            prompt,
            -1,  # seed
            16,  # num_frames
            25,  # num_inference_steps
            api_name="/generate_video"
        )

        # Result typically includes path to a generated file, sometimes as tuple
        if isinstance(result, tuple):
            video_path = result[0]
        else:
            video_path = result

        # The space returns a dictionary with 'video' containing the path in some cases
        if isinstance(video_path, dict) and 'video' in video_path:
             video_path = video_path['video']

        return video_path, None
    except Exception as e:
        return None, f"Ошибка генерации видео: {str(e)}"
