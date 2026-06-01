import streamlit as st

# Ensure we can import modules
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from modules.routing import get_route
from modules.text import init_chat_session, generate_text_stream
from modules.image import generate_image
from modules.music import generate_music
from modules.video import generate_video

# --- Layout & Configuration ---
st.set_page_config(
    page_title="Gemini Ultimate Bot",
    page_icon="✨",
    layout="wide"
)

st.title("✨ Gemini Ultimate Bot")
st.markdown("Генерация текста, изображений, музыки и видео!")

# --- Session State Initialization ---
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'gemini_client' not in st.session_state:
    st.session_state.gemini_client = None
if 'chat_session' not in st.session_state:
    st.session_state.chat_session = None
if 'current_api_key' not in st.session_state:
    st.session_state.current_api_key = ""

# --- Sidebar ---
with st.sidebar:
    st.header("Настройки")
    api_key = st.text_input("Введите GOOGLE_API_KEY", type="password")

    if st.button("Очистить историю"):
        st.session_state.chat_history = []
        st.session_state.gemini_client = None
        st.session_state.chat_session = None
        st.session_state.current_api_key = ""
        st.rerun()

# Re-init chat if API key changes or isn't init
if api_key and api_key != st.session_state.current_api_key:
    init_chat_session(api_key)
elif api_key and st.session_state.chat_session is None:
    init_chat_session(api_key)

# --- Chat Interface ---
# Display history
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        if msg["type"] == "text":
            st.markdown(msg["content"])
        elif msg["type"] == "image":
            st.image(msg["content"])
        elif msg["type"] == "music":
            st.audio(msg["content"])
        elif msg["type"] == "video":
            st.video(msg["content"])
        elif msg["type"] == "error":
            st.error(msg["content"])

# User Input
if prompt := st.chat_input("Введите ваш запрос..."):
    # Require API key for everything text-related (Gemini requirement)
    # Media might not strictly need it, but let's enforce API key generally or let routing handle it

    # Store user message
    st.session_state.chat_history.append({"role": "user", "type": "text", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    route = get_route(prompt)

    with st.chat_message("assistant"):
        if route == 'text':
            if not st.session_state.chat_session:
                st.error("Пожалуйста, введите ваш GOOGLE_API_KEY в боковой панели.")
                st.session_state.chat_history.append({"role": "assistant", "type": "error", "content": "API Key required."})
            else:
                placeholder = st.empty()
                full_response = ""
                for chunk in generate_text_stream(prompt, st.session_state.chat_session):
                    full_response += chunk
                    placeholder.markdown(full_response + "▌")
                placeholder.markdown(full_response)
                st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": full_response})

        elif route == 'image':
            with st.spinner("Генерация изображения..."):
                url, err = generate_image(prompt)
                if err:
                    st.error(err)
                    st.session_state.chat_history.append({"role": "assistant", "type": "error", "content": err})
                elif url:
                    st.image(url)
                    st.session_state.chat_history.append({"role": "assistant", "type": "image", "content": url})

        elif route == 'music':
            with st.spinner("Генерация музыки... это может занять минуту"):
                audio_path, err = generate_music(prompt)
                if err:
                    st.error(err)
                    st.session_state.chat_history.append({"role": "assistant", "type": "error", "content": err})
                elif audio_path:
                    st.audio(audio_path)
                    st.session_state.chat_history.append({"role": "assistant", "type": "music", "content": audio_path})

        elif route == 'video':
            with st.spinner("Генерация видео... это может занять несколько минут"):
                video_path, err = generate_video(prompt)
                if err:
                    st.error(err)
                    st.session_state.chat_history.append({"role": "assistant", "type": "error", "content": err})
                elif video_path:
                    st.video(video_path)
                    st.session_state.chat_history.append({"role": "assistant", "type": "video", "content": video_path})
