import streamlit as st
import os

from modules.routing import get_route
from modules.text import initialize_chat_session, generate_text_stream
from modules.image import generate_image
from modules.music import generate_music
from modules.video import generate_video

# Setup Streamlit page configuration
st.set_page_config(
    page_title="Gemini Ultimate Bot",
    page_icon="🤖",
    layout="wide"
)

# Initialize Session State
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "chat_session" not in st.session_state:
    st.session_state.chat_session = None
if "gemini_client" not in st.session_state:
    st.session_state.gemini_client = None
if "current_api_key" not in st.session_state:
    st.session_state.current_api_key = ""

def clear_chat_history():
    st.session_state.chat_history = []
    st.session_state.chat_session = None
    st.session_state.gemini_client = None

# Sidebar Configuration
st.sidebar.title("Настройки ⚙️")
api_key = st.sidebar.text_input("Введите GOOGLE_API_KEY", type="password", value=st.session_state.current_api_key)

if st.sidebar.button("Очистить историю", on_click=clear_chat_history):
    pass

st.title("Gemini Ultimate Bot 🤖")
st.markdown("Генерация текста, изображений, музыки и видео!")

# Check API Key changes
if api_key != st.session_state.current_api_key:
    st.session_state.current_api_key = api_key
    st.session_state.chat_session = None # Force reinitialization

if not api_key:
    st.info("Пожалуйста, введите ваш Google API Key в боковой панели, чтобы начать.")
    st.stop()

# Initialize Gemini if needed
if st.session_state.chat_session is None:
    client, chat, error = initialize_chat_session(api_key)
    if error:
        st.error(error)
        st.stop()
    st.session_state.gemini_client = client
    st.session_state.chat_session = chat

# Display Chat History
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

# Chat Input
prompt = st.chat_input("Напишите что-нибудь...")

if prompt:
    # 1. Add user message to UI and history
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.chat_history.append({"role": "user", "type": "text", "content": prompt})

    # 2. Route prompt
    route = get_route(prompt)

    # 3. Handle specific route
    with st.chat_message("assistant"):
        if route == "text":
            response_placeholder = st.empty()
            full_response = ""
            for chunk in generate_text_stream(st.session_state.chat_session, prompt):
                full_response += chunk
                response_placeholder.markdown(full_response + "▌")
            response_placeholder.markdown(full_response)
            st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": full_response})

        elif route == "image":
            with st.spinner("Создаю изображение..."):
                url, error = generate_image(prompt)
                if error:
                    st.error(error)
                elif url:
                    st.image(url)
                    st.session_state.chat_history.append({"role": "assistant", "type": "image", "content": url})

        elif route == "music":
            with st.spinner("Создаю музыку... Это может занять некоторое время."):
                audio_path, error = generate_music(prompt)
                if error:
                    st.error(error)
                elif audio_path:
                    st.audio(audio_path)
                    st.session_state.chat_history.append({"role": "assistant", "type": "music", "content": audio_path})

        elif route == "video":
            with st.spinner("Создаю видео... Это ресурсоемкий процесс."):
                video_path, error = generate_video(prompt)
                if error:
                    st.error(error)
                elif video_path:
                    st.video(video_path)
                    st.session_state.chat_history.append({"role": "assistant", "type": "video", "content": video_path})
