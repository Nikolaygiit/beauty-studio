import logging
from gradio_client import Client

def generate_video(prompt, client=None):
    """
    Generates video using damo-vilab/modelscope-text-to-video-synthesis space.
    Requires a pre-initialized client to avoid recreating it per request.
    Returns (video_path_or_dict, None) on success, or (None, error_message) on failure.
    """
    try:
        if client is None:
             # Fallback if no client passed
             client = Client("damo-vilab/modelscope-text-to-video-synthesis")

        result = client.predict(
            prompt,
            -1,  # seed
            16,  # num_frames
            25,  # num_inference_steps
            api_name="/generate_video"
        )
        return result, None
    except Exception as e:
        error_msg = str(e)
        logging.error(f"Video Generation Error: {error_msg}")
        if "RUNTIME_ERROR" in error_msg:
             return None, f"Ошибка при генерации видео (ошибка сервера Gradio): {error_msg}"
        return None, f"Ошибка при генерации видео: {error_msg}"
