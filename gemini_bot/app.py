import streamlit as st
import os

from modules.routing import get_route
from modules.text import get_client, initialize_chat_session, generate_text_stream
from modules.image import generate_image
from modules.music import generate_music
from modules.video import generate_video

# Streamlit App Configuration
st.set_page_config(page_title="Gemini Ultimate Bot", page_icon="🤖", layout="wide")

st.title("🤖 Gemini Ultimate Bot")
st.markdown("Добро пожаловать! Я бот, который может генерировать **текст, изображения, музыку и видео**. "
            "Просто напишите, что вы хотите сделать (например: *'нарисуй кота'*, *'песня про лето'* или *'видео космоса'*).")

# Sidebar
with st.sidebar:
    st.header("Настройки")

    # Store API key in session state
    if "current_api_key" not in st.session_state:
        st.session_state.current_api_key = ""

    api_key_input = st.text_input("Введите GOOGLE_API_KEY", type="password", value=st.session_state.current_api_key)

    # Check if API key changed
    if api_key_input != st.session_state.current_api_key:
        st.session_state.current_api_key = api_key_input
        # Reset chat session on new key
        if "chat_session" in st.session_state:
            del st.session_state.chat_session
        if "gemini_client" in st.session_state:
            del st.session_state.gemini_client

    if st.button("Clear Chat History"):
        if "chat_history" in st.session_state:
            st.session_state.chat_history = []
        if "chat_session" in st.session_state:
            del st.session_state.chat_session
        if "gemini_client" in st.session_state:
            del st.session_state.gemini_client
        st.rerun()

# Initialize history and session
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "gemini_client" not in st.session_state or st.session_state.gemini_client is None:
    st.session_state.gemini_client = get_client(st.session_state.current_api_key)

if "chat_session" not in st.session_state or st.session_state.chat_session is None:
    st.session_state.chat_session = initialize_chat_session(st.session_state.gemini_client)

# Display chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        if message["type"] == "text":
            st.markdown(message["content"])
        elif message["type"] == "image":
            st.image(message["content"], caption="Сгенерированное изображение")
        elif message["type"] == "music":
            st.audio(message["content"])
        elif message["type"] == "video":
            st.video(message["content"])
        elif message["type"] == "error":
            st.error(message["content"])

# User input
prompt = st.chat_input("Ваш запрос...")

if prompt:
    # Add user message to history
    st.session_state.chat_history.append({"role": "user", "type": "text", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    # Determine route
    route = get_route(prompt)

    with st.chat_message("assistant"):
        if route == "image":
            with st.spinner("Генерирую изображение..."):
                image_url, error = generate_image(prompt)
                if error:
                    st.error(error)
                    st.session_state.chat_history.append({"role": "assistant", "type": "error", "content": error})
                else:
                    st.image(image_url, caption="Сгенерированное изображение")
                    st.session_state.chat_history.append({"role": "assistant", "type": "image", "content": image_url})

        elif route == "music":
            with st.spinner("Генерирую музыку (может занять некоторое время)..."):
                music_path, error = generate_music(prompt)
                if error:
                    st.error(error)
                    st.session_state.chat_history.append({"role": "assistant", "type": "error", "content": error})
                else:
                    st.audio(music_path)
                    st.session_state.chat_history.append({"role": "assistant", "type": "music", "content": music_path})

        elif route == "video":
            with st.spinner("Генерирую видео (это долгий процесс, пожалуйста подождите)..."):
                video_path, error = generate_video(prompt)
                if error:
                    st.error(error)
                    st.session_state.chat_history.append({"role": "assistant", "type": "error", "content": error})
                else:
                    st.video(video_path)
                    st.session_state.chat_history.append({"role": "assistant", "type": "video", "content": video_path})

        else: # text
            if not st.session_state.current_api_key:
                err_msg = "Пожалуйста, введите GOOGLE_API_KEY в боковом меню."
                st.error(err_msg)
                st.session_state.chat_history.append({"role": "assistant", "type": "error", "content": err_msg})
            elif not st.session_state.chat_session:
                err_msg = "Ошибка инициализации сессии. Проверьте API ключ."
                st.error(err_msg)
                st.session_state.chat_history.append({"role": "assistant", "type": "error", "content": err_msg})
            else:
                response_stream = generate_text_stream(st.session_state.chat_session, prompt)
                full_response = st.write_stream(response_stream)
                st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": full_response})
