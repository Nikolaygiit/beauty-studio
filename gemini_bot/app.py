import streamlit as st
import os
from modules.text import TextGeneration
from modules.image import ImageGeneration
from modules.music import MusicGeneration
from modules.video import VideoGeneration

st.set_page_config(page_title="Gemini Ultimate Bot", page_icon="🤖", layout="wide")

st.title("🤖 Gemini Ultimate Bot")

# Sidebar for Configuration
with st.sidebar:
    st.header("Настройки")
    api_key = st.text_input("Google API Key", type="password")

    # Check if API key changed
    if "api_key" not in st.session_state:
        st.session_state.api_key = ""

    if api_key and api_key != st.session_state.api_key:
        st.session_state.api_key = api_key
        os.environ["GOOGLE_API_KEY"] = api_key
        # Re-init text model
        if "text_model" in st.session_state:
            del st.session_state.text_model
        # Clear chat history on key change
        st.session_state.messages = []

    st.markdown("---")
    st.markdown("### О боте")
    st.markdown("Этот бот использует **Gemini** для текста, **Pollinations** для изображений, и **HuggingFace** модели для музыки и видео.")
    st.markdown("Created by Jules")

# Initialize Session State for Messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Initialize Text Model if key is present
if "text_model" not in st.session_state and st.session_state.api_key:
    try:
        st.session_state.text_model = TextGeneration(st.session_state.api_key)
    except Exception as e:
        st.error(f"Error initializing Gemini: {e}")

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["💬 Чат & Текст", "🎨 Изображения", "🎵 Музыка", "🎥 Видео"])

# --- TAB 1: Chat ---
with tab1:
    st.header("Чат с Gemini")
    if not st.session_state.api_key:
        st.warning("Пожалуйста, введите Google API Key в боковой панели.")
    else:
        # Display Chat History
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Chat Input
        if prompt := st.chat_input("Введите сообщение..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                full_response = ""
                try:
                    if "text_model" in st.session_state:
                        response = st.session_state.text_model.send_message(prompt, stream=True)
                        for chunk in response:
                            if chunk.text:
                                full_response += chunk.text
                                message_placeholder.markdown(full_response + "▌")
                        message_placeholder.markdown(full_response)
                        st.session_state.messages.append({"role": "assistant", "content": full_response})
                    else:
                        st.error("Model not initialized.")
                except Exception as e:
                    st.error(f"Error: {e}")

# --- TAB 2: Images ---
with tab2:
    st.header("Генерация Изображений")
    st.info("Используется Pollinations.ai (Бесплатно, быстро)")
    img_prompt = st.text_input("Опишите изображение", key="img_prompt")
    col1, col2 = st.columns(2)
    with col1:
        width = st.number_input("Ширина", value=1024, step=64)
    with col2:
        height = st.number_input("Высота", value=1024, step=64)

    if st.button("Сгенерировать Изображение"):
        if img_prompt:
            with st.spinner("Генерация..."):
                try:
                    img_gen = ImageGeneration()
                    url = img_gen.generate(img_prompt, width=int(width), height=int(height))
                    st.image(url, caption=img_prompt)
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.warning("Введите описание.")

# --- TAB 3: Music ---
with tab3:
    st.header("Генерация Музыки")
    st.info("Используется HuggingFace Spaces (Может быть очередь)")
    music_prompt = st.text_input("Опишите музыку", key="music_prompt")
    duration = st.slider("Длительность (сек)", 5, 30, 10)

    if st.button("Сгенерировать Музыку"):
        if music_prompt:
            with st.spinner("Генерация... (это может занять 30-60 секунд)"):
                try:
                    music_gen = MusicGeneration()
                    # Check if client init failed
                    if not music_gen.client:
                         st.error("Не удалось подключиться к сервису музыки.")
                    else:
                        result = music_gen.generate(music_prompt, duration)

                        # Handle potential error tuple return from my wrapper
                        if isinstance(result, tuple) and result[0] is None:
                            st.error(f"Error: {result[1]}")
                        else:
                            # Gradio client predict usually returns the filepath directly for audio
                            # But verify if it's a tuple (path, metadata) or just path
                            audio_path = result
                            if isinstance(result, tuple):
                                audio_path = result[0] # Assuming first element is path if it returns tuple

                            st.audio(audio_path)
                            st.success("Готово!")
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.warning("Введите описание.")

# --- TAB 4: Video ---
with tab4:
    st.header("Генерация Видео")
    st.info("Используется ModelScope (Очень ресурсоемко, может быть очередь)")
    video_prompt = st.text_input("Опишите видео (на английском лучше)", key="video_prompt")

    if st.button("Сгенерировать Видео"):
        if video_prompt:
            with st.spinner("Генерация... (это может занять несколько минут)"):
                try:
                    video_gen = VideoGeneration()
                    if not video_gen.client:
                         st.error("Не удалось подключиться к сервису видео.")
                    else:
                        result = video_gen.generate(video_prompt)

                        if isinstance(result, tuple) and result[0] is None:
                            st.error(f"Error: {result[1]}")
                        else:
                            video_path = result
                            if isinstance(result, tuple):
                                video_path = result[0]

                            st.video(video_path)
                            st.success("Готово!")
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.warning("Введите описание.")
