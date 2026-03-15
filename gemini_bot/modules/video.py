import streamlit as st
from gradio_client import Client

@st.cache_resource(show_spinner=False)
def get_video_client():
    """Caches and returns the Gradio client for video generation."""
    try:
        return Client("damo-vilab/modelscope-text-to-video-synthesis")
    except RuntimeError as e:
        return f"RUNTIME_ERROR: Ошибка инициализации видео клиента: {e}"
    except Exception as e:
        return f"Ошибка инициализации видео клиента: {e}"

def generate_video(prompt):
    """
    Generates video using the damo-vilab/modelscope-text-to-video-synthesis space.
    Uses fixed parameters: seed -1, 16 frames, and 25 inference steps.
    """
    client = get_video_client()
    if isinstance(client, str):
        return None, client # Return error message

    try:
        # Typical args for modelscope text-to-video prediction: text, seed, video_length, num_inference_steps
        result = client.predict(
            prompt,
            -1,  # seed
            16,  # video length
            25,  # num_inference_steps
            api_name="/predict"
        )
        return result, None
    except RuntimeError as e:
        return None, f"RUNTIME_ERROR: Ошибка во время генерации видео: {e}"
    except Exception as e:
        return None, f"Ошибка генерации видео: {e}"
