import streamlit as st
import sys
import os

# Ensure modules can be imported
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gemini_bot.modules import text, image, music, video

st.set_page_config(page_title="Gemini Ultimate Bot", page_icon="🤖", layout="wide")

st.title("🤖 Gemini Ultimate Bot")
st.markdown("Генерация текста, изображений, музыки и видео с использованием нейросетей!")

# --- Sidebar ---
st.sidebar.header("Настройки")
api_key = st.sidebar.text_input("Введите GOOGLE_API_KEY", type="password")

if st.sidebar.button("Очистить историю чата"):
    st.session_state.chat_history = []
    if "chat_session" in st.session_state:
        del st.session_state.chat_session
    if "gemini_client" in st.session_state:
        del st.session_state.gemini_client
    st.rerun()

# --- Session State Initialization ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "current_api_key" not in st.session_state:
    st.session_state.current_api_key = None

# Initialize/Re-initialize Gemini client if API key changes or is provided
if api_key and (st.session_state.current_api_key != api_key or "gemini_client" not in st.session_state):
    st.session_state.current_api_key = api_key
    client = text.get_client(api_key)
    st.session_state.gemini_client = client
    st.session_state.chat_session = text.init_chat(client)
    if st.session_state.chat_session is None:
        st.sidebar.error("Ошибка инициализации чата. Проверьте API ключ.")

# --- Chat Interface ---
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

# --- User Input ---
if prompt := st.chat_input("Напишите сообщение (напр. 'нарисуй кота', 'создай музыку', 'сгенерируй видео', или просто задайте вопрос)"):

    st.session_state.chat_history.append({"role": "user", "type": "text", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    prompt_lower = prompt.lower()

    # --- Image Routing ---
    if any(keyword in prompt_lower for keyword in ["нарисуй", "фото", "изображение"]):
        with st.chat_message("assistant"):
            with st.spinner("Генерация изображения..."):
                img_url = image.generate_image(prompt)
                st.image(img_url)
                st.session_state.chat_history.append({"role": "assistant", "type": "image", "content": img_url})

    # --- Music Routing ---
    elif any(keyword in prompt_lower for keyword in ["музыка", "песня", "трек"]):
        with st.chat_message("assistant"):
            with st.spinner("Генерация музыки (это может занять некоторое время)..."):
                audio_path, error = music.generate_music(prompt)
                if error:
                    st.error(error)
                    st.session_state.chat_history.append({"role": "assistant", "type": "error", "content": error})
                elif audio_path:
                    st.audio(audio_path)
                    st.session_state.chat_history.append({"role": "assistant", "type": "audio", "content": audio_path})
                else:
                    st.error("Не удалось сгенерировать аудио.")

    # --- Video Routing ---
    elif any(keyword in prompt_lower for keyword in ["видео", "ролик"]):
        with st.chat_message("assistant"):
            with st.spinner("Генерация видео (это может занять несколько минут)..."):
                video_path, error = video.generate_video(prompt)
                if error:
                    st.error(error)
                    st.session_state.chat_history.append({"role": "assistant", "type": "error", "content": error})
                elif video_path:
                    st.video(video_path)
                    st.session_state.chat_history.append({"role": "assistant", "type": "video", "content": video_path})
                else:
                    st.error("Не удалось сгенерировать видео.")

    # --- Text Routing ---
    else:
        with st.chat_message("assistant"):
            if not api_key:
                st.error("Пожалуйста, введите GOOGLE_API_KEY в боковой панели для генерации текста.")
            elif "chat_session" in st.session_state and st.session_state.chat_session:
                with st.spinner("Думаю..."):
                    # Use a placeholder to stream the text
                    placeholder = st.empty()
                    full_response = ""
                    for chunk in text.generate_text_stream(st.session_state.chat_session, prompt):
                        full_response += chunk
                        placeholder.markdown(full_response + "▌")
                    placeholder.markdown(full_response)
                    st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": full_response})
            else:
                 st.error("Чат не инициализирован. Проверьте API ключ.")
