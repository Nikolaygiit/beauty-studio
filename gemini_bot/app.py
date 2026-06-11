import streamlit as st
import os
from modules.routing import determine_route
from modules.text import create_chat_session
from modules.image import generate_image
from modules.music import generate_music
from modules.video import generate_video

# Streamlit Page Config
st.set_page_config(
    page_title="Gemini Ultimate Bot",
    page_icon="✨",
    layout="wide"
)

# Sidebar setup
with st.sidebar:
    st.title("✨ Настройки")
    api_key_input = st.text_input("Введите GOOGLE_API_KEY", type="password", key="api_key_input")

    if st.button("Очистить историю чата", use_container_width=True):
        if "chat_history" in st.session_state:
            del st.session_state.chat_history
        if "chat_session" in st.session_state:
            del st.session_state.chat_session
        if "gemini_client" in st.session_state:
            del st.session_state.gemini_client
        st.rerun()

# State Management
if "current_api_key" not in st.session_state or st.session_state.current_api_key != api_key_input:
    st.session_state.current_api_key = api_key_input
    # Clear previous chat state if API key changes
    if "chat_history" in st.session_state:
        del st.session_state.chat_history
    if "chat_session" in st.session_state:
        del st.session_state.chat_session
    if "gemini_client" in st.session_state:
        del st.session_state.gemini_client

if not st.session_state.current_api_key:
    st.info("Пожалуйста, введите ваш Google API Key в боковой панели, чтобы начать.")
    st.stop()

# Initialize Gemini Chat
if "chat_session" not in st.session_state:
    try:
        client, chat_session = create_chat_session(st.session_state.current_api_key)
        st.session_state.gemini_client = client
        st.session_state.chat_session = chat_session
        st.session_state.chat_history = []
    except Exception as e:
        st.error(f"Ошибка при инициализации Gemini: {e}")
        st.stop()

st.title("Gemini Ultimate Bot 🤖")

# Display History
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

# User Input
if prompt := st.chat_input("Введите ваш запрос..."):
    # Add User message to history
    st.session_state.chat_history.append({"role": "user", "type": "text", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Determine route
    route = determine_route(prompt)

    with st.chat_message("assistant"):
        if route == "image":
            with st.spinner("Генерация изображения..."):
                image_url, err = generate_image(prompt)
                if err:
                    st.error(err)
                else:
                    st.image(image_url)
                    st.session_state.chat_history.append({"role": "assistant", "type": "image", "content": image_url})

        elif route == "music":
            with st.spinner("Генерация музыки... (это может занять время)"):
                audio_path, err = generate_music(prompt)
                if err:
                    st.error(err)
                elif audio_path:
                    st.audio(audio_path)
                    st.session_state.chat_history.append({"role": "assistant", "type": "audio", "content": audio_path})
                else:
                    st.error("Не удалось получить аудио.")

        elif route == "video":
            with st.spinner("Генерация видео... (это может занять время)"):
                video_path, err = generate_video(prompt)
                if err:
                    st.error(err)
                elif video_path:
                    st.video(video_path)
                    st.session_state.chat_history.append({"role": "assistant", "type": "video", "content": video_path})
                else:
                    st.error("Не удалось получить видео.")

        else: # Text Route
            with st.spinner("Думаю..."):
                try:
                    response_placeholder = st.empty()
                    full_response = ""

                    response_stream = st.session_state.chat_session.send_message_stream(prompt)
                    for chunk in response_stream:
                        if chunk.text:
                            full_response += chunk.text
                            response_placeholder.markdown(full_response + "▌")

                    response_placeholder.markdown(full_response)
                    st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": full_response})
                except Exception as e:
                    st.error(f"Ошибка при генерации текста: {e}")
