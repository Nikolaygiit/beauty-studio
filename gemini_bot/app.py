import streamlit as st
import os

from modules.text import init_chat_session, generate_text_stream
from modules.image import generate_image_url
from modules.music import get_music_client, generate_music
from modules.video import get_video_client, generate_video

# --- Caching expensive Gradio clients ---
@st.cache_resource(show_spinner=False)
def load_music_client():
    return get_music_client()

@st.cache_resource(show_spinner=False)
def load_video_client():
    return get_video_client()

music_client = load_music_client()
video_client = load_video_client()

st.title("Gemini Ultimate Bot")
st.markdown("Генерация изображений, музыки, видео и текста с помощью Gemini-2.0-flash.")

# --- Sidebar Configuration ---
with st.sidebar:
    st.header("Настройки")
    api_key = st.text_input("Введите GOOGLE_API_KEY:", type="password")

    if st.button("Clear Chat History"):
        if "chat_history" in st.session_state:
            del st.session_state["chat_history"]
        if "chat_session" in st.session_state:
            del st.session_state["chat_session"]
        if "gemini_client" in st.session_state:
            del st.session_state["gemini_client"]
        if "current_api_key" in st.session_state:
            del st.session_state["current_api_key"]
        st.success("История чата очищена!")
        st.rerun()

# --- Initialize Session State ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "current_api_key" not in st.session_state:
    st.session_state.current_api_key = ""

# Handle API Key Changes
if api_key and api_key != st.session_state.current_api_key:
    st.session_state.current_api_key = api_key
    client, session, err = init_chat_session(api_key)
    if err:
        st.error(err)
    else:
        st.session_state.gemini_client = client
        st.session_state.chat_session = session

# --- Display Chat History ---
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        if message["type"] == "text":
            st.markdown(message["content"])
        elif message["type"] == "image":
            st.image(message["content"])
            st.markdown(f"*{message['caption']}*")
        elif message["type"] == "audio":
            st.audio(message["content"])
            st.markdown(f"*{message['caption']}*")
        elif message["type"] == "video":
            st.video(message["content"])
            st.markdown(f"*{message['caption']}*")

# --- Main Chat Input ---
prompt = st.chat_input("Спросите меня о чем-нибудь (или попросите сгенерировать фото, музыку, видео)...")

if prompt:
    # 1. Display User Message
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.chat_history.append({"role": "user", "type": "text", "content": prompt})

    # 2. Check for Keywords
    prompt_lower = prompt.lower()

    is_image = any(kw in prompt_lower for kw in ["нарисуй", "фото", "изображение"])
    is_music = any(kw in prompt_lower for kw in ["музыка", "песня", "трек"])
    is_video = any(kw in prompt_lower for kw in ["видео", "ролик"])

    # 3. Route to respective generators
    with st.chat_message("assistant"):
        if is_image:
            with st.spinner("Генерация изображения..."):
                img_url, err = generate_image_url(prompt)
                if err:
                    st.error(err)
                    st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": f"Ошибка: {err}"})
                else:
                    st.image(img_url)
                    st.session_state.chat_history.append({"role": "assistant", "type": "image", "content": img_url, "caption": prompt})

        elif is_music:
            with st.spinner("Генерация музыки (это может занять некоторое время)..."):
                audio_path, err = generate_music(music_client, prompt)
                if err:
                    st.error(err)
                    st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": f"Ошибка: {err}"})
                elif audio_path:
                    st.audio(audio_path)
                    st.session_state.chat_history.append({"role": "assistant", "type": "audio", "content": audio_path, "caption": prompt})
                else:
                     st.error("Не удалось получить аудио файл.")

        elif is_video:
            with st.spinner("Генерация видео (это может занять время)..."):
                video_path, err = generate_video(video_client, prompt)
                if err:
                    st.error(err)
                    st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": f"Ошибка: {err}"})
                elif video_path:
                    st.video(video_path)
                    st.session_state.chat_history.append({"role": "assistant", "type": "video", "content": video_path, "caption": prompt})
                else:
                     st.error("Не удалось получить видео файл.")

        else:
            # Default to Text generation
            if "chat_session" not in st.session_state:
                st.warning("Пожалуйста, введите GOOGLE_API_KEY в боковой панели.")
            else:
                response_placeholder = st.empty()
                full_response = ""
                for chunk in generate_text_stream(st.session_state.chat_session, prompt):
                    full_response += chunk
                    response_placeholder.markdown(full_response + "▌")
                response_placeholder.markdown(full_response)
                st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": full_response})