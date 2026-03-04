import streamlit as st
from gradio_client import Client
import os

# Cache the client initialization so it doesn't reload on every rerun
@st.cache_resource
def get_music_client():
    try:
        # Use musicgen-streaming space
        client = Client("sanchit-gandhi/musicgen-streaming")
        return client
    except Exception as e:
        return str(e)

def render_music_module():
    st.header("🎵 Генерация музыки (MusicGen)")
    st.write("Использует модель MusicGen от Meta (через HuggingFace Space).")

    client = get_music_client()

    if isinstance(client, str):
        st.error(f"Не удалось подключиться к сервису генерации музыки. Ошибка: {client}")
        return

    prompt = st.text_area("Описание музыки:", "80s pop track with synth and instrumentals",
                         help="Рекомендуется использовать английский язык для лучших результатов")

    col1, col2 = st.columns(2)
    with col1:
        audio_length = st.slider("Длительность (секунды)", min_value=1.0, max_value=30.0, value=15.0, step=1.0)
    with col2:
        seed = st.number_input("Seed", value=5)

    if st.button("Сгенерировать музыку"):
        if prompt:
            with st.spinner("Пишем хит... Это может занять несколько минут."):
                try:
                    # As per memory: fn_index=0 for predictions
                    result_path = client.predict(
                        text_prompt=prompt,
                        audio_length_in_s=float(audio_length),
                        play_steps_in_s=1.5,
                        seed=float(seed),
                        fn_index=0
                    )

                    # Gradio client downloads to a temp folder, let's play it
                    if os.path.exists(result_path):
                        st.audio(result_path)

                        # Read file for download button
                        with open(result_path, "rb") as file:
                            st.download_button(
                                label="⬇️ Скачать аудио",
                                data=file,
                                file_name="generated_music.wav",
                                mime="audio/wav"
                            )
                    else:
                        st.error("Файл не был создан. Попробуйте еще раз.")

                except Exception as e:
                    st.error(f"Ошибка при генерации музыки: {e}")
        else:
            st.warning("Пожалуйста, введите описание музыки.")
