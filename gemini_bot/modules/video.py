from gradio_client import Client

def init_video_client():
    """Initializes the video generator client.
    Handles RUNTIME_ERROR from the gradio space if it occurs.
    """
    try:
        client = Client("damo-vilab/modelscope-text-to-video-synthesis")
        return client
    except Exception as e:
        error_msg = str(e)
        if "RUNTIME_ERROR" in error_msg:
            return f"Ошибка: Видео сервер сейчас недоступен (RUNTIME_ERROR)."
        return f"Ошибка инициализации видео: {error_msg}"

def generate_video(client, prompt: str):
    """Generates video using the provided video generator client.
    Uses fixed parameters based on the model scope defaults.
    """
    if isinstance(client, str):
        # Client initialization failed, return the error message
        return client, None

    try:
        # fixed parameters: seed -1, 16 frames, 25 inference steps based on memory
        result = client.predict(
            prompt,
            -1, # seed
            25, # num_inference_steps
            16, # num_frames
            api_name="/video_synthesis"
        )
        # Returns a dict that has video path or just the video path depending on gradio client version
        video_path = result.get('video') if isinstance(result, dict) else result
        return None, video_path
    except Exception as e:
        error_msg = str(e)
        if "RUNTIME_ERROR" in error_msg:
             return f"Ошибка: Видео сервер сейчас недоступен (RUNTIME_ERROR).", None
        return f"Произошла ошибка при генерации видео: {error_msg}", None
