import streamlit as st
import os
from modules.text import init_gemini_client, init_chat_session, stream_gemini_response
from modules.image import generate_image_url
from modules.music import generate_music
from modules.video import generate_video

# --- Configure Page ---
st.set_page_config(page_title="Gemini Ultimate Bot", page_icon="🤖")

st.title("Gemini Ultimate Bot 🤖")
st.markdown("Генерация текста, изображений, музыки и видео!")

# --- Session State Management ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "gemini_client" not in st.session_state:
    st.session_state.gemini_client = None
if "chat_session" not in st.session_state:
    st.session_state.chat_session = None
if "current_api_key" not in st.session_state:
    st.session_state.current_api_key = ""

# --- Sidebar Configuration ---
with st.sidebar:
    st.header("Настройки")
    api_key_input = st.text_input("Введите ваш Google API Key", type="password", value=st.session_state.current_api_key)

    if st.button("Clear Chat History"):
        st.session_state.chat_history = []
        st.session_state.chat_session = None
        st.session_state.gemini_client = None
        st.session_state.current_api_key = ""
        st.rerun()

# Re-initialize client if API key changes
if api_key_input != st.session_state.current_api_key and api_key_input:
    client, error = init_gemini_client(api_key_input)
    if error:
        st.error(f"Ошибка инициализации клиента: {error}")
    else:
        st.session_state.gemini_client = client
        st.session_state.current_api_key = api_key_input
        chat, chat_error = init_chat_session(client)
        if chat_error:
            st.error(f"Ошибка создания сессии: {chat_error}")
        else:
            st.session_state.chat_session = chat
            st.success("API ключ успешно применен!")

# --- Main UI ---
if not st.session_state.current_api_key:
    st.warning("Пожалуйста, введите Google API Key в боковой панели.")
    st.stop()

# Display chat history
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

# Chat Input
prompt = st.chat_input("Напишите сообщение...")
if prompt:
    # 1. Add User Message
    st.session_state.chat_history.append({"role": "user", "type": "text", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Determine Intent based on Russian keywords
    prompt_lower = prompt.lower()

    with st.chat_message("assistant"):
        if any(kw in prompt_lower for kw in ['нарисуй', 'фото', 'изображение']):
            st.markdown("*Генерирую изображение...*")
            url, err = generate_image_url(prompt)
            if err:
                 st.error(err)
                 st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": err})
            else:
                 st.image(url)
                 st.session_state.chat_history.append({"role": "assistant", "type": "image", "content": url})

        elif any(kw in prompt_lower for kw in ['музыка', 'песня', 'трек']):
            st.markdown("*Генерирую музыку... (это может занять некоторое время)*")
            audio_path, err = generate_music(prompt)
            if err:
                 st.error(err)
                 st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": err})
            else:
                 st.audio(audio_path)
                 st.session_state.chat_history.append({"role": "assistant", "type": "music", "content": audio_path})

        elif any(kw in prompt_lower for kw in ['видео', 'ролик']):
            st.markdown("*Генерирую видео... (это может занять некоторое время)*")
            video_path, err = generate_video(prompt)
            if err:
                 st.error(err)
                 st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": err})
            else:
                 st.video(video_path)
                 st.session_state.chat_history.append({"role": "assistant", "type": "video", "content": video_path})

        else:
            # Default to Gemini Text Stream
            if st.session_state.chat_session:
                 response_container = st.empty()
                 full_response = ""
                 try:
                     for chunk_text in stream_gemini_response(st.session_state.chat_session, prompt):
                         full_response += chunk_text
                         response_container.markdown(full_response + "▌")
                     response_container.markdown(full_response)
                     st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": full_response})
                 except Exception as e:
                     st.error(f"Ошибка потока: {e}")
            else:
                 st.error("Сессия чата не инициализирована.")
