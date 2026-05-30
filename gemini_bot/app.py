import streamlit as st
import os
from modules.routing import get_route
from modules.text import init_gemini, generate_text_stream
from modules.image import generate_image
from modules.music import generate_music
from modules.video import generate_video

# Настройка страницы
st.set_page_config(
    page_title="Gemini Ultimate Bot",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Gemini Ultimate Bot")
st.markdown("Универсальный помощник: текст, фото, музыка и видео!")

# Инициализация состояния истории чата
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Боковая панель для настроек
with st.sidebar:
    st.header("Настройки")
    api_key = st.text_input("Введите GOOGLE_API_KEY", type="password")

    if st.button("Очистить историю чата"):
        st.session_state.chat_history = []
        if 'chat_session' in st.session_state:
            del st.session_state.chat_session
        if 'gemini_client' in st.session_state:
            del st.session_state.gemini_client
        st.rerun()

    st.markdown("---")
    st.markdown("""
    **Поддерживаемые команды:**
    - 📝 Текст (по умолчанию)
    - 🎨 Нарисуй / фото / картинка ...
    - 🎵 Музыка / песня / трек ...
    - 🎥 Видео / ролик ...
    """)

# Основная логика чата
if not api_key:
    st.info("Пожалуйста, введите GOOGLE_API_KEY в боковой панели, чтобы начать работу.")
else:
    # Инициализируем Gemini при наличии ключа
    init_gemini(api_key)

    # Отображение истории
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            if message["type"] == "text":
                st.markdown(message["content"])
            elif message["type"] == "image":
                st.image(message["content"])
            elif message["type"] == "music":
                st.audio(message["content"])
            elif message["type"] == "video":
                st.video(message["content"])
            elif message["type"] == "error":
                st.error(message["content"])

    # Ввод пользователя
    prompt = st.chat_input("Введите ваш запрос...")

    if prompt:
        # Добавляем и отображаем запрос пользователя
        st.session_state.chat_history.append({"role": "user", "type": "text", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Определяем тип маршрутизации
        route = get_route(prompt)

        with st.chat_message("assistant"):
            if route == 'text':
                response_placeholder = st.empty()
                full_response = ""
                # Потоковая генерация текста
                for chunk in generate_text_stream(prompt):
                    full_response += chunk
                    response_placeholder.markdown(full_response + "▌")
                response_placeholder.markdown(full_response)
                st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": full_response})

            elif route == 'image':
                with st.spinner("Генерирую изображение..."):
                    url, error = generate_image(prompt)
                    if error:
                        st.error(error)
                        st.session_state.chat_history.append({"role": "assistant", "type": "error", "content": error})
                    else:
                        st.image(url)
                        st.session_state.chat_history.append({"role": "assistant", "type": "image", "content": url})

            elif route == 'music':
                with st.spinner("Генерирую музыку..."):
                    audio_path, error = generate_music(prompt)
                    if error:
                        st.error(error)
                        st.session_state.chat_history.append({"role": "assistant", "type": "error", "content": error})
                    else:
                        st.audio(audio_path)
                        st.session_state.chat_history.append({"role": "assistant", "type": "music", "content": audio_path})

            elif route == 'video':
                with st.spinner("Генерирую видео..."):
                    video_path, error = generate_video(prompt)
                    if error:
                        st.error(error)
                        st.session_state.chat_history.append({"role": "assistant", "type": "error", "content": error})
                    else:
                        st.video(video_path)
                        st.session_state.chat_history.append({"role": "assistant", "type": "video", "content": video_path})
