import streamlit as st
import os

from modules.routing import get_route
from modules.text import get_gemini_client, get_chat_session, generate_text_stream
from modules.image import generate_image
from modules.music import get_music_client, generate_music
from modules.video import get_video_client, generate_video

# --- SETUP ---
st.set_page_config(page_title="Gemini Ultimate Bot", page_icon="🤖", layout="wide")
st.title("Gemini Ultimate Bot 🤖")

# --- INITIALIZE SESSION STATE ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "chat_session" not in st.session_state:
    st.session_state.chat_session = None
if "gemini_client" not in st.session_state:
    st.session_state.gemini_client = None
if "current_api_key" not in st.session_state:
    st.session_state.current_api_key = ""

# --- SIDEBAR ---
with st.sidebar:
    st.header("Настройки")
    api_key = st.text_input("Введите ваш Google Gemini API Key:", type="password", value=st.session_state.current_api_key)

    if st.button("Очистить историю чата"):
        st.session_state.chat_history = []
        st.session_state.chat_session = None
        st.session_state.gemini_client = None
        st.session_state.current_api_key = ""
        st.rerun()

# --- INITIALIZE / UPDATE CLIENT ---
if api_key and api_key != st.session_state.current_api_key:
    st.session_state.current_api_key = api_key
    client, error = get_gemini_client(api_key)
    if error:
        st.error(error)
    else:
        st.session_state.gemini_client = client
        st.session_state.chat_session = get_chat_session(client)
        st.success("API Key успешно установлен!")

# --- CHAT HISTORY RENDERING ---
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        if message["type"] == "text":
            st.markdown(message["content"])
        elif message["type"] == "image":
            st.markdown(message["content"])
            if "media_path" in message and message["media_path"]:
                st.image(message["media_path"])
        elif message["type"] == "music":
            st.markdown(message["content"])
            if "media_path" in message and message["media_path"]:
                st.audio(message["media_path"])
        elif message["type"] == "video":
            st.markdown(message["content"])
            if "media_path" in message and message["media_path"]:
                st.video(message["media_path"])

# --- CHAT INPUT & PROCESSING ---
prompt = st.chat_input("Введите ваш запрос...")

if prompt:
    # Check if we have the client configured
    if not st.session_state.chat_session:
        st.warning("Пожалуйста, введите ваш Google Gemini API Key в боковой панели.")
        st.stop()

    # Append user message
    st.session_state.chat_history.append({"role": "user", "type": "text", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Route request
    route = get_route(prompt)

    # Bot response
    with st.chat_message("assistant"):
        if route == "image":
            st.markdown("Генерирую изображение...")
            image_url, error = generate_image(prompt)
            if error:
                st.error(error)
                st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": error})
            else:
                st.image(image_url)
                st.session_state.chat_history.append({"role": "assistant", "type": "image", "content": f"Сгенерировано изображение по запросу: {prompt}", "media_path": image_url})

        elif route == "music":
            st.markdown("Генерирую музыку... (это может занять некоторое время)")
            client, error = get_music_client()
            if error:
                st.error(error)
                st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": error})
            else:
                with st.spinner("Создание трека..."):
                    audio_path, error = generate_music(client, prompt)
                if error:
                    st.error(error)
                    st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": error})
                else:
                    st.audio(audio_path)
                    st.session_state.chat_history.append({"role": "assistant", "type": "music", "content": f"Сгенерирована музыка по запросу: {prompt}", "media_path": audio_path})

        elif route == "video":
            st.markdown("Генерирую видео... (это может занять некоторое время)")
            client, error = get_video_client()
            if error:
                st.error(error)
                st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": error})
            else:
                with st.spinner("Создание видео..."):
                    video_path, error = generate_video(client, prompt)
                if error:
                    st.error(error)
                    st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": error})
                else:
                    st.video(video_path)
                    st.session_state.chat_history.append({"role": "assistant", "type": "video", "content": f"Сгенерировано видео по запросу: {prompt}", "media_path": video_path})

        else: # text
            response_placeholder = st.empty()
            full_response = ""
            for chunk_text in generate_text_stream(st.session_state.chat_session, prompt):
                full_response += chunk_text
                response_placeholder.markdown(full_response + "▌")
            response_placeholder.markdown(full_response)
            st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": full_response})
