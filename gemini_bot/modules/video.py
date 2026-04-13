import streamlit as st
from gradio_client import Client

@st.cache_resource
def get_video_client():
    """Initializes and caches the Gradio client for video generation."""
    try:
        return Client("damo-vilab/modelscope-text-to-video-synthesis")
    except Exception as e:
        return f"Client Init Error: {e}"

def generate_video(prompt):
    """
    Generates video using the damo-vilab/modelscope-text-to-video-synthesis space.
    """
    client = get_video_client()
    if isinstance(client, str): # Error during initialization
        return None, client

    try:
        result = client.predict(
            prompt,
            -1, # seed
            16, # num_frames
            25, # num_inference_steps
            api_name="/generate_video"
        )
        # result is typically a dictionary containing 'video' key or direct path
        if isinstance(result, dict) and 'video' in result:
             return result['video'], None
        return result, None
    except Exception as e:
        return None, f"Prediction Error: {e}"
