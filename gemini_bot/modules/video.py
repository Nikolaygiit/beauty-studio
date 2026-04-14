from gradio_client import Client

def init_video_client():
    """Инициализирует клиент Gradio для генерации видео."""
    try:
        client = Client("damo-vilab/modelscope-text-to-video-synthesis")
        return client
    except Exception as e:
        return f"Ошибка инициализации видео-клиента (RUNTIME_ERROR и др.): {str(e)}"

def generate_video(client, prompt):
    """
    Генерирует видео по текстовому описанию.
    """
    if isinstance(client, str):
        return None, client # Возвращаем текст ошибки инициализации

    try:
        result = client.predict(
            prompt,   # prompt
            -1,       # seed
            16,       # num_frames
            25,       # num_inference_steps
            api_name="/generate_video"
        )
        return result, None
    except Exception as e:
        return None, f"Ошибка генерации видео: {str(e)}"
