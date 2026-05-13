from gradio_client import Client
import streamlit as st

@st.cache_resource(show_spinner=False)
def get_music_client():
    """Returns a cached instance of the Gradio client for musicgen."""
    try:
        return Client("sanchit-gandhi/musicgen-streaming")
    except Exception as e:
        st.error(f"Failed to initialize Music client: {e}")
        return None

def generate_music(prompt):
    """
    Generates music using the sanchit-gandhi/musicgen-streaming Gradio client.
    Returns (audio_path, error_message).
    """
    client = get_music_client()
    if client is None:
         return None, "Music client initialization failed."

    try:
        # Named arguments as per memory context
        result = client.predict(
            text_prompt=prompt,
            audio_length_in_s=15,
            play_steps_in_s=1.5,
            seed=0,
            api_name="/generate_audio"
        )
        return result, None
    except Exception as e:
        return None, f"Failed to generate music: {e}"
