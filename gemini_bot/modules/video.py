import streamlit as st
from gradio_client import Client

@st.cache_resource(show_spinner=False)
def get_video_client():
    try:
        return Client("damo-vilab/modelscope-text-to-video-synthesis")
    except Exception as e:
        return str(e)

def generate_video(prompt: str):
    """
    Generates video using damo-vilab/modelscope-text-to-video-synthesis.
    """
    client = get_video_client()
    if isinstance(client, str):
        return f"Error initializing video client: {client}"

    try:
        # For modelscope-text-to-video-synthesis API based on gradio version
        result = client.predict(
            prompt,
            -1, # seed
            16, # num_frames
            25, # num_inference_steps
            api_name="/generate_video"
        )
        return result
    except Exception as e:
        if "RUNTIME_ERROR" in str(e):
            return "RUNTIME_ERROR: The video generation service is currently unavailable or busy. Please try again later."
        return f"Error generating video: {str(e)}"
