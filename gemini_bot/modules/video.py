import streamlit as st
import random
from gradio_client import Client
import os

@st.cache_resource
def get_video_client():
    try:
        # Default as per memory
        client = Client("damo-vilab/modelscope-text-to-video-synthesis")
        return client
    except Exception as e:
        return str(e)

def render_video_module():
    st.header("🎬 Генерация видео")
    st.write("Генерация коротких видеофрагментов по тексту.")

    client = get_video_client()

    if isinstance(client, str):
        st.error(f"Сервис генерации видео временно недоступен. Ошибка: {client}")
        return

    prompt = st.text_area("Описание видео:", "Astronaut riding a horse on mars, high quality",
                         help="Используйте английский язык для промптов")

    st.info("Внимание: Генерация видео может занимать значительное время (5-10 минут) и часто завершается таймаутом на бесплатных серверах.")

    if st.button("Сгенерировать видео"):
        if prompt:
            with st.spinner("Создаю видео... Пожалуйста, подождите."):
                try:
                    # As per memory: fixed parameters: seed -1, 16 frames, and 25 inference steps
                    result = client.predict(
                        prompt,
                        -1, # seed (random)
                        16, # num frames
                        25, # num inference steps
                        api_name="/predict"
                    )

                    if result and os.path.exists(result):
                        st.video(result)

                        with open(result, "rb") as file:
                            st.download_button(
                                label="⬇️ Скачать видео",
                                data=file,
                                file_name="generated_video.mp4",
                                mime="video/mp4"
                            )
                    else:
                        st.error("Не удалось получить видео из сервиса.")
                except Exception as e:
                    st.error(f"Ошибка при генерации видео. Возможно, сервер перегружен: {e}")
        else:
            st.warning("Пожалуйста, введите описание видео.")
