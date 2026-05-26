import streamlit as st
from gradio_client import Client

@st.cache_resource
def get_video_client():
    """
    Returns a cached Gradio client for video generation.
    Returns (client, error_message)
    """
    try:
        client = Client("damo-vilab/modelscope-text-to-video-synthesis")
        return client, None
    except Exception as e:
        return None, f"Ошибка инициализации генератора видео: {str(e)}"

def generate_video(prompt):
    """
    Generates video using damo-vilab/modelscope-text-to-video-synthesis Gradio Space.
    Returns (path, error_message)
    """
    client, error = get_video_client()
    if error:
        return None, error

    try:
        result = client.predict(
            prompt,
            -1, # seed
            16, # num_frames
            25, # num_inference_steps
            api_name="/generate_video"
        )
        # The result from generate_video is often a tuple or dictionary,
        # but gradio client generally returns the path to the file as string or tuple.
        # Let's check type. If tuple, get the first element which is usually the file path.
        # Gradio spaces might return dict or tuple, but based on typical usage, it returns a dict with 'video' key or direct path.
        path = result
        if isinstance(result, tuple) and len(result) > 0:
            path = result[0]
        elif isinstance(result, dict) and 'video' in result:
            path = result['video']

        return path, None
    except ValueError as e:
        return None, f"Ошибка генерации видео (ValueError): {str(e)}"
    except RuntimeError as e:
        return None, f"Ошибка генерации видео (RuntimeError): {str(e)}"
    except Exception as e:
        return None, f"Ошибка генерации видео: {str(e)}"
