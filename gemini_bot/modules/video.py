import streamlit as st
from gradio_client import Client

@st.cache_resource
def get_video_client():
    """Initializes and caches the Text-to-Video Gradio client."""
    try:
        return Client("damo-vilab/modelscope-text-to-video-synthesis")
    except Exception as e:
        return None, f"Failed to initialize Video client: {e}"

def generate_video(prompt):
    """Generates video from a text prompt using modelscope."""
    client = get_video_client()

    # If get_video_client returned a tuple, it means an error occurred
    if isinstance(client, tuple):
        return None, client[1]

    try:
        result = client.predict(
            prompt,
            -1,  # seed
            16,  # num_frames
            25,  # num_inference_steps
            api_name="/generate_video"
        )
        # The result from Gradio for a video file is usually the local file path
        # It's returned as a dictionary, so we need to extract the video path
        if isinstance(result, dict) and 'video' in result:
             return result['video'], None
        elif isinstance(result, str):
            return result, None
        elif isinstance(result, tuple) and len(result) > 0:
             return result[0], None
        else:
            return result, None # fallback

    except Exception as e:
        return None, f"Error generating video: {e}"
