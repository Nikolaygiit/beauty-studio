import streamlit as st
import os
import requests

from modules.routing import get_route
from modules.text import init_gemini_client, generate_text_stream
from modules.image import generate_image
from modules.music import generate_music
from modules.video import generate_video

# Настройка страницы
st.set_page_config(page_title="Gemini Ultimate Bot", page_icon="🤖", layout="centered")
st.title("🤖 Gemini Ultimate Bot")
st.markdown("Генерация текста, изображений, музыки и видео в одном месте!")

# Инициализация состояния
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "chat_session" not in st.session_state:
    st.session_state.chat_session = None
if "gemini_client" not in st.session_state:
    st.session_state.gemini_client = None
if "current_api_key" not in st.session_state:
    st.session_state.current_api_key = ""

# Боковая панель
with st.sidebar:
    st.header("⚙️ Настройки")
    api_key = st.text_input("Введите GOOGLE_API_KEY", type="password", value=st.session_state.current_api_key)

    # Обработка изменения API ключа
    if api_key != st.session_state.current_api_key and api_key:
        st.session_state.current_api_key = api_key
        client, chat, error = init_gemini_client(api_key)
        if error:
            st.error(error)
        else:
            st.session_state.gemini_client = client
            st.session_state.chat_session = chat
            st.success("API ключ успешно применён!")

    # Кнопка очистки истории
    if st.button("Очистить историю чата"):
        st.session_state.chat_history = []
        # Пересоздаем сессию чата, если ключ есть
        if st.session_state.current_api_key:
            client, chat, _ = init_gemini_client(st.session_state.current_api_key)
            st.session_state.gemini_client = client
            st.session_state.chat_session = chat
        st.rerun()

# Отображение истории чата
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        if message["type"] == "text":
            st.markdown(message["content"])
        elif message["type"] == "image":
            st.image(message["content"], caption="Сгенерированное изображение")
        elif message["type"] == "audio":
            st.audio(message["content"])
        elif message["type"] == "video":
            st.video(message["content"])

# Ввод пользователя
prompt = st.chat_input("Напишите сообщение...")

if prompt:
    if not st.session_state.current_api_key:
        st.error("Пожалуйста, введите GOOGLE_API_KEY в боковой панели.")
        st.stop()

    # Отображение сообщения пользователя
    st.chat_message("user").markdown(prompt)
    st.session_state.chat_history.append({"role": "user", "type": "text", "content": prompt})

    # Определяем маршрут
    route = get_route(prompt)

    with st.chat_message("assistant"):
        if route == "image":
            with st.spinner("Генерирую изображение..."):
                url, error = generate_image(prompt)
                if error:
                    st.error(error)
                    st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": error})
                else:
                    st.image(url, caption="Сгенерированное изображение")
                    st.session_state.chat_history.append({"role": "assistant", "type": "image", "content": url})

        elif route == "music":
            with st.spinner("Генерирую музыку..."):
                audio_path, error = generate_music(prompt)
                if error:
                    st.error(error)
                    st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": error})
                else:
                    st.audio(audio_path)
                    st.session_state.chat_history.append({"role": "assistant", "type": "audio", "content": audio_path})

        elif route == "video":
            with st.spinner("Генерирую видео..."):
                video_path, error = generate_video(prompt)
                if error:
                    st.error(error)
                    st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": error})
                else:
                    st.video(video_path)
                    st.session_state.chat_history.append({"role": "assistant", "type": "video", "content": video_path})

        else: # text
            with st.spinner("Генерирую ответ..."):
                if not st.session_state.chat_session:
                    st.error("Сессия чата не инициализирована.")
                else:
                    try:
                        response_placeholder = st.empty()
                        full_response = ""

                        stream = generate_text_stream(st.session_state.chat_session, prompt)
                        for chunk in stream:
                            if chunk.text:
                                full_response += chunk.text
                                response_placeholder.markdown(full_response + "▌")

                        response_placeholder.markdown(full_response)
                        st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": full_response})
                    except Exception as e:
                        error_msg = f"Ошибка генерации текста: {str(e)}"
                        st.error(error_msg)
                        st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": error_msg})
