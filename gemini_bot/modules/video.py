import streamlit as st
from gradio_client import Client

@st.cache_resource
def get_video_client():
    """Initializes and caches the Gradio client for video generation."""
    try:
        return Client("damo-vilab/modelscope-text-to-video-synthesis")
    except Exception as e:
        return f"RUNTIME_ERROR: {str(e)}"

def generate_video(client, prompt):
    """
    Generates video using the damo-vilab/modelscope-text-to-video-synthesis space.
    """
    if isinstance(client, str) and "RUNTIME_ERROR" in client:
        return None, client # Return error string

    try:
        # fixed positional parameters: prompt, seed, num_frames, num_inference_steps
        result = client.predict(
            prompt,
            -1,
            16,
            25,
            api_name="/generate_video"
        )
        return result, None
    except Exception as e:
        return None, f"RUNTIME_ERROR: {str(e)}"
