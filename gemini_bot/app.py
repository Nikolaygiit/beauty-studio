import streamlit as st
import os
from modules.text import init_gemini_client, create_chat_session, generate_text_stream
from modules.image import generate_image_url
from modules.music import generate_music
from modules.video import generate_video

# --- UI Configuration ---
st.set_page_config(page_title="Gemini Ultimate Bot", page_icon="✨", layout="wide")
st.title("✨ Gemini Ultimate Bot")
st.markdown("Лучший бот на базе Gemini: текст, изображения, музыка и видео!")

# --- Sidebar & API Key ---
with st.sidebar:
    st.header("Настройки")
    api_key_input = st.text_input("Введите Google API Key:", type="password", help="Получите ключ в Google AI Studio")

    if st.button("Очистить историю чата"):
        st.session_state.chat_history = []
        st.session_state.chat_session = None
        st.session_state.gemini_client = None
        st.session_state.current_api_key = None
        st.rerun()

# --- State Management ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "current_api_key" not in st.session_state:
    st.session_state.current_api_key = None
if "gemini_client" not in st.session_state:
    st.session_state.gemini_client = None
if "chat_session" not in st.session_state:
    st.session_state.chat_session = None

# Handle API Key Change
if api_key_input and api_key_input != st.session_state.current_api_key:
    st.session_state.current_api_key = api_key_input
    st.session_state.gemini_client = init_gemini_client(api_key_input)
    if st.session_state.gemini_client:
        st.session_state.chat_session = create_chat_session(st.session_state.gemini_client)

# Require API Key
if not st.session_state.current_api_key or not st.session_state.chat_session:
    st.warning("Пожалуйста, введите ваш Google API Key в боковой панели, чтобы начать.")
    st.stop()

# --- Render Chat History ---
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        if msg.get("type") == "text":
            st.markdown(msg["content"])
        elif msg.get("type") == "image":
            st.image(msg["content"], caption=msg.get("prompt"))
        elif msg.get("type") == "music":
            st.audio(msg["content"])
            st.markdown(f"**Промпт:** {msg.get('prompt')}")
        elif msg.get("type") == "video":
            st.video(msg["content"])
            st.markdown(f"**Промпт:** {msg.get('prompt')}")

# --- Input & Routing ---
prompt = st.chat_input("Напишите сообщение (напр. 'нарисуй кота', 'создай песню', 'видео океана')...")

if prompt:
    # Add user message to history
    st.session_state.chat_history.append({"role": "user", "type": "text", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    prompt_lower = prompt.lower()

    with st.chat_message("assistant"):
        # Image Routing
        if any(keyword in prompt_lower for keyword in ['нарисуй', 'фото', 'изображение']):
            st.markdown("*Генерирую изображение...*")
            image_url = generate_image_url(prompt)
            st.image(image_url, caption=prompt)
            st.session_state.chat_history.append({"role": "assistant", "type": "image", "content": image_url, "prompt": prompt})

        # Music Routing
        elif any(keyword in prompt_lower for keyword in ['музыка', 'песня', 'трек']):
            with st.spinner("Создаю музыку... Это может занять некоторое время."):
                audio_path, error = generate_music(prompt)
                if error:
                    st.error(f"Ошибка генерации музыки: {error}")
                    st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": f"Ошибка: {error}"})
                elif audio_path:
                    st.audio(audio_path)
                    st.session_state.chat_history.append({"role": "assistant", "type": "music", "content": audio_path, "prompt": prompt})
                else:
                    st.error("Не удалось сгенерировать музыку (пустой результат).")

        # Video Routing
        elif any(keyword in prompt_lower for keyword in ['видео', 'ролик']):
            with st.spinner("Создаю видео... Это может занять несколько минут."):
                video_path, error = generate_video(prompt)
                if error:
                    st.error(f"Ошибка генерации видео: {error}")
                    st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": f"Ошибка: {error}"})
                elif video_path:
                    st.video(video_path)
                    st.session_state.chat_history.append({"role": "assistant", "type": "video", "content": video_path, "prompt": prompt})
                else:
                    st.error("Не удалось сгенерировать видео (пустой результат).")

        # Text Routing (Default)
        else:
            message_placeholder = st.empty()
            full_response = ""
            for chunk in generate_text_stream(st.session_state.chat_session, prompt):
                full_response += chunk
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
            st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": full_response})
