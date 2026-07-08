import streamlit as st
from gradio_client import Client

@st.cache_resource
def get_video_client():
    """
    Initializes and caches the Gradio client for video generation.
    Returns (client, error_message).
    """
    try:
        client = Client("damo-vilab/modelscope-text-to-video-synthesis")
        return client, None
    except Exception as e:
        return None, f"Failed to initialize video client: {e}"

def generate_video(prompt: str):
    """
    Generates video using the cached text-to-video-synthesis model.
    Uses positional parameters for the /generate_video API.
    Returns (media_path, error_message).
    """
    if not prompt:
        return None, "Prompt cannot be empty"

    client, err = get_video_client()
    if err:
        return None, err

    try:
        # The API requires positional arguments: prompt, seed, num_frames, num_inference_steps
        result = client.predict(
            prompt,
            -1,   # seed
            16,   # num_frames
            25,   # num_inference_steps
            api_name="/generate_video"
        )
        return result, None
    except Exception as e:
        return None, str(e)
