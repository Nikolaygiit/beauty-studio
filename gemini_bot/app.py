import streamlit as st
import os
from modules.text import get_gemini_client, init_chat_session
from modules.image import generate_image
from modules.music import generate_music
from modules.video import generate_video
from modules.routing import route_prompt

# Page configuration
st.set_page_config(page_title="Gemini Ultimate Bot", page_icon="✨")
st.title("✨ Gemini Ultimate Bot")

# Sidebar
with st.sidebar:
    st.header("Настройки")
    api_key_input = st.text_input("Введите GOOGLE_API_KEY", type="password")

    if st.button("Clear Chat History"):
        if 'chat_history' in st.session_state:
            del st.session_state['chat_history']
        if 'chat_session' in st.session_state:
            del st.session_state['chat_session']
        if 'gemini_client' in st.session_state:
            del st.session_state['gemini_client']
        st.success("История очищена!")

# Session State Initialization
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'current_api_key' not in st.session_state:
    st.session_state.current_api_key = None

# Update client if API key changes
if api_key_input and api_key_input != st.session_state.current_api_key:
    st.session_state.current_api_key = api_key_input
    client, error = get_gemini_client(api_key_input)
    if error:
        st.sidebar.error(f"Ошибка инициализации Gemini: {error}")
    else:
        st.session_state.gemini_client = client
        chat, chat_error = init_chat_session(client)
        if chat_error:
            st.sidebar.error(f"Ошибка создания сессии: {chat_error}")
        else:
            st.session_state.chat_session = chat
            st.sidebar.success("API ключ успешно применён!")

# Main Chat Interface
if not st.session_state.current_api_key:
    st.warning("Пожалуйста, введите GOOGLE_API_KEY в боковой панели.")
    st.stop()

if 'chat_session' not in st.session_state:
    st.warning("Сессия чата не инициализирована. Проверьте API ключ.")
    st.stop()

# Render chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        if message["type"] == "text":
            st.markdown(message["content"])
        elif message["type"] == "image":
            st.image(message["media_path"], caption=message["content"])
        elif message["type"] == "music":
            st.markdown(f"**Музыка для:** {message['content']}")
            st.audio(message["media_path"])
        elif message["type"] == "video":
            st.markdown(f"**Видео для:** {message['content']}")
            st.video(message["media_path"])

# Chat Input
if prompt := st.chat_input("Введите ваш запрос..."):
    st.session_state.chat_history.append({"role": "user", "type": "text", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    media_type = route_prompt(prompt)

    with st.chat_message("assistant"):
        if media_type == 'image':
            with st.spinner("Генерация изображения..."):
                url, err = generate_image(prompt)
                if err:
                    st.error(f"Ошибка: {err}")
                elif url:
                    st.image(url, caption=prompt)
                    st.session_state.chat_history.append({"role": "assistant", "type": "image", "content": prompt, "media_path": url})

        elif media_type == 'music':
            with st.spinner("Генерация музыки (это может занять время)..."):
                path, err = generate_music(prompt)
                if err:
                    st.error(f"Ошибка: {err}")
                elif path:
                    st.audio(path)
                    st.session_state.chat_history.append({"role": "assistant", "type": "music", "content": prompt, "media_path": path})

        elif media_type == 'video':
            with st.spinner("Генерация видео (это может занять время)..."):
                path, err = generate_video(prompt)
                if err:
                    st.error(f"Ошибка: {err}")
                elif path:
                    st.video(path)
                    st.session_state.chat_history.append({"role": "assistant", "type": "video", "content": prompt, "media_path": path})

        else: # text
            with st.spinner("Думаю..."):
                try:
                    chat = st.session_state.chat_session
                    response = chat.send_message_stream(prompt)

                    placeholder = st.empty()
                    full_response = ""
                    for chunk in response:
                        if chunk.text:
                            full_response += chunk.text
                            placeholder.markdown(full_response + "▌")
                    placeholder.markdown(full_response)

                    st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": full_response})
                except Exception as e:
                    st.error(f"Ошибка генерации текста: {e}")
