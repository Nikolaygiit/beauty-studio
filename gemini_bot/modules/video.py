import streamlit as st
from gradio_client import Client

@st.cache_resource(show_spinner=False)
def get_video_client():
    """
    Initializes and caches the gradio client for modelscope-text-to-video-synthesis.
    """
    try:
        client = Client("damo-vilab/modelscope-text-to-video-synthesis")
        return client
    except Exception as e:
        return f"Error initializing video client: {e}"

def generate_video(client, prompt):
    """
    Generates video given a prompt using fixed parameters.
    Handles RUNTIME_ERROR and returns the result or an error message.
    """
    if isinstance(client, str):
        return None, client # Return error string

    try:
        result = client.predict(
            prompt=prompt,
            seed=-1,
            num_frames=16,
            num_inference_steps=25,
            api_name="/predict"
        )
        return result, None
    except Exception as e:
        return None, f"Runtime error generating video: {e}"
