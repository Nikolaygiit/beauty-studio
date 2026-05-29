import streamlit as st
import os

from modules.routing import route_prompt
from modules.text import get_gemini_client, init_chat_session, generate_text_stream
from modules.image import generate_image
from modules.music import generate_music
from modules.video import generate_video

# --- Page Config ---
st.set_page_config(page_title="Gemini Ultimate Bot", page_icon="✨", layout="wide")
st.title("✨ Gemini Ultimate Bot")
st.caption("Чат-бот на базе Gemini 2.0 Flash. Генерирует текст, изображения, музыку и видео.")

# --- Session State Initialization ---
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
    st.header("⚙️ Настройки")
    api_key = st.text_input("Введите GOOGLE_API_KEY", type="password", value=st.session_state.current_api_key)

    if api_key != st.session_state.current_api_key:
        st.session_state.current_api_key = api_key
        st.session_state.gemini_client = get_gemini_client(api_key)
        if st.session_state.gemini_client:
            st.session_state.chat_session = init_chat_session(st.session_state.gemini_client)
            st.session_state.chat_history = []

    st.divider()

    if st.button("🗑️ Очистить историю", use_container_width=True):
        st.session_state.chat_history = []
        if st.session_state.gemini_client:
            st.session_state.chat_session = init_chat_session(st.session_state.gemini_client)
        st.rerun()

    st.divider()
    st.markdown("### Инструкция")
    st.markdown("- **Текст:** Просто общайтесь с ботом.\n- **Изображения:** Используйте слова *нарисуй, фото, изображение*.\n- **Музыка:** Используйте слова *музыка, песня, трек*.\n- **Видео:** Используйте слова *видео, ролик*.")

# --- Chat Interface ---
if not st.session_state.current_api_key:
    st.info("Пожалуйста, введите ваш Google API Key в боковой панели, чтобы начать.")
    st.stop()

if not st.session_state.chat_session:
    st.error("Ошибка инициализации сессии. Проверьте API ключ.")
    st.stop()

# Display chat history
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
prompt = st.chat_input("Введите ваше сообщение...")

if prompt:
    # 1. Add and display user message
    st.session_state.chat_history.append({"role": "user", "type": "text", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Route the prompt
    route = route_prompt(prompt)

    # 3. Handle based on route
    with st.chat_message("assistant"):
        if route == "image":
            with st.spinner("Создаю изображение..."):
                url, error = generate_image(prompt)
                if error:
                    st.error(error)
                    st.session_state.chat_history.append({"role": "assistant", "type": "error", "content": error})
                else:
                    st.image(url)
                    st.session_state.chat_history.append({"role": "assistant", "type": "image", "content": url})

        elif route == "music":
            with st.spinner("Создаю музыку... (это может занять время)"):
                media_path, error = generate_music(prompt)
                if error:
                    st.error(error)
                    st.session_state.chat_history.append({"role": "assistant", "type": "error", "content": error})
                else:
                    st.audio(media_path)
                    st.session_state.chat_history.append({"role": "assistant", "type": "music", "content": media_path})

        elif route == "video":
            with st.spinner("Создаю видео... (это может занять много времени)"):
                media_path, error = generate_video(prompt)
                if error:
                    st.error(error)
                    st.session_state.chat_history.append({"role": "assistant", "type": "error", "content": error})
                else:
                    st.video(media_path)
                    st.session_state.chat_history.append({"role": "assistant", "type": "video", "content": media_path})

        else: # Text
            with st.spinner("Печатаю..."):
                stream = generate_text_stream(st.session_state.chat_session, prompt)
                response_text = st.write_stream(stream)
                st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": response_text})
