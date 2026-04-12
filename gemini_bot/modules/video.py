import streamlit as st
from gradio_client import Client

@st.cache_resource
def get_video_client():
    """Initializes and caches the gradio client for video generation."""
    try:
        return Client("damo-vilab/modelscope-text-to-video-synthesis")
    except Exception as e:
        return f"Error initializing video client (RUNTIME_ERROR or other): {e}"

def generate_video(prompt):
    """
    Generates video using the damo-vilab/modelscope-text-to-video-synthesis space.
    Uses the /generate_video API endpoint with positional arguments.
    """
    client = get_video_client()
    if isinstance(client, str):
        return client, None # return error message

    try:
        # Fixed positional parameters for the /generate_video API: prompt, -1 (seed), 16 (num_frames), 25 (num_inference_steps)
        result = client.predict(
            prompt,
            -1,
            16,
            25,
            api_name="/generate_video"
        )
        return None, result # return None error, result video path
    except Exception as e:
        return f"Error generating video (RUNTIME_ERROR or other): {e}", None
