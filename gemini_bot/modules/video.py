import streamlit as st
from gradio_client import Client

@st.cache_resource
def get_video_client():
    try:
        return Client("damo-vilab/modelscope-text-to-video-synthesis")
    except Exception as e:
        return f"Ошибка инициализации генератора видео: {str(e)}"

def generate_video(prompt: str):
    client = get_video_client()
    if isinstance(client, str):
        return client # Возвращаем ошибку инициализации

    try:
        result = client.predict(
            prompt,
            -1, # seed
            16, # num_frames
            25, # num_inference_steps
            api_name="/video_synthesis"
        )
        # Ожидаем, что result['video'] - путь к видео или само видео
        # Gradio API обычно возвращает путь к сохраненному файлу
        # Проверяем, что возвращает API
        if isinstance(result, str):
            return result
        elif isinstance(result, dict) and 'video' in result:
            return result['video']
        elif isinstance(result, tuple) and len(result) > 0:
            return result[0]
        else:
             return result

    except Exception as e:
        return f"Ошибка генерации видео: {str(e)}"
