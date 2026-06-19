import streamlit as st
from gradio_client import Client

@st.cache_resource
def get_video_client():
    return Client("damo-vilab/modelscope-text-to-video-synthesis")

def generate_video(prompt: str) -> tuple[str | None, str | None]:
    """
    Generates video using ModelScope Gradio space.
    Returns (video_path, error_message).
    """
    try:
        client = get_video_client()
        result = client.predict(
            prompt,
            -1,  # seed
            16,  # num_frames
            25,  # num_inference_steps
            api_name="/generate_video"
        )
        # The result from Gradio might be a dictionary with 'video' key or a path string.
        # Ensure we return a string path.
        if isinstance(result, dict) and 'video' in result:
            return result['video'], None
        elif isinstance(result, str):
            return result, None
        else:
            # Try to get the first element if it's a tuple/list
            try:
                return result[0]['video'], None
            except:
                return str(result), None
    except ValueError as ve:
         return None, f"ValueError generating video: {str(ve)}"
    except RuntimeError as re:
         return None, f"RuntimeError generating video: {str(re)}"
    except Exception as e:
        return None, f"Error generating video: {str(e)}"
