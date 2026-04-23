import streamlit as st
import os

from modules.text import init_chat_session, generate_text_stream
from modules.image import generate_image
from modules.music import generate_music
from modules.video import generate_video

# Streamlit App Configuration
st.set_page_config(page_title="Gemini Ultimate Bot", page_icon="🤖", layout="wide")

st.title("🤖 Gemini Ultimate Bot")
st.markdown("Добро пожаловать! Я могу генерировать текст, изображения, музыку и видео. "
            "Для изображений используйте слова: 'нарисуй', 'фото', 'изображение'. "
            "Для музыки: 'музыка', 'песня', 'трек'. "
            "Для видео: 'видео', 'ролик'.")

# Initialize session state for api key, chat history and Gemini client
if "current_api_key" not in st.session_state:
    st.session_state.current_api_key = ""
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "chat_session" not in st.session_state:
    st.session_state.chat_session = None
if "gemini_client" not in st.session_state:
    st.session_state.gemini_client = None

# Sidebar for settings and clear history
with st.sidebar:
    st.header("Настройки")
    api_key_input = st.text_input("Введите GOOGLE_API_KEY", type="password", value=st.session_state.current_api_key)

    if api_key_input and api_key_input != st.session_state.current_api_key:
        st.session_state.current_api_key = api_key_input
        # Re-initialize Gemini client
        client, chat = init_chat_session(api_key_input)
        if client and chat:
            st.session_state.gemini_client = client
            st.session_state.chat_session = chat
            st.success("API ключ успешно применен!")

    if st.button("Очистить историю чата"):
        st.session_state.chat_history = []
        if st.session_state.current_api_key:
            client, chat = init_chat_session(st.session_state.current_api_key)
            st.session_state.gemini_client = client
            st.session_state.chat_session = chat
        st.rerun()

# Check if API Key is configured for text generation
if not st.session_state.current_api_key:
    st.warning("Пожалуйста, введите GOOGLE_API_KEY в боковом меню для работы текстовой модели.")

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
        elif message["type"] == "error":
            st.error(message["content"])

# Chat input
prompt = st.chat_input("Введите ваш запрос...")

if prompt:
    # Add user message to chat
    st.session_state.chat_history.append({"role": "user", "type": "text", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    prompt_lower = prompt.lower()

    # Keyword Routing
    if any(keyword in prompt_lower for keyword in ['нарисуй', 'фото', 'изображение']):
        with st.chat_message("assistant"):
            with st.spinner("Рисую изображение..."):
                url, error = generate_image(prompt)
                if error:
                    st.error(error)
                    st.session_state.chat_history.append({"role": "assistant", "type": "error", "content": error})
                elif url:
                    st.image(url)
                    st.session_state.chat_history.append({"role": "assistant", "type": "image", "content": url})

    elif any(keyword in prompt_lower for keyword in ['музыка', 'песня', 'трек']):
        with st.chat_message("assistant"):
            with st.spinner("Создаю музыку..."):
                audio_path, error = generate_music(prompt)
                if error:
                    st.error(error)
                    st.session_state.chat_history.append({"role": "assistant", "type": "error", "content": error})
                elif audio_path:
                    st.audio(audio_path)
                    st.session_state.chat_history.append({"role": "assistant", "type": "audio", "content": audio_path})

    elif any(keyword in prompt_lower for keyword in ['видео', 'ролик']):
        with st.chat_message("assistant"):
            with st.spinner("Генерирую видео..."):
                video_path, error = generate_video(prompt)
                if error:
                    st.error(error)
                    st.session_state.chat_history.append({"role": "assistant", "type": "error", "content": error})
                elif video_path:
                    st.video(video_path)
                    st.session_state.chat_history.append({"role": "assistant", "type": "video", "content": video_path})

    else:
        # Default to text generation
        if not st.session_state.chat_session:
            with st.chat_message("assistant"):
                st.error("Пожалуйста, введите GOOGLE_API_KEY для текстовых запросов.")
        else:
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                full_response = ""
                # Streaming response
                for chunk in generate_text_stream(st.session_state.chat_session, prompt):
                    full_response += chunk
                    message_placeholder.markdown(full_response + "▌")
                message_placeholder.markdown(full_response)
                st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": full_response})