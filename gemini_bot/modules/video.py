import streamlit as st
from gradio_client import Client

@st.cache_resource
def get_video_client():
    try:
        return Client("damo-vilab/modelscope-text-to-video-synthesis")
    except Exception as e:
        # We need to handle this correctly. Caching functions shouldn't really return exceptions as state,
        # but for simplicity we will throw and catch in the generate_video function.
        raise e

def generate_video(prompt: str) -> tuple[str | None, str | None]:
    """
    Generates video using the damo-vilab/modelscope-text-to-video-synthesis space.
    Returns a tuple of (video_path_dict_or_path, error_message).
    Note: The specific space returns a dictionary with 'video' as key containing the path, or just the path itself in some client versions.
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

        # Result might be a string (path) or a dictionary depending on gradio client version
        video_path = result.get('video') if isinstance(result, dict) else result
        return video_path, None
    except ValueError as e:
        return None, f"Ошибка значения при генерации видео: {str(e)}"
    except RuntimeError as e:
        return None, f"Ошибка выполнения при генерации видео: {str(e)}"
    except Exception as e:
        return None, f"Неизвестная ошибка при генерации видео: {str(e)}"
