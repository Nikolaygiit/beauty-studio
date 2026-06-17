import streamlit as st
from gradio_client import Client

@st.cache_resource
def get_video_client():
    try:
        return Client("damo-vilab/modelscope-text-to-video-synthesis")
    except Exception as e:
        return None

def generate_video(prompt: str) -> tuple[str | None, str | None]:
    if not prompt:
        return None, "Prompt is required for video generation"

    client = get_video_client()
    if not client:
        return None, "Failed to initialize video generation client"

    try:
        # fixed positional parameters for this specific space
        result = client.predict(
            prompt,
            -1, # seed
            16, # num_frames
            25, # num_inference_steps
            api_name="/generate_video"
        )
        return result, None
    except Exception as e:
        return None, f"Error generating video: {str(e)}"
