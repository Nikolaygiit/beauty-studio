import streamlit as st
import os

# Import modules
from modules.routing import get_route
from modules.text import create_client_and_chat, generate_text_stream
from modules.image import generate_image_url
from modules.music import generate_music
from modules.video import generate_video

# Streamlit Page Config
st.set_page_config(page_title="Gemini Ultimate Bot", page_icon="🤖", layout="wide")

st.title("🤖 Gemini Ultimate Bot")
st.markdown("Привет! Я могу общаться с тобой, а также генерировать изображения, музыку и видео по твоим запросам. Просто напиши, что тебе нужно.")

# Sidebar for API Key and Settings
st.sidebar.title("Настройки")
api_key = st.sidebar.text_input("Введи свой Google API Key", type="password")

if st.sidebar.button("Очистить историю чата"):
    st.session_state.chat_history = []
    if "chat_session" in st.session_state:
        del st.session_state.chat_session
    if "gemini_client" in st.session_state:
        del st.session_state.gemini_client
    st.rerun()

# Initialize session state for chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Update Gemini Client if API key changes
if "current_api_key" not in st.session_state or st.session_state.current_api_key != api_key:
    st.session_state.current_api_key = api_key
    if api_key:
        client, chat = create_client_and_chat(api_key)
        if client and chat:
            st.session_state.gemini_client = client
            st.session_state.chat_session = chat
            st.sidebar.success("API Key успешно подключен!")
        else:
            st.sidebar.error("Неверный API Key или ошибка подключения.")
    else:
        st.session_state.gemini_client = None
        st.session_state.chat_session = None

# Render Chat History
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
        elif message["type"] == "error":
            st.error(message["content"])

# Chat Input
if prompt := st.chat_input("Напиши сообщение..."):
    if not api_key:
        st.warning("Пожалуйста, введите Google API Key в боковой панели.")
        st.stop()

    # Display user prompt
    st.session_state.chat_history.append({"role": "user", "type": "text", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Routing
    route = get_route(prompt)

    with st.chat_message("assistant"):
        if route == "image":
            with st.spinner("Генерирую изображение..."):
                image_url = generate_image_url(prompt)
                st.image(image_url)
                st.session_state.chat_history.append({"role": "assistant", "type": "image", "content": image_url})

        elif route == "music":
            with st.spinner("Генерирую музыку..."):
                music_path, error = generate_music(prompt)
                if error:
                    st.error(error)
                    st.session_state.chat_history.append({"role": "assistant", "type": "error", "content": error})
                elif music_path:
                    st.audio(music_path)
                    st.session_state.chat_history.append({"role": "assistant", "type": "music", "content": music_path})

        elif route == "video":
            with st.spinner("Генерирую видео..."):
                video_path, error = generate_video(prompt)
                if error:
                    st.error(error)
                    st.session_state.chat_history.append({"role": "assistant", "type": "error", "content": error})
                elif video_path:
                    st.video(video_path)
                    st.session_state.chat_history.append({"role": "assistant", "type": "video", "content": video_path})

        else: # text
            if "chat_session" in st.session_state and st.session_state.chat_session:
                with st.spinner("Думаю..."):
                    # Use a placeholder for streaming
                    response_placeholder = st.empty()
                    full_response = ""
                    for chunk_text in generate_text_stream(st.session_state.chat_session, prompt):
                        full_response += chunk_text
                        response_placeholder.markdown(full_response + "▌")
                    response_placeholder.markdown(full_response)
                    st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": full_response})
            else:
                st.error("Сессия чата не инициализирована. Проверьте API Key.")
