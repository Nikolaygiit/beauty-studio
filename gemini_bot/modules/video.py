import streamlit as st
from gradio_client import Client
import logging

logger = logging.getLogger(__name__)

@st.cache_resource(show_spinner=False)
def get_video_client():
    """
    Initializes and caches the Gradio client for video generation.
    """
    try:
        return Client("damo-vilab/modelscope-text-to-video-synthesis")
    except ValueError as ve:
        error_msg = f"Ошибка конфигурации клиента видео: {ve}"
        logger.error(error_msg)
        return error_msg
    except RuntimeError as re:
        error_msg = f"Ошибка выполнения клиента видео: {re}"
        logger.error(error_msg)
        return error_msg
    except Exception as e:
        error_msg = f"Неизвестная ошибка инициализации клиента видео: {e}"
        logger.error(error_msg)
        return error_msg

def generate_video(prompt: str) -> tuple[str | None, str | None]:
    """
    Generates video using the damo-vilab/modelscope-text-to-video-synthesis Gradio space.
    Returns (video_file_path, error_message).
    """
    client_or_error = get_video_client()
    if isinstance(client_or_error, str):
        return None, client_or_error

    client = client_or_error

    try:
        result = client.predict(
            prompt,
            -1,  # seed
            16,  # num_frames
            25,  # num_inference_steps
            api_name="/generate_video"
        )

        # Result is typically a dictionary containing 'video' path or direct tuple
        if isinstance(result, dict) and 'video' in result:
             return result['video'], None
        elif isinstance(result, tuple) and len(result) > 0:
             return result[0], None
        return result, None
    except ValueError as ve:
        error_msg = f"Ошибка значений при генерации видео: {ve}"
        logger.error(error_msg)
        return None, error_msg
    except RuntimeError as re:
        error_msg = f"Ошибка выполнения при генерации видео: {re}"
        logger.error(error_msg)
        return None, error_msg
    except Exception as e:
        error_msg = f"Неизвестная ошибка при генерации видео: {str(e)}"
        logger.error(error_msg)
        return None, error_msg
