from gradio_client import Client
import random

def get_music_client():
    """Инициализирует и возвращает клиент Gradio для генерации музыки."""
    try:
        client = Client("sanchit-gandhi/musicgen-streaming")
        return client
    except Exception as e:
        return f"Ошибка подключения к сервису генерации музыки: {str(e)}"

def generate_music(client, prompt):
    """
    Генерирует музыку по текстовому промпту.
    Возвращает путь к сгенерированному аудиофайлу.
    """
    if isinstance(client, str):
        # Если клиент - это строка с ошибкой инициализации
        return None, client

    try:
        # Параметры: text_prompt, audio_length_in_s, play_steps_in_s, seed
        seed = random.randint(1, 100000)
        result = client.predict(
            text_prompt=prompt,
            audio_length_in_s=15,
            play_steps_in_s=1.5,
            seed=seed,
            api_name="/generate_audio"
        )
        return result, None
    except Exception as e:
        return None, f"Ошибка генерации музыки: {str(e)}"
