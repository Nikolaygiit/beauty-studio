import streamlit as st
from gradio_client import Client

@st.cache_resource
def get_video_client():
    """Caches the initialization of the Gradio video client."""
    try:
        return Client("damo-vilab/modelscope-text-to-video-synthesis")
    except Exception as e:
         return f"Error initializing video client: {e}"

def generate_video(prompt):
    """Generates video using the damo-vilab/modelscope-text-to-video-synthesis space."""
    client = get_video_client()

    if isinstance(client, str):
         return None, client # Return error string

    try:
        result = client.predict(
            prompt,
            -1,	# seed
            16,	# num_frames
            25,	# num_inference_steps
            api_name="/generate_video"
        )
        return result, None # Result is a tuple with paths, usually first element is the video
    except Exception as e:
        if "RUNTIME_ERROR" in str(e):
             return None, f"Video generation runtime error (Space might be busy): {e}"
        return None, f"Error generating video: {e}"
