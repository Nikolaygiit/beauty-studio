import streamlit as st
from gradio_client import Client

@st.cache_resource
def get_video_client():
    """
    Initializes and caches the Gradio client for video generation.
    Returns (client, error_message)
    """
    try:
        client = Client("damo-vilab/modelscope-text-to-video-synthesis")
        return client, None
    except Exception as e:
        return None, f"Failed to initialize video client: {e}"

def generate_video(prompt: str) -> tuple[str, str]:
    """
    Generates video based on the prompt using the cached Gradio client.
    Returns (video_path, error_message)
    """
    client, error = get_video_client()
    if error:
        return None, error

    try:
        # According to memory: fixed positional parameters for the /generate_video API:
        # prompt, -1 (seed), 16 (num_frames), and 25 (num_inference_steps).
        result = client.predict(
            prompt,  # prompt
            -1,      # seed
            16,      # num_frames
            25,      # num_inference_steps
            api_name="/generate_video"
        )
        # The result is expected to be a dictionary where 'video' is a filepath
        # We need to extract the filepath
        if isinstance(result, dict) and 'video' in result:
            return result['video'], None
        elif isinstance(result, str):
            return result, None
        elif isinstance(result, tuple) or isinstance(result, list):
            # Try to return the first element if it's a tuple or list
            return result[0], None
        else:
            return str(result), None

    except ValueError as e:
        return None, f"ValueError during video generation: {e}"
    except RuntimeError as e:
        return None, f"RuntimeError during video generation: {e}"
    except Exception as e:
        return None, f"Failed to generate video: {e}"
