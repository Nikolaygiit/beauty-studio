import streamlit as st
from gradio_client import Client

@st.cache_resource(show_spinner=False)
def get_video_client():
    try:
        return Client("damo-vilab/modelscope-text-to-video-synthesis")
    except Exception as e: # Catching general exception including ValueError
        return f"Error initializing client: {str(e)}"

def generate_video(prompt):
    try:
        client = get_video_client()
        if isinstance(client, str):
            return None, client

        result = client.predict(
            prompt,
            -1,
            16,
            25,
            api_name="/generate_video"
        )
        return result, None
    except Exception as e:
        return None, str(e)
