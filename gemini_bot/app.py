import streamlit as st
import os

from modules.routing import get_route
from modules.image import generate_image
from modules.music import generate_music
from modules.video import generate_video
from modules.text import get_gemini_client, init_chat_session, stream_text

st.set_page_config(page_title="Gemini Ultimate Bot", page_icon="✨")

st.title("Gemini Ultimate Bot ✨")
st.caption("Бот с генерацией текста, изображений, музыки и видео")

# Sidebar for configuration
with st.sidebar:
    st.header("Настройки")
    api_key_input = st.text_input("GOOGLE_API_KEY", type="password", key="api_key_input")

    if st.button("Очистить историю чата", type="primary"):
        st.session_state.chat_history = []
        st.session_state.chat_session = None
        st.session_state.gemini_client = None
        st.session_state.current_api_key = None
        st.rerun()

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "chat_session" not in st.session_state:
    st.session_state.chat_session = None
if "gemini_client" not in st.session_state:
    st.session_state.gemini_client = None
if "current_api_key" not in st.session_state:
    st.session_state.current_api_key = None

# Update client and chat session if API key changes
if api_key_input and api_key_input != st.session_state.current_api_key:
    client, error = get_gemini_client(api_key_input)
    if error:
        st.sidebar.error(error)
    else:
        st.session_state.gemini_client = client
        chat_session = init_chat_session(client)
        if chat_session:
            st.session_state.chat_session = chat_session
            st.session_state.current_api_key = api_key_input
            st.sidebar.success("API ключ успешно применен!")
        else:
            st.sidebar.error("Ошибка инициализации сессии чата.")

# Render chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        msg_type = message.get("type", "text")

        if msg_type == "text":
            st.markdown(message["content"])
        elif msg_type == "image":
            st.markdown(f"**Запрос:** {message['content']}")
            st.image(message["media_path"], caption=message["content"])
        elif msg_type == "music":
            st.markdown(f"**Запрос:** {message['content']}")
            st.audio(message["media_path"])
        elif msg_type == "video":
            st.markdown(f"**Запрос:** {message['content']}")
            st.video(message["media_path"])

# Main input chat box
if prompt := st.chat_input("Введите ваш запрос..."):
    # Require API key
    if not st.session_state.gemini_client or not st.session_state.chat_session:
        st.error("Пожалуйста, введите корректный GOOGLE_API_KEY в настройках.")
        st.stop()

    # Add user message to history
    st.session_state.chat_history.append({"role": "user", "content": prompt, "type": "text"})

    with st.chat_message("user"):
        st.markdown(prompt)

    route = get_route(prompt)

    with st.chat_message("assistant"):
        if route == "image":
            with st.spinner("Генерация изображения..."):
                url, error = generate_image(prompt)
                if error:
                    st.error(error)
                    st.session_state.chat_history.append({"role": "assistant", "content": error, "type": "text"})
                elif url:
                    st.image(url)
                    st.session_state.chat_history.append({"role": "assistant", "content": prompt, "type": "image", "media_path": url})

        elif route == "music":
            with st.spinner("Генерация музыки..."):
                path, error = generate_music(prompt)
                if error:
                    st.error(error)
                    st.session_state.chat_history.append({"role": "assistant", "content": error, "type": "text"})
                elif path:
                    st.audio(path)
                    st.session_state.chat_history.append({"role": "assistant", "content": prompt, "type": "music", "media_path": path})

        elif route == "video":
            with st.spinner("Генерация видео..."):
                path, error = generate_video(prompt)
                if error:
                    st.error(error)
                    st.session_state.chat_history.append({"role": "assistant", "content": error, "type": "text"})
                elif path:
                    st.video(path)
                    st.session_state.chat_history.append({"role": "assistant", "content": prompt, "type": "video", "media_path": path})

        else:
            # Text routing
            with st.spinner("Думаю..."):
                response_placeholder = st.empty()
                full_response = ""

                for chunk in stream_text(st.session_state.chat_session, prompt):
                    full_response += chunk
                    response_placeholder.markdown(full_response + "▌")

                response_placeholder.markdown(full_response)
                st.session_state.chat_history.append({"role": "assistant", "content": full_response, "type": "text"})
