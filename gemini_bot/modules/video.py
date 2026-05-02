from gradio_client import Client
import streamlit as st

@st.cache_resource
def get_video_client():
    """Caches the Gradio Client initialization for the video model."""
    try:
        return Client("damo-vilab/modelscope-text-to-video-synthesis")
    except Exception as e:
        return str(e)

def generate_video(prompt: str) -> tuple[str, str]:
    """
    Generates video using damo-vilab/modelscope-text-to-video-synthesis via Gradio.
    Returns a tuple of (video_file_path_or_url, error_message).
    """
    client = get_video_client()

    if isinstance(client, str):
         return None, f"Ошибка инициализации генератора видео: {client}"

    try:
        # Based on typical usage for this gradio space
        # predict passes positional params for the /generate_video endpoint
        # prompt, seed, num_frames, num_inference_steps
        result = client.predict(
            prompt,
            -1,  # seed
            16,  # num_frames
            25,  # num_inference_steps
            api_name="/generate_video"
        )
        return result, None
    except Exception as e:
        return None, f"Ошибка при генерации видео: {str(e)}"
