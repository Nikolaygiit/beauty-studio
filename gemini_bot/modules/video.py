import streamlit as st
from gradio_client import Client

@st.cache_resource
def get_video_client():
    """Initialize and cache the video generation client."""
    try:
        return Client("damo-vilab/modelscope-text-to-video-synthesis")
    except Exception as e:
        return str(e)

def generate_video(prompt: str):
    """
    Generates video using the damo-vilab/modelscope-text-to-video-synthesis space.
    Returns (video_path, error_message).
    """
    client_or_error = get_video_client()
    if isinstance(client_or_error, str):
        return None, f"Error initializing video client: {client_or_error}"

    try:
        client = client_or_error
        # Parameters based on memory for /generate_video API
        # prompt, seed, num_frames, num_inference_steps
        result = client.predict(
            prompt,
            -1,
            16,
            25,
            api_name="/generate_video"
        )
        # The result returns a dictionary with 'video' as the key to the path,
        # or just the path depending on gradio_client version, we will handle path.
        video_path = result.get("video") if isinstance(result, dict) else result
        return video_path, None
    except Exception as e:
        return None, f"Error generating video: {e}"
