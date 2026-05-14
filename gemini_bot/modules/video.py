import streamlit as st
from gradio_client import Client

@st.cache_resource
def get_video_client():
    return Client("damo-vilab/modelscope-text-to-video-synthesis")

def generate_video(prompt: str) -> tuple[str | None, str | None]:
    """
    Generates video using the damo-vilab/modelscope-text-to-video-synthesis Gradio Space.
    Returns (video_path, error_msg).
    """
    try:
        client = get_video_client()
        result = client.predict(
            prompt,  # text_prompt
            -1,      # seed
            16,      # num_frames
            25,      # num_inference_steps
            api_name="/generate_video"
        )
        return result, None
    except ValueError as e:
         return None, f"Ошибка API генерации видео: {str(e)}"
    except RuntimeError as e:
         return None, f"Ошибка выполнения видео-модели: {str(e)}"
    except Exception as e:
        return None, f"Неизвестная ошибка при генерации видео: {str(e)}"
