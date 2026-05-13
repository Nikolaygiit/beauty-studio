from gradio_client import Client
import streamlit as st

@st.cache_resource(show_spinner=False)
def get_video_client():
    """Returns a cached instance of the Gradio client for text-to-video."""
    try:
        return Client("damo-vilab/modelscope-text-to-video-synthesis")
    except (ValueError, RuntimeError, Exception) as e:
        return f"Failed to initialize Video client: {e}"

def generate_video(prompt):
    """
    Generates video using the damo-vilab/modelscope-text-to-video-synthesis Gradio client.
    Returns (video_path, error_message).
    """
    client = get_video_client()
    if isinstance(client, str): # Error during initialization
         return None, client
    if client is None:
         return None, "Video client initialization failed."

    try:
        # Fixed positional parameters as per memory: prompt, seed (-1), num_frames (16), num_inference_steps (25)
        result = client.predict(
            prompt,
            -1,
            16,
            25,
            api_name="/generate_video"
        )
        return result, None
    except (ValueError, RuntimeError, Exception) as e:
        return None, f"Failed to generate video: {e}"
