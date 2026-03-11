import time

def generate_music(prompt, client):
    """
    Генерация музыки с использованием Gradio клиента `sanchit-gandhi/musicgen-streaming`.
    """
    try:
        # Client initialization is handled in app.py to avoid recreating it
        if not client:
            return None, "Клиент не инициализирован. Пожалуйста, перезапустите приложение."

        result = client.predict(
            prompt=prompt,
            api_name="/generate_audio"
        )
        return result, None
    except Exception as e:
        return None, f"Ошибка при генерации музыки: {str(e)}"
