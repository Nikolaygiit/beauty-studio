from gradio_client import Client
import streamlit as st

@st.cache_resource
def get_video_client():
    try:
        return Client("damo-vilab/modelscope-text-to-video-synthesis")
    except Exception as e:
        return f"Error initializing video client: {e}"

def generate_video(prompt):
    client = get_video_client()
    if isinstance(client, str):
        return client

    try:
        result = client.predict(
            prompt,
            -1,  # seed
            25,  # inference steps
            16,  # num frames
            api_name="/text2video"
        )
        return result
    except Exception as e:
        return f"Error generating video: {e}"
