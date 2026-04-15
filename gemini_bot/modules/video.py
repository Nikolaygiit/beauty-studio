from gradio_client import Client

def generate_video(prompt: str, client: Client) -> str:
    """
    Generates video using the provided gradio client connected to 'damo-vilab/modelscope-text-to-video-synthesis'.
    """
    if isinstance(client, str): # Handle initialization error stored as string
        return client

    try:
        # Based on memory: The video generation module configured with fixed positional parameters for the `/generate_video` API: `prompt`, `-1` (seed), `16` (num_frames), and `25` (num_inference_steps).
        result = client.predict(
            prompt,
            -1,
            16,
            25,
            api_name="/generate_video"
        )
        # Returns a dict with a video path or tuple
        if isinstance(result, tuple) and len(result) > 0:
            return result[0]
        elif isinstance(result, dict) and 'video' in result:
             return result['video']
        return result
    except Exception as e:
        error_msg = str(e)
        if "RUNTIME_ERROR" in error_msg:
            return "Ошибка при генерации видео: Сервис временно недоступен (RUNTIME_ERROR). Пожалуйста, попробуйте позже."
        return f"Ошибка при генерации видео: {error_msg}"
