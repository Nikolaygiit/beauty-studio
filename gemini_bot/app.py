import streamlit as st
import logging

from modules.text import init_chat_session, generate_text_stream
from modules.image import generate_image
from modules.music import MusicGenerator
from modules.video import VideoGenerator

# --- Config ---
st.set_page_config(page_title="Gemini Ultimate Bot", page_icon="✨", layout="wide")
logging.basicConfig(level=logging.INFO)

# --- Sidebar ---
with st.sidebar:
    st.title("Настройки ⚙️")
    api_key = st.text_input("Введите ваш Google API Key", type="password")

    if st.button("Очистить историю чата"):
        if "chat_session" in st.session_state:
            del st.session_state["chat_session"]
        if "messages" in st.session_state:
            st.session_state.messages = []
        st.success("История чата очищена.")

# --- Session State ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Main UI ---
st.title("Gemini Ultimate Bot ✨")
st.write("Привет! Я могу общаться с тобой, генерировать изображения, музыку и видео.")

if not api_key:
    st.warning("Пожалуйста, введите ваш Google API Key в боковом меню слева.")
    st.stop()

# Initialize Chat Session
if "chat_session" not in st.session_state:
    chat_session = init_chat_session(api_key)
    if chat_session:
        st.session_state.chat_session = chat_session
        st.success("Чат успешно инициализирован.")
    else:
        st.error("Ошибка инициализации чата. Проверьте ваш API ключ.")
        st.stop()

# --- Generators Caching ---
@st.cache_resource
def get_music_generator():
    return MusicGenerator()

@st.cache_resource
def get_video_generator():
    return VideoGenerator()

music_gen = get_music_generator()
video_gen = get_video_generator()


# --- Chat Display ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg["type"] == "text":
            st.write(msg["content"])
        elif msg["type"] == "image":
            st.image(msg["content"])
        elif msg["type"] == "audio":
            st.audio(msg["content"])
        elif msg["type"] == "video":
            st.video(msg["content"])
        elif msg["type"] == "error":
            st.error(msg["content"])

# --- User Input ---
prompt = st.chat_input("Напишите что-нибудь или попросите нарисовать, сгенерировать музыку/видео...")

if prompt:
    # Append user message
    st.session_state.messages.append({"role": "user", "type": "text", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    prompt_lower = prompt.lower()

    # Simple routing logic
    if any(prompt_lower.startswith(word) for word in ['нарисуй', 'фото', 'изображение']):
        with st.chat_message("assistant"):
            with st.spinner("Генерирую изображение... 🎨"):
                image_url = generate_image(prompt)
            if "Ошибка" in image_url:
                 st.error(image_url)
                 st.session_state.messages.append({"role": "assistant", "type": "error", "content": image_url})
            else:
                 st.image(image_url)
                 st.session_state.messages.append({"role": "assistant", "type": "image", "content": image_url})

    elif any(prompt_lower.startswith(word) for word in ['музыка', 'песня', 'трек']):
        with st.chat_message("assistant"):
            with st.spinner("Генерирую музыку... 🎵 Это может занять некоторое время."):
                audio_path = music_gen.generate(prompt)
            if "Ошибка" in audio_path:
                 st.error(audio_path)
                 st.session_state.messages.append({"role": "assistant", "type": "error", "content": audio_path})
            else:
                 st.audio(audio_path)
                 st.session_state.messages.append({"role": "assistant", "type": "audio", "content": audio_path})

    elif any(prompt_lower.startswith(word) for word in ['видео', 'ролик']):
        with st.chat_message("assistant"):
            with st.spinner("Генерирую видео... 🎬 Это может занять некоторое время."):
                video_path = video_gen.generate(prompt)
            if "Ошибка" in video_path:
                 st.error(video_path)
                 st.session_state.messages.append({"role": "assistant", "type": "error", "content": video_path})
            else:
                 st.video(video_path)
                 st.session_state.messages.append({"role": "assistant", "type": "video", "content": video_path})

    else:
        # Default Text Generation
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            for chunk in generate_text_stream(st.session_state.chat_session, prompt):
                full_response += chunk
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "type": "text", "content": full_response})
