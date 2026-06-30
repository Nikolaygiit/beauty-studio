import streamlit as st
from gradio_client import Client
import traceback

@st.cache_resource
def get_video_client():
    """
    Initializes and returns the Gradio Client for text-to-video-synthesis.
    Returns (client, error_message).
    """
    try:
        client = Client("damo-vilab/modelscope-text-to-video-synthesis")
        return client, None
    except Exception as e:
        return None, f"Error initializing video client: {e}"

def generate_video(prompt: str) -> tuple[str, str]:
    """
    Generates video based on the prompt using Gradio text-to-video-synthesis space.
    Returns (media_path, error_message).
    """
    client, error = get_video_client()
    if error:
        return None, error

    try:
        result = client.predict(
            prompt, # prompt
            -1,     # seed
            16,     # num_frames
            25,     # num_inference_steps
            api_name="/generate_video"
        )
        return result, None
    except Exception as e:
        traceback.print_exc()
        return None, f"Error generating video: {e}"
