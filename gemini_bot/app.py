import streamlit as st
from google import genai
import os

from modules.text import generate_text, init_chat_session
from modules.image import generate_image
from modules.music import MusicGenerator
from modules.video import VideoGenerator

st.set_page_config(page_title="Gemini Ultimate Bot", page_icon="🤖", layout="wide")

@st.cache_resource
def get_music_generator():
    return MusicGenerator()

@st.cache_resource
def get_video_generator():
    return VideoGenerator()

st.title("Gemini Ultimate Bot 🤖")
st.markdown("Генерация текста, изображений, музыки и видео!")

# Sidebar config
with st.sidebar:
    st.header("Настройки")
    api_key = st.text_input("Введите GOOGLE_API_KEY", type="password")

    if st.button("Очистить историю чата"):
        st.session_state.chat_session = None
        st.session_state.messages = []
        st.rerun()

# Initialize session state variables
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat_session" not in st.session_state:
    st.session_state.chat_session = None

# Initialize Gemini client if API key is provided
if api_key and st.session_state.chat_session is None:
    try:
        client = genai.Client(api_key=api_key)
        st.session_state.chat_session = init_chat_session(client)
    except Exception as e:
        st.error(f"Ошибка инициализации Gemini: {e}")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["type"] == "text":
            st.markdown(message["content"])
        elif message["type"] == "image":
            st.image(message["content"])
        elif message["type"] == "audio":
            if isinstance(message["content"], tuple): # musicgen streaming returns tuple
                st.audio(message["content"][0])
            else:
                st.audio(message["content"])
        elif message["type"] == "video":
            st.video(message["content"])

# Chat input
if prompt := st.chat_input("Напишите сообщение (напр. 'нарисуй кота', 'музыка для релакса', 'видео океана')..."):
    st.session_state.messages.append({"role": "user", "type": "text", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    prompt_lower = prompt.lower()

    # Image routing
    if any(keyword in prompt_lower for keyword in ['нарисуй', 'фото', 'изображение']):
        with st.chat_message("assistant"):
            with st.spinner("Генерация изображения..."):
                url = generate_image(prompt)
                st.image(url)
                st.session_state.messages.append({"role": "assistant", "type": "image", "content": url})

    # Music routing
    elif any(keyword in prompt_lower for keyword in ['музыка', 'песня', 'трек']):
        with st.chat_message("assistant"):
            with st.spinner("Генерация музыки (это может занять некоторое время)..."):
                music_gen = get_music_generator()
                result = music_gen.generate_music(prompt)
                if isinstance(result, str) and "Ошибка" in result:
                    st.error(result)
                    st.session_state.messages.append({"role": "assistant", "type": "text", "content": result})
                else:
                    audio_file = result[0] if isinstance(result, tuple) else result
                    st.audio(audio_file)
                    st.session_state.messages.append({"role": "assistant", "type": "audio", "content": result})

    # Video routing
    elif any(keyword in prompt_lower for keyword in ['видео', 'ролик']):
        with st.chat_message("assistant"):
            with st.spinner("Генерация видео (ожидайте, это ресурсоемкий процесс)..."):
                video_gen = get_video_generator()
                result = video_gen.generate_video(prompt)
                if isinstance(result, str) and "Ошибка" in result:
                    st.error(result)
                    st.session_state.messages.append({"role": "assistant", "type": "text", "content": result})
                else:
                    video_file = result[0] if isinstance(result, tuple) else result
                    st.video(video_file)
                    st.session_state.messages.append({"role": "assistant", "type": "video", "content": result})

    # Text routing
    else:
        if not api_key:
            st.warning("Пожалуйста, введите GOOGLE_API_KEY в боковой панели для генерации текста.")
        elif st.session_state.chat_session:
            with st.chat_message("assistant"):
                with st.spinner("Размышляю..."):
                    text_response = generate_text(prompt, st.session_state.chat_session)
                    st.markdown(text_response)
                    st.session_state.messages.append({"role": "assistant", "type": "text", "content": text_response})
        else:
            st.error("Сессия чата не инициализирована. Проверьте API ключ.")
