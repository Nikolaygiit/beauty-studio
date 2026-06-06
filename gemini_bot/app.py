import streamlit as st
import os

from modules.routing import route_prompt
from modules.text import init_chat_session
from modules.image import generate_image
from modules.music import generate_music
from modules.video import generate_video

# --- UI Setup ---
st.set_page_config(page_title="Gemini Ultimate Bot", page_icon="🤖")
st.title("Gemini Ultimate Bot 🤖")

# --- Session State Management ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "chat_session" not in st.session_state:
    st.session_state.chat_session = None
if "gemini_client" not in st.session_state:
    st.session_state.gemini_client = None
if "current_api_key" not in st.session_state:
    st.session_state.current_api_key = ""

# --- Sidebar ---
with st.sidebar:
    st.header("Настройки")
    api_key = st.text_input("Введите GOOGLE_API_KEY", type="password", value=st.session_state.current_api_key)

    # Reinitialize session if API key changes
    if api_key != st.session_state.current_api_key:
        st.session_state.current_api_key = api_key
        st.session_state.chat_session = None
        st.session_state.gemini_client = None

    if st.button("Очистить историю чата"):
        st.session_state.chat_history = []
        st.session_state.chat_session = None
        st.session_state.gemini_client = None
        st.rerun()

# --- Initialize Chat Session ---
if api_key and not st.session_state.chat_session:
    try:
        client, chat = init_chat_session(api_key)
        st.session_state.gemini_client = client
        st.session_state.chat_session = chat
    except Exception as e:
        st.error(f"Ошибка инициализации Gemini: {e}")

# --- Display Chat History ---
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

# --- Main Chat Input Loop ---
prompt = st.chat_input("Введите запрос (текст, изображение, музыка, видео)...")

if prompt:
    if not api_key:
        st.warning("Пожалуйста, введите GOOGLE_API_KEY в боковой панели.")
    else:
        # User message
        st.session_state.chat_history.append({"role": "user", "type": "text", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Route the prompt
        route = route_prompt(prompt)

        with st.chat_message("assistant"):
            if route == "image":
                with st.spinner("Генерация изображения..."):
                    url, error = generate_image(prompt)
                    if error:
                        st.error(error)
                    else:
                        st.image(url)
                        st.session_state.chat_history.append({"role": "assistant", "type": "image", "content": url})

            elif route == "music":
                with st.spinner("Генерация музыки (это может занять некоторое время)..."):
                    path, error = generate_music(prompt)
                    if error:
                        st.error(error)
                    else:
                        st.audio(path)
                        st.session_state.chat_history.append({"role": "assistant", "type": "music", "content": path})

            elif route == "video":
                with st.spinner("Генерация видео (это может занять значительное время)..."):
                    path, error = generate_video(prompt)
                    if error:
                        st.error(error)
                    else:
                        st.video(path)
                        st.session_state.chat_history.append({"role": "assistant", "type": "video", "content": path})

            else: # text
                with st.spinner("Генерация ответа..."):
                    try:
                        response_placeholder = st.empty()
                        full_response = ""

                        # Streaming response
                        response_stream = st.session_state.chat_session.send_message_stream(prompt)
                        for chunk in response_stream:
                            if chunk.text:
                                full_response += chunk.text
                                response_placeholder.markdown(full_response + "▌")

                        response_placeholder.markdown(full_response)
                        st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": full_response})
                    except Exception as e:
                        st.error(f"Ошибка при генерации текста: {e}")
