import streamlit as st
from gradio_client import Client

@st.cache_resource
def get_video_client():
    try:
        return Client("damo-vilab/modelscope-text-to-video-synthesis")
    except Exception as e:
        return f"Ошибка инициализации видео-клиента: {str(e)}"

def generate_video(prompt: str) -> tuple[str | None, str | None]:
    """
    Generate video using the damo-vilab/modelscope-text-to-video-synthesis space.

    Args:
        prompt: The text prompt for video generation.

    Returns:
        A tuple of (video_path, error_message).
    """
    client_or_error = get_video_client()

    if isinstance(client_or_error, str):
        return None, client_or_error

    client = client_or_error

    try:
        # Note: positional arguments based on memory
        result = client.predict(
            prompt,
            -1,  # seed
            16,  # num_frames
            25,  # num_inference_steps
            api_name="/generate_video"
        )
        # The result from generate_video might be a path or a dict depending on Gradio version.
        # usually it is a path to the video.

        # we check if it is a dict and has 'video' key
        if isinstance(result, dict) and 'video' in result:
             return result['video'], None

        return result, None
    except ValueError as e:
        return None, f"Ошибка значений видео-генератора: {str(e)}"
    except RuntimeError as e:
        return None, f"Ошибка выполнения видео-генератора: {str(e)}"
    except Exception as e:
         return None, f"Неизвестная ошибка видео-генератора: {str(e)}"
