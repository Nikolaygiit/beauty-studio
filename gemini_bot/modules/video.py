import streamlit as st
from gradio_client import Client

@st.cache_resource
def get_video_client():
    """
    Returns a cached instance of the Gradio Client for video generation.
    """
    try:
        return Client("damo-vilab/modelscope-text-to-video-synthesis")
    except Exception as e:
        return f"Ошибка инициализации видео клиента: {str(e)}"

def generate_video(prompt: str) -> tuple[str | None, str | None]:
    """
    Generates video using the damo-vilab/modelscope-text-to-video-synthesis Gradio space.
    Passes fixed positional parameters: prompt, -1 (seed), 16 (num_frames), 25 (num_inference_steps).
    Returns: (video_file_path, error_message)
    """
    client = get_video_client()
    if isinstance(client, str):
        return None, client

    try:
        result = client.predict(
            prompt,
            -1,  # seed
            16,  # num_frames
            25,  # num_inference_steps
            api_name="/generate_video"
        )
        # Check if the result is a dict with 'video' key (Gradio can return dicts with metadata)
        if isinstance(result, dict) and 'video' in result:
            return result['video'], None
        # Often it returns just the file path
        elif isinstance(result, str):
            return result, None
        elif isinstance(result, tuple) and len(result) > 0 and isinstance(result[0], dict) and 'video' in result[0]:
            return result[0]['video'], None
        elif isinstance(result, dict) and 'value' in result and isinstance(result['value'], dict) and 'video' in result['value']:
            return result['value']['video'], None

        return str(result), None # Fallback

    except ValueError as e:
        return None, f"Ошибка значения при генерации видео: {str(e)}"
    except RuntimeError as e:
        return None, f"Ошибка времени выполнения при генерации видео: {str(e)}"
    except Exception as e:
        return None, f"Ошибка генерации видео: {str(e)}"
