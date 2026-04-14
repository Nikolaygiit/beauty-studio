from gradio_client import Client

def init_music_client():
    """Инициализирует клиент Gradio для генерации музыки."""
    try:
        client = Client("sanchit-gandhi/musicgen-streaming")
        return client
    except Exception as e:
        return f"Ошибка инициализации музыкального клиента: {str(e)}"

def generate_music(client, prompt):
    """
    Генерирует музыку по текстовому описанию.
    """
    if isinstance(client, str):
        return None, client # Вернуть текст ошибки

    try:
        result = client.predict(
            text_prompt=prompt,
            audio_length_in_s=15,
            play_steps_in_s=1.5,
            seed=0,
            api_name="/generate_audio"
        )
        return result, None
    except Exception as e:
        return None, f"Ошибка генерации музыки: {str(e)}"
