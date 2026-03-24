from gradio_client import Client

def initialize_video_client():
    try:
        client = Client("damo-vilab/modelscope-text-to-video-synthesis")
        return client
    except Exception as e:
        if "RUNTIME_ERROR" in str(e):
            return "Ошибка RUNTIME_ERROR при подключении к сервису генерации видео. Сервис может быть временно недоступен."
        return f"Ошибка при инициализации клиента видео: {str(e)}"

def generate_video(client, prompt):
    if isinstance(client, str):
        return None, client # Return error message

    try:
        result = client.predict(
            prompt,	# str in 'Prompt' Textbox component
            -1,	# int | float (numeric value between -1 and 2147483647) in 'Seed' Slider component
            16,	# int | float (numeric value between 16 and 16) in 'Number of Frames' Slider component
            25,	# int | float (numeric value between 10 and 50) in 'Number of Inference Steps' Slider component
            api_name="/generate_video"
        )
        return result, None
    except Exception as e:
        if "RUNTIME_ERROR" in str(e):
            return None, "Ошибка RUNTIME_ERROR при генерации видео. Сервис может быть перегружен."
        return None, f"Ошибка при генерации видео: {str(e)}"
