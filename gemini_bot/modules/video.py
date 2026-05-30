import streamlit as st
from gradio_client import Client

@st.cache_resource
def get_video_client():
    """
    Инициализирует и кэширует Gradio-клиент для генерации видео.
    """
    try:
        return Client("damo-vilab/modelscope-text-to-video-synthesis")
    except Exception as e:
        return f"Ошибка инициализации клиента: {str(e)}"

def generate_video(prompt: str) -> tuple[str | None, str | None]:
    """
    Генерирует видео через модель ModelScope Text-to-Video.
    Возвращает: (путь_к_видеофайлу, сообщение_об_ошибке)
    """
    client = get_video_client()

    if isinstance(client, str): # Ошибка при инициализации
        return None, client

    try:
        # Вызываем API модели ModelScope
        result = client.predict(
            prompt,   # prompt
            -1,       # seed
            16,       # num_frames
            25,       # num_inference_steps
            api_name="/generate_video"
        )
        return result, None
    except ValueError as e:
        return None, f"Ошибка в параметрах запроса: {str(e)}"
    except RuntimeError as e:
        return None, f"Ошибка времени выполнения на сервере: {str(e)}"
    except Exception as e:
        return None, f"Неизвестная ошибка при генерации видео: {str(e)}"
