import streamlit as st
from modules.text import init_chat_session, generate_text_stream
from modules.image import generate_image_url
from modules.music import generate_music
from modules.video import generate_video
import re

st.set_page_config(page_title="Gemini Ultimate Bot", page_icon="🤖", layout="wide")

st.title("Gemini Ultimate Bot 🤖")

# Sidebar
st.sidebar.header("Настройки")
api_key = st.sidebar.text_input("Введите GOOGLE_API_KEY", type="password")

if st.sidebar.button("Очистить историю чата"):
    st.session_state.chat_session = None
    st.session_state.messages = []
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.markdown("### Инструкция:")
st.sidebar.markdown("1. Введите Google API Key.")
st.sidebar.markdown("2. Задавайте вопросы для текста.")
st.sidebar.markdown("3. Для картинок начните запрос со слов: **'нарисуй'**, **'фото'**, **'изображение'**.")
st.sidebar.markdown("4. Используйте вкладки для прямой генерации видео или музыки.")

# Initialize session state for messages and chat session
if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_session" not in st.session_state:
    st.session_state.chat_session = None

if api_key and not st.session_state.chat_session:
    chat = init_chat_session(api_key)
    if chat:
        st.session_state.chat_session = chat
        st.sidebar.success("Gemini API успешно подключен!")

# UI Tabs
tab_chat, tab_music, tab_video = st.tabs(["💬 Чат (Текст & Картинки)", "🎵 Музыка", "🎬 Видео"])

with tab_chat:
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            if message["type"] == "text":
                st.markdown(message["content"])
            elif message["type"] == "image":
                st.image(message["content"], caption=message["prompt"])

    # Chat Input
    prompt = st.chat_input("Введите ваш запрос...")

    if prompt:
        # Check if the prompt is for an image
        # Check for Russian keywords at the beginning
        img_match = re.match(r'^(нарисуй|фото|изображение)\s+(.*)', prompt, re.IGNORECASE)

        if img_match:
            # It's an image request
            image_prompt = img_match.group(2).strip()
            if not image_prompt:
                image_prompt = prompt # fallback if they just type "нарисуй" without context

            # Add user message to UI
            st.session_state.messages.append({"role": "user", "type": "text", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                with st.spinner("Генерация изображения..."):
                    img_url = generate_image_url(image_prompt)
                    st.image(img_url, caption=image_prompt)
                    st.session_state.messages.append({
                        "role": "assistant",
                        "type": "image",
                        "content": img_url,
                        "prompt": image_prompt
                    })
        else:
            # It's a text request
            st.session_state.messages.append({"role": "user", "type": "text", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                if not st.session_state.chat_session:
                    st.error("Пожалуйста, введите GOOGLE_API_KEY в боковой панели.")
                else:
                    response_placeholder = st.empty()
                    full_response = ""
                    for chunk in generate_text_stream(st.session_state.chat_session, prompt):
                        full_response += chunk
                        response_placeholder.markdown(full_response + "▌")
                    response_placeholder.markdown(full_response)

                    st.session_state.messages.append({
                        "role": "assistant",
                        "type": "text",
                        "content": full_response
                    })

with tab_music:
    st.header("Генерация Музыки 🎵")
    music_prompt = st.text_area("Опишите музыку, которую хотите сгенерировать (желательно на английском):", height=100)

    if st.button("Сгенерировать музыку", type="primary"):
        if not music_prompt:
            st.warning("Пожалуйста, введите описание музыки.")
        else:
            with st.spinner("Генерация музыки... Это может занять несколько минут."):
                audio_path, error = generate_music(music_prompt)
                if error:
                    st.error(error)
                elif audio_path:
                    # Depending on the Gradio client output, it might be a tuple or a direct string path
                    # sanchit-gandhi/musicgen-streaming typically returns a single tuple element containing the path, or just the path
                    if isinstance(audio_path, tuple) or isinstance(audio_path, list):
                        st.audio(audio_path[0])
                    else:
                        st.audio(audio_path)
                    st.success("Музыка успешно сгенерирована!")

with tab_video:
    st.header("Генерация Видео 🎬")
    video_prompt = st.text_area("Опишите видео, которое хотите сгенерировать (желательно на английском):", height=100)

    if st.button("Сгенерировать видео", type="primary"):
        if not video_prompt:
            st.warning("Пожалуйста, введите описание видео.")
        else:
            with st.spinner("Генерация видео... Это может занять несколько минут."):
                video_result, error = generate_video(video_prompt)
                if error:
                    st.error(error)
                elif video_result:
                    # damo-vilab usually returns a path to the mp4
                    # we extract the path based on typical Gradio video outputs
                    try:
                        if isinstance(video_result, dict) and 'video' in video_result:
                             st.video(video_result['video'])
                        elif isinstance(video_result, tuple) or isinstance(video_result, list):
                             st.video(video_result[0])
                        else:
                             st.video(video_result)
                        st.success("Видео успешно сгенерировано!")
                    except Exception as e:
                        st.error(f"Ошибка отображения видео: {e}. Сырой результат: {video_result}")
