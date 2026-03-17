from gradio_client import Client

def get_video_client():
    """Инициализирует и возвращает клиент Gradio для генерации видео."""
    try:
        client = Client("damo-vilab/modelscope-text-to-video-synthesis")
        return client
    except Exception as e:
        # Грациозная обработка RUNTIME_ERROR и других ошибок инициализации
        return f"Сервис генерации видео временно недоступен ({str(e)})."

def generate_video(client, prompt):
    """
    Генерирует видео по текстовому промпту.
    """
    if isinstance(client, str):
        # Если клиент - это сообщение об ошибке
        return None, client

    try:
        # Фиксированные параметры: prompt, -1 (seed), 16 (frames), 25 (steps)
        result = client.predict(
            prompt,
            api_name="/predict"
        )
        return result, None
    except Exception as e:
        return None, f"Ошибка генерации видео: {str(e)}"
