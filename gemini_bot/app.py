import streamlit as st
from PIL import Image
import os

from modules.text import get_chat_session, generate_text_stream
from modules.image import generate_image
from modules.music import get_music_client, generate_music
from modules.video import get_video_client, generate_video

st.set_page_config(page_title="Gemini Ultimate Bot", layout="wide")

st.title("🤖 Gemini Ultimate Bot")
st.markdown("Генерация текста, изображений, фото, музыки и видео под ключ.")

# Sidebar
st.sidebar.header("Настройки")
api_key = st.sidebar.text_input("Введите GOOGLE_API_KEY", type="password")
mode = st.sidebar.selectbox("Выберите режим генерации", ["Текст", "Изображение", "Музыка", "Видео"])

if st.sidebar.button("Очистить историю чата"):
    st.session_state.messages = []
    if "chat_session" in st.session_state:
        del st.session_state["chat_session"]
    st.rerun()

# Initialize session state for messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["type"] == "text":
            st.markdown(message["content"])
        elif message["type"] == "image":
            if isinstance(message["content"], Image.Image):
                 st.image(message["content"])
            else:
                 st.error(message["content"])
        elif message["type"] == "audio":
            if isinstance(message["content"], str) and not message["content"].startswith("Ошибка"):
                 st.audio(message["content"])
            else:
                 st.error(message["content"])
        elif message["type"] == "video":
            if isinstance(message["content"], str) and not message["content"].startswith("Ошибка"):
                 st.video(message["content"])
            else:
                 st.error(message["content"])

# User input
if prompt := st.chat_input("Введите ваш запрос..."):
    # Check API key if text mode is selected
    if mode == "Текст" and not api_key:
        st.warning("Пожалуйста, введите GOOGLE_API_KEY в боковой панели.")
        st.stop()

    # Append user message
    st.session_state.messages.append({"role": "user", "type": "text", "content": prompt})

    # Process based on mode
    with st.chat_message("assistant"):
        if mode == "Текст":
            if "chat_session" not in st.session_state:
                # Need to convert streamlit history format to gemini format if needed,
                # but for simplicity we start fresh if cleared, or keep the session object.
                st.session_state.chat_session = get_chat_session(api_key, history=[])

            response_container = st.empty()
            full_response = ""
            for chunk in generate_text_stream(st.session_state.chat_session, prompt):
                full_response += chunk
                response_container.markdown(full_response + "▌")
            response_container.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "type": "text", "content": full_response})

        elif mode == "Изображение":
            with st.spinner("Генерация изображения..."):
                img = generate_image(prompt)
                if isinstance(img, Image.Image):
                    st.image(img)
                    st.session_state.messages.append({"role": "assistant", "type": "image", "content": img})
                else:
                    st.error(img)
                    st.session_state.messages.append({"role": "assistant", "type": "text", "content": img})

        elif mode == "Музыка":
            with st.spinner("Генерация музыки (это может занять время)..."):
                client = get_music_client()
                result = generate_music(prompt, client)
                if isinstance(result, str) and not result.startswith("Ошибка"):
                    st.audio(result)
                    st.session_state.messages.append({"role": "assistant", "type": "audio", "content": result})
                else:
                    st.error(result)
                    st.session_state.messages.append({"role": "assistant", "type": "text", "content": result})

        elif mode == "Видео":
            with st.spinner("Генерация видео..."):
                client = get_video_client()
                result = generate_video(prompt, client)
                if isinstance(result, str) and not result.startswith("Ошибка"):
                    st.video(result)
                    st.session_state.messages.append({"role": "assistant", "type": "video", "content": result})
                else:
                    st.error(result)
                    st.session_state.messages.append({"role": "assistant", "type": "text", "content": result})
