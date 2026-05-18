from gradio_client import Client

def get_video_client():
    """Initializes the video client."""
    try:
        client = Client("damo-vilab/modelscope-text-to-video-synthesis")
        return client, None
    except Exception as e:
        # Gracefully handle exception by returning error message
        return None, f"Ошибка инициализации ModelScope клиента: {str(e)}"

def generate_video(client: Client, prompt: str):
    """
    Generates video using the provided Gradio client.
    Returns (media_path, error_msg).
    """
    if not client:
        return None, "Клиент ModelScope не инициализирован."

    try:
        result = client.predict(
            prompt,
            -1, # seed
            16, # num_frames
            25, # num_inference_steps
            api_name="/generate_video"
        )
        return result, None
    except ValueError as ve:
        return None, f"ValueError при генерации видео: {str(ve)}"
    except RuntimeError as re:
        return None, f"RuntimeError при генерации видео: {str(re)}"
    except Exception as e:
        return None, f"Неизвестная ошибка генерации видео: {str(e)}"
