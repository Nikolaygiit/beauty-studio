from gradio_client import Client
import streamlit as st

@st.cache_resource
def get_video_client():
    return Client("damo-vilab/modelscope-text-to-video-synthesis")

def generate_video(prompt: str) -> tuple[str | None, str | None]:
    try:
        client = get_video_client()
        result = client.predict(
            prompt,
            -1,  # seed
            16,  # num_frames
            25,  # num_inference_steps
            api_name="/generate_video"
        )
        # Note: Depending on the specific Gradio interface, the result format might differ.
        # usually it returns a dictionary or directly the path to the video file.
        # For this particular endpoint, it returns a dictionary where we typically need the path or the first item.
        # Adjusting the return type as needed:
        if isinstance(result, dict) and "video" in result:
             return result["video"], None
        elif isinstance(result, str):
            return result, None
        elif isinstance(result, tuple) or isinstance(result, list):
             return result[0], None
        return str(result), None
    except ValueError as e:
        return None, f"Video generation value error: {str(e)}"
    except RuntimeError as e:
        return None, f"Video generation runtime error: {str(e)}"
    except Exception as e:
        return None, f"Video generation error: {str(e)}"
