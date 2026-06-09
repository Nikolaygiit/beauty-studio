import streamlit as st
import sys
import os

# Add the project root to sys.path so modules can be imported correctly
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gemini_bot.modules.routing import get_route
from gemini_bot.modules.image import generate_image
from gemini_bot.modules.music import generate_music
from gemini_bot.modules.video import generate_video
from gemini_bot.modules.text import init_gemini, generate_text_stream

# --- Page Config ---
st.set_page_config(page_title="Gemini Ultimate Bot", page_icon="🤖", layout="centered")

st.title("🤖 Gemini Ultimate Bot")
st.markdown("Генерация текста, изображений, музыки и видео!")

# --- Sidebar ---
st.sidebar.title("Настройки")
api_key = st.sidebar.text_input("Введите GOOGLE_API_KEY", type="password")

if st.sidebar.button("Очистить историю чата"):
    st.session_state.chat_history = []
    st.session_state.chat_session = None
    st.session_state.gemini_client = None
    st.rerun()

# --- Initialize Session State ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "current_api_key" not in st.session_state:
    st.session_state.current_api_key = None
if "chat_session" not in st.session_state:
    st.session_state.chat_session = None

# Reinitialize Gemini if API key changes
if api_key and api_key != st.session_state.current_api_key:
    st.session_state.current_api_key = api_key
    try:
        client, session = init_gemini(api_key)
        st.session_state.gemini_client = client
        st.session_state.chat_session = session
        st.sidebar.success("API ключ успешно применен!")
    except Exception as e:
        st.sidebar.error(f"Ошибка инициализации Gemini: {e}")

# --- Display Chat History ---
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        if message["type"] == "text":
            st.markdown(message["content"])
        elif message["type"] == "image":
            st.image(message["content"])
        elif message["type"] == "audio":
            st.audio(message["content"])
        elif message["type"] == "video":
            st.video(message["content"])
        elif message["type"] == "error":
            st.error(message["content"])

# --- Chat Input ---
if prompt := st.chat_input("Введите ваш запрос..."):
    if not st.session_state.chat_session:
        st.warning("Пожалуйста, введите валидный GOOGLE_API_KEY в боковой панели.")
        st.stop()

    # Append user prompt
    st.session_state.chat_history.append({"role": "user", "type": "text", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Route request
    route = get_route(prompt)

    with st.chat_message("assistant"):
        if route == "image":
            with st.spinner("Генерирую изображение..."):
                url, err = generate_image(prompt)
                if err:
                    st.error(err)
                    st.session_state.chat_history.append({"role": "assistant", "type": "error", "content": err})
                else:
                    st.image(url)
                    st.session_state.chat_history.append({"role": "assistant", "type": "image", "content": url})

        elif route == "music":
            with st.spinner("Генерирую музыку (это может занять время)..."):
                path, err = generate_music(prompt)
                if err:
                    st.error(err)
                    st.session_state.chat_history.append({"role": "assistant", "type": "error", "content": err})
                else:
                    st.audio(path)
                    st.session_state.chat_history.append({"role": "assistant", "type": "audio", "content": path})

        elif route == "video":
            with st.spinner("Генерирую видео (это может занять значительное время)..."):
                path, err = generate_video(prompt)
                if err:
                    st.error(err)
                    st.session_state.chat_history.append({"role": "assistant", "type": "error", "content": err})
                else:
                    st.video(path)
                    st.session_state.chat_history.append({"role": "assistant", "type": "video", "content": path})

        elif route == "text":
            message_placeholder = st.empty()
            full_response = ""
            for chunk in generate_text_stream(st.session_state.chat_session, prompt):
                full_response += chunk
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
            st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": full_response})
