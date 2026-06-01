import streamlit as st
from gradio_client import Client

@st.cache_resource
def get_video_client():
    """
    Initializes and caches the Gradio client for video generation.
    Returns (client, None) or (None, error_message).
    """
    try:
        client = Client("damo-vilab/modelscope-text-to-video-synthesis")
        return client, None
    except Exception as e:
        return None, f"Failed to initialize video generation client: {str(e)}"

def generate_video(prompt: str):
    """
    Generates video using the damo-vilab space.
    Returns (video_path, None) or (None, error_message).
    """
    client, err = get_video_client()
    if err:
        return None, err

    try:
        # Based on memory, use /generate_video API endpoint with fixed positional params:
        # prompt, -1 (seed), 16 (num_frames), 25 (num_inference_steps)
        result = client.predict(
            prompt,
            -1,
            16,
            25,
            api_name="/generate_video"
        )

        # Result is usually a path to the generated video or a tuple
        if isinstance(result, tuple) or isinstance(result, list):
            # Sometimes Gradio returns a dict with 'video' path inside tuple
            if isinstance(result[0], dict) and 'video' in result[0]:
                return result[0]['video'], None
            return result[0], None

        return result, None
    except Exception as e:
        return None, f"Error generating video: {str(e)}"
