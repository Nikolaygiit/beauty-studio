import streamlit as st
from gradio_client import Client

@st.cache_resource
def get_video_client():
    """Инициализация и кэширование клиента Gradio для видео."""
    try:
        return Client("damo-vilab/modelscope-text-to-video-synthesis")
    except Exception as e:
        return f"Ошибка подключения к сервису генерации видео: {str(e)}"

def generate_video(prompt: str):
    """
    Генерирует видео с использованием damo-vilab/modelscope-text-to-video-synthesis.
    Возвращает (путь_к_видео, None) или (None, сообщение_об_ошибке).
    """
    client = get_video_client()

    if isinstance(client, str):
        # Ошибка при инициализации
        return None, client

    try:
        # Убираем возможные префиксы
        clean_prompt = prompt.lower()
        for kw in ['сгенерируй видео', 'создай видео', 'видео', 'ролик']:
            clean_prompt = clean_prompt.replace(kw, "").strip()

        if not clean_prompt:
            clean_prompt = prompt

        # Согласно memory: /generate_video API с позиционными аргументами: prompt, -1 (seed), 16 (num_frames), 25 (num_inference_steps)
        result = client.predict(
            clean_prompt,  # str  in 'Prompt' Textbox component
            -1,            # float (numeric value between -1 and 2147483647) in 'Seed' Slider component
            16,            # float (numeric value between 16 and 32) in 'Number of Frames' Slider component
            25,            # float (numeric value between 10 and 50) in 'Number of Inference Steps' Slider component
            api_name="/generate_video"
        )

        return result, None
    except ValueError as e:
        return None, f"Ошибка параметров при генерации видео: {str(e)}"
    except RuntimeError as e:
        return None, f"Ошибка выполнения при генерации видео: {str(e)}"
    except Exception as e:
        return None, f"Неизвестная ошибка при генерации видео: {str(e)}"
