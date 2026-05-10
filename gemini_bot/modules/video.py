import streamlit as st
from gradio_client import Client

@st.cache_resource
def get_video_client():
    """Initializes and caches the gradio client for video generation."""
    try:
        return Client("damo-vilab/modelscope-text-to-video-synthesis")
    except Exception as e:
        return None

def generate_video(prompt):
    """
    Generates video using the damo-vilab/modelscope-text-to-video-synthesis space.
    Returns a tuple of (video_path, error_message).
    """
    client = get_video_client()
    if not client:
        return None, "Failed to initialize video generation client."

    try:
        result = client.predict(
            prompt,
            -1,
            16,
            25,
            api_name="/generate_video"
        )
        # Check if the result is a dict containing 'video' key (Gradio file representation)
        if isinstance(result, dict) and 'video' in result:
             return result['video'], None
        elif isinstance(result, str):
             # Sometimes it directly returns the file path
             return result, None
        elif isinstance(result, tuple) and len(result) > 0 and isinstance(result[0], dict) and 'video' in result[0]:
             return result[0]['video'], None
        else:
            return result, None

    except Exception as e:
        return None, f"Error generating video: {e}"
