import streamlit as st
import os

from modules.text import init_gemini_client, generate_text_stream
from modules.image import generate_image
from modules.music import generate_music
from modules.video import generate_video

# UI Configuration
st.set_page_config(page_title="Gemini Ultimate Bot", page_icon="🤖")
st.title("Gemini Ultimate Bot")

# Initialize session state for chat
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "current_api_key" not in st.session_state:
    st.session_state.current_api_key = ""

def reset_chat():
    st.session_state.chat_history = []
    if "chat_session" in st.session_state:
        del st.session_state.chat_session
    if "gemini_client" in st.session_state:
        del st.session_state.gemini_client
    # Re-initialize with current key if available
    if st.session_state.current_api_key:
        init_gemini_client(st.session_state.current_api_key)

# Sidebar
with st.sidebar:
    st.header("Настройки")
    api_key = st.text_input("Введите GOOGLE_API_KEY", type="password", value=st.session_state.current_api_key)

    # Handle key change
    if api_key != st.session_state.current_api_key:
        st.session_state.current_api_key = api_key
        if api_key:
            success, error = init_gemini_client(api_key)
            if success:
                st.success("API ключ успешно применен!")
            else:
                st.error(f"Ошибка инициализации Gemini: {error}")

    if st.button("Очистить историю чата", on_click=reset_chat):
        st.success("История очищена!")

# Display chat history
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

# Chat input
if prompt := st.chat_input("Введите ваш запрос..."):
    # Require API key
    if not st.session_state.current_api_key:
        st.error("Пожалуйста, введите GOOGLE_API_KEY в боковой панели.")
        st.stop()

    # Append user message
    st.session_state.chat_history.append({"role": "user", "type": "text", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    prompt_lower = prompt.lower()

    # Routing logic
    if any(keyword in prompt_lower for keyword in ["нарисуй", "фото", "изображение"]):
        with st.chat_message("assistant"):
            with st.spinner("Генерация изображения..."):
                url, error = generate_image(prompt)
                if error:
                    st.error(error)
                    st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": error})
                else:
                    st.image(url)
                    st.session_state.chat_history.append({"role": "assistant", "type": "image", "content": url})

    elif any(keyword in prompt_lower for keyword in ["музыка", "песня", "трек"]):
        with st.chat_message("assistant"):
            with st.spinner("Генерация музыки (это может занять некоторое время)..."):
                audio_path, error = generate_music(prompt)
                if error:
                    st.error(error)
                    st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": error})
                else:
                    st.audio(audio_path)
                    st.session_state.chat_history.append({"role": "assistant", "type": "audio", "content": audio_path})

    elif any(keyword in prompt_lower for keyword in ["видео", "ролик"]):
        with st.chat_message("assistant"):
            with st.spinner("Генерация видео (это может занять продолжительное время)..."):
                video_path, error = generate_video(prompt)
                if error:
                    st.error(error)
                    st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": error})
                else:
                    st.video(video_path)
                    st.session_state.chat_history.append({"role": "assistant", "type": "video", "content": video_path})

    else:
        # Default to text generation via Gemini
        with st.chat_message("assistant"):
            stream = generate_text_stream(prompt)
            response = st.write_stream(stream)
            st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": response})
