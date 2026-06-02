import streamlit as st
import sys
import os

# Add the project root to sys.path so modules can be imported directly
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.routing import route_prompt
from modules.text import get_gemini_client, init_chat_session, generate_text_stream
from modules.image import generate_image
from modules.music import generate_music
from modules.video import generate_video

st.set_page_config(page_title="Gemini Ultimate Bot", page_icon="✨", layout="wide")

st.title("✨ Gemini Ultimate Bot")
st.markdown("Бот, который может генерировать текст, изображения, музыку и видео!")

# Sidebar for API Key and Settings
with st.sidebar:
    st.header("Настройки")
    api_key_input = st.text_input("Введите GOOGLE_API_KEY", type="password")

    if st.button("Очистить историю чата"):
        st.session_state.chat_history = []
        if 'chat_session' in st.session_state:
            del st.session_state.chat_session
        if 'gemini_client' in st.session_state:
            del st.session_state.gemini_client
        if 'current_api_key' in st.session_state:
            del st.session_state.current_api_key
        st.success("История очищена!")

# Initialize session state for chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Handle API Key change
if api_key_input:
    if "current_api_key" not in st.session_state or st.session_state.current_api_key != api_key_input:
        st.session_state.current_api_key = api_key_input
        st.session_state.gemini_client = get_gemini_client(api_key_input)
        st.session_state.chat_session = init_chat_session(st.session_state.gemini_client)
        # We don't clear history on API key change to preserve UX, but we have a new session backend

# Display chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        if message["type"] == "text":
            st.markdown(message["content"])
        elif message["type"] == "image":
            st.image(message["content"], caption=message.get("caption", ""))
        elif message["type"] == "music":
            st.markdown(f"**Промпт:** {message.get('caption', '')}")
            st.audio(message["content"])
        elif message["type"] == "video":
            st.markdown(f"**Промпт:** {message.get('caption', '')}")
            st.video(message["content"])

# Chat Input
if prompt := st.chat_input("Введите ваш запрос..."):
    if not api_key_input:
        st.error("Пожалуйста, введите GOOGLE_API_KEY в боковой панели.")
    else:
        # User message
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.chat_history.append({"role": "user", "type": "text", "content": prompt})

        # Route the prompt
        route = route_prompt(prompt)

        # Bot response
        with st.chat_message("assistant"):
            if route == "text":
                response_container = st.empty()
                full_response = ""
                # Streaming text
                for chunk in generate_text_stream(st.session_state.chat_session, prompt):
                    full_response += chunk
                    response_container.markdown(full_response + "▌")
                response_container.markdown(full_response)
                st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": full_response})

            elif route == "image":
                with st.spinner("Генерация изображения..."):
                    url, error = generate_image(prompt)
                    if error:
                        st.error(error)
                        st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": error})
                    elif url:
                        st.image(url, caption=prompt)
                        st.session_state.chat_history.append({"role": "assistant", "type": "image", "content": url, "caption": prompt})

            elif route == "music":
                with st.spinner("Генерация музыки (это может занять некоторое время)..."):
                    media_path, error = generate_music(prompt)
                    if error:
                        st.error(error)
                        st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": error})
                    elif media_path:
                        st.audio(media_path)
                        st.session_state.chat_history.append({"role": "assistant", "type": "music", "content": media_path, "caption": prompt})

            elif route == "video":
                with st.spinner("Генерация видео (это может занять время)..."):
                    media_path, error = generate_video(prompt)
                    if error:
                        st.error(error)
                        st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": error})
                    elif media_path:
                        st.video(media_path)
                        st.session_state.chat_history.append({"role": "assistant", "type": "video", "content": media_path, "caption": prompt})
