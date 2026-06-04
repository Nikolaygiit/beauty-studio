import streamlit as st
from google import genai
import sys
import os

# Add the project root to the path so modules can be imported
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gemini_bot.modules import text, image, music, video, routing

st.set_page_config(page_title="Gemini Ultimate Bot", page_icon="✨")

st.title("Gemini Ultimate Bot ✨")
st.markdown("Чат-бот на базе Gemini с генерацией текста, изображений, музыки и видео.")

# Sidebar setup
with st.sidebar:
    api_key = st.text_input("Введите GOOGLE_API_KEY", type="password")
    if st.button("Очистить историю чата"):
        if "chat_history" in st.session_state:
            del st.session_state["chat_history"]
        if "chat_session" in st.session_state:
            del st.session_state["chat_session"]
        if "gemini_client" in st.session_state:
            del st.session_state["gemini_client"]
        st.rerun()

# State initialization
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "current_api_key" not in st.session_state:
    st.session_state.current_api_key = None

# Handle API key change
if api_key and api_key != st.session_state.current_api_key:
    try:
        client = genai.Client(api_key=api_key)
        chat_session = text.init_chat_session(client)
        if chat_session:
            st.session_state.gemini_client = client
            st.session_state.chat_session = chat_session
            st.session_state.current_api_key = api_key
            st.session_state.chat_history = [] # Reset history on new key
            st.success("API ключ успешно применен!")
    except Exception as e:
        st.error(f"Ошибка применения API ключа: {str(e)}")

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
        elif message["type"] == "error":
            st.error(message["content"])

# Chat input
if prompt := st.chat_input("Напишите сообщение..."):
    if not api_key:
        st.error("Пожалуйста, введите GOOGLE_API_KEY в боковой панели.")
        st.stop()

    if "chat_session" not in st.session_state:
        st.error("Сессия чата не инициализирована. Проверьте API ключ.")
        st.stop()

    # User message
    st.session_state.chat_history.append({"role": "user", "type": "text", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    route = routing.get_route(prompt)

    with st.chat_message("assistant"):
        if route == "text":
            response_stream = text.generate_text(prompt, st.session_state.gemini_client, st.session_state.chat_session)
            if response_stream:
                response_text = ""
                placeholder = st.empty()
                try:
                    for chunk in response_stream:
                        if chunk.text:
                            response_text += chunk.text
                            placeholder.markdown(response_text + "▌")
                    placeholder.markdown(response_text)
                    st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": response_text})
                except Exception as e:
                    st.error(f"Ошибка потоковой передачи: {str(e)}")
                    st.session_state.chat_history.append({"role": "assistant", "type": "error", "content": f"Ошибка потоковой передачи: {str(e)}"})
        elif route == "image":
            with st.spinner("Генерация изображения..."):
                url, error = image.generate_image(prompt)
                if url:
                    st.image(url)
                    st.session_state.chat_history.append({"role": "assistant", "type": "image", "content": url})
                else:
                    st.error(error)
                    st.session_state.chat_history.append({"role": "assistant", "type": "error", "content": error})
        elif route == "music":
            with st.spinner("Генерация музыки..."):
                audio_path, error = music.generate_music(prompt)
                if audio_path:
                    st.audio(audio_path)
                    st.session_state.chat_history.append({"role": "assistant", "type": "music", "content": audio_path})
                else:
                    st.error(error)
                    st.session_state.chat_history.append({"role": "assistant", "type": "error", "content": error})
        elif route == "video":
            with st.spinner("Генерация видео..."):
                video_path, error = video.generate_video(prompt)
                if video_path:
                    st.video(video_path)
                    st.session_state.chat_history.append({"role": "assistant", "type": "video", "content": video_path})
                else:
                    st.error(error)
                    st.session_state.chat_history.append({"role": "assistant", "type": "error", "content": error})
