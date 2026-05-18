import streamlit as st
import os

from modules.text import init_client, init_chat_session, generate_text_stream
from modules.image import generate_image
from modules.music import get_music_client, generate_music
from modules.video import get_video_client, generate_video

# --- UI Setup ---
st.set_page_config(page_title="Gemini Ultimate Bot", layout="wide")
st.title("Gemini Ultimate Bot")

# --- Sidebar ---
st.sidebar.title("Настройки")
api_key = st.sidebar.text_input("Введите GOOGLE_API_KEY", type="password")
clear_chat_btn = st.sidebar.button("Clear Chat History")

# --- Session State ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "chat_session" not in st.session_state:
    st.session_state.chat_session = None
if "gemini_client" not in st.session_state:
    st.session_state.gemini_client = None
if "current_api_key" not in st.session_state:
    st.session_state.current_api_key = ""

# Handle Clear Chat History
if clear_chat_btn:
    st.session_state.chat_history = []
    st.session_state.chat_session = None
    st.session_state.gemini_client = None
    st.session_state.current_api_key = ""
    st.rerun()

# --- Initialize Gemini API if Key changes ---
if api_key and api_key != st.session_state.current_api_key:
    st.session_state.current_api_key = api_key
    client, error = init_client(api_key)
    if error:
        st.sidebar.error(f"Ошибка API: {error}")
    else:
        st.session_state.gemini_client = client
        session, error = init_chat_session(client)
        if error:
            st.sidebar.error(f"Ошибка сессии: {error}")
        else:
            st.session_state.chat_session = session

# --- Caching Media Clients ---
@st.cache_resource
def load_music_client():
    return get_music_client()

@st.cache_resource
def load_video_client():
    return get_video_client()

# Prepare media clients (does not stop app if fails, will show error on prompt)
music_client, music_err = load_music_client()
video_client, video_err = load_video_client()


# --- Main Interface ---

# Display chat history
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        if msg["type"] == "text":
            st.markdown(msg["content"])
        elif msg["type"] == "image":
            st.image(msg["content"], caption="Сгенерированное изображение")
        elif msg["type"] == "music":
            st.audio(msg["content"], format="audio/wav")
        elif msg["type"] == "video":
            st.video(msg["content"])

# User Input
prompt = st.chat_input("Введите сообщение...")

if prompt:
    if not st.session_state.chat_session:
        st.error("Пожалуйста, введите валидный GOOGLE_API_KEY в боковой панели.")
    else:
        # Save user message
        st.session_state.chat_history.append({"role": "user", "type": "text", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Routing Logic
        prompt_lower = prompt.lower()
        image_keywords = ["нарисуй", "фото", "изображение"]
        music_keywords = ["музыка", "песня", "трек"]
        video_keywords = ["видео", "ролик"]

        is_image = any(kw in prompt_lower for kw in image_keywords)
        is_music = any(kw in prompt_lower for kw in music_keywords)
        is_video = any(kw in prompt_lower for kw in video_keywords)

        with st.chat_message("assistant"):
            if is_image:
                with st.spinner("Генерация изображения..."):
                    url, err = generate_image(prompt)
                    if err:
                        st.error(f"Ошибка: {err}")
                    elif url:
                        st.image(url, caption="Сгенерированное изображение")
                        st.session_state.chat_history.append({"role": "assistant", "type": "image", "content": url})

            elif is_music:
                with st.spinner("Генерация музыки..."):
                    if music_err:
                        st.error(music_err)
                    else:
                        media_path, err = generate_music(music_client, prompt)
                        if err:
                            st.error(f"Ошибка: {err}")
                        elif media_path:
                            st.audio(media_path, format="audio/wav")
                            st.session_state.chat_history.append({"role": "assistant", "type": "music", "content": media_path})

            elif is_video:
                with st.spinner("Генерация видео..."):
                    if video_err:
                        st.error(video_err)
                    else:
                        media_path, err = generate_video(video_client, prompt)
                        if err:
                            st.error(f"Ошибка: {err}")
                        elif media_path:
                            st.video(media_path)
                            st.session_state.chat_history.append({"role": "assistant", "type": "video", "content": media_path})

            else:
                # Text fallback
                with st.spinner("Генерация ответа..."):
                    try:
                        stream, err = generate_text_stream(st.session_state.chat_session, prompt)
                        if err:
                            st.error(f"Ошибка Gemini: {err}")
                        elif stream:
                            full_response = ""
                            placeholder = st.empty()
                            for chunk in stream:
                                if chunk.text:
                                    full_response += chunk.text
                                    placeholder.markdown(full_response + "▌")
                            placeholder.markdown(full_response)
                            st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": full_response})
                    except Exception as e:
                        st.error(f"Произошла непредвиденная ошибка при генерации текста: {e}")
