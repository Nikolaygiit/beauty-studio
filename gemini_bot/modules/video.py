import streamlit as st
from gradio_client import Client
import os

@st.cache_resource
def get_video_client():
    try:
        return Client("damo-vilab/modelscope-text-to-video-synthesis")
    except Exception as e:
        return f"RUNTIME_ERROR: {str(e)}"

def generate_video(prompt):
    """
    Generates video using the modelscope space via Gradio Client.
    """
    client = get_video_client()

    if isinstance(client, str):
        return None, client

    try:
        result = client.predict(
            prompt,
            -1, # seed
            16, # num_frames
            25, # num_inference_steps
            api_name="/generate_video"
        )

        video_path = None
        if isinstance(result, str):
            video_path = result
        elif isinstance(result, (list, tuple)) and len(result) > 0:
            if isinstance(result[0], str):
                video_path = result[0]
            elif isinstance(result[0], dict) and 'video' in result[0]:
                video_path = result[0]['video']
            elif isinstance(result[0], dict) and 'name' in result[0]:
                video_path = result[0]['name']
        elif isinstance(result, dict):
            if 'video' in result:
                video_path = result['video']
            elif 'name' in result:
                video_path = result['name']

        if video_path and os.path.exists(video_path):
             return video_path, None

        return result, None

    except Exception as e:
        return None, f"RUNTIME_ERROR: {str(e)}"
