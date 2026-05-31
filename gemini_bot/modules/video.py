import streamlit as st
from gradio_client import Client

@st.cache_resource
def get_video_client():
    try:
        return Client("damo-vilab/modelscope-text-to-video-synthesis")
    except Exception as e:
        return str(e)

def generate_video(prompt: str) -> tuple[str | None, str | None]:
    """
    Generate video using damo-vilab/modelscope-text-to-video-synthesis space.
    Returns (video_path, None) on success, or (None, error_message) on failure.
    """
    client = get_video_client()

    if isinstance(client, str):
        return None, f"Ошибка при подключении к сервису генерации видео: {client}"

    try:
        # Expected positional arguments: prompt, seed, num_frames, num_inference_steps
        result = client.predict(
            prompt,
            -1,  # seed
            16,  # num_frames
            25,  # num_inference_steps
            api_name="/generate_video"
        )
        # Assuming the first element of result dictionary/tuple is the path
        if isinstance(result, dict) and 'video' in result:
             return result['video'], None
        elif isinstance(result, (list, tuple)) and len(result) > 0:
            return result[0], None
        return result, None
    except Exception as e:
        return None, f"Ошибка при генерации видео: {str(e)}"
