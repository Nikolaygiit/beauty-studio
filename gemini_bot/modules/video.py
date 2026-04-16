import streamlit as st
from gradio_client import Client

@st.cache_resource
def get_video_client():
    """Initializes and caches the Video Gradio client."""
    try:
        return Client("damo-vilab/modelscope-text-to-video-synthesis")
    except Exception as e:
        return f"Error initializing video client: {e}"

def generate_video(client, prompt):
    """Generates video using the Text-to-Video Synthesis client."""
    if isinstance(client, str): # Error during initialization
        return client

    try:
        result = client.predict(
            prompt,
            -1,  # seed
            16,  # num_frames
            25,  # num_inference_steps
            api_name="/generate_video"
        )
        return result
    except Exception as e:
        return f"Error generating video: {e}"
