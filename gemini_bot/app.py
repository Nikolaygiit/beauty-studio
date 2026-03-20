import streamlit as st
from modules.text import get_chat_session, stream_text_response
from modules.image import generate_image
from modules.music import MusicGenerator
from modules.video import VideoGenerator

st.set_page_config(page_title="Gemini Ultimate Bot", layout="wide")

# Cache heavy initializations
@st.cache_resource
def get_music_generator():
    return MusicGenerator()

@st.cache_resource
def get_video_generator():
    return VideoGenerator()

music_gen = get_music_generator()
video_gen = get_video_generator()

st.title("Gemini Ultimate Bot")

# Sidebar
st.sidebar.title("Settings")
api_key = st.sidebar.text_input("GOOGLE_API_KEY", type="password")

if st.sidebar.button("Clear Chat History"):
    st.session_state.messages = []
    st.session_state.chat_session = None
    st.rerun()

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_session" not in st.session_state or st.session_state.chat_session is None:
    if api_key:
        st.session_state.chat_session = get_chat_session(api_key)

# Display chat messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg.get("type") == "text":
            st.markdown(msg["content"])
        elif msg.get("type") == "image":
            st.image(msg["content"], caption=msg.get("caption", ""))
        elif msg.get("type") == "audio":
            st.audio(msg["content"])
        elif msg.get("type") == "video":
            st.video(msg["content"])
        elif msg.get("type") == "error":
            st.error(msg["content"])

# Chat input
if prompt := st.chat_input("Введите сообщение (нарисуй..., музыка..., видео... для медиа):"):
    if not api_key:
        st.error("Пожалуйста, введите GOOGLE_API_KEY в боковой панели.")
        st.stop()

    st.session_state.messages.append({"role": "user", "type": "text", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    prompt_lower = prompt.lower().strip()

    with st.chat_message("assistant"):
        # Image routing
        if prompt_lower.startswith(("нарисуй", "фото", "изображение")):
            with st.spinner("Генерация изображения..."):
                img, err = generate_image(prompt)
                if err:
                    st.error(err)
                    st.session_state.messages.append({"role": "assistant", "type": "error", "content": err})
                elif img:
                    st.image(img, caption=prompt)
                    st.session_state.messages.append({"role": "assistant", "type": "image", "content": img, "caption": prompt})

        # Music routing
        elif prompt_lower.startswith(("музыка", "песня", "трек")):
            with st.spinner("Генерация музыки..."):
                audio_path, err = music_gen.generate(prompt)
                if err:
                    st.error(err)
                    st.session_state.messages.append({"role": "assistant", "type": "error", "content": err})
                elif audio_path:
                    st.audio(audio_path)
                    st.session_state.messages.append({"role": "assistant", "type": "audio", "content": audio_path})

        # Video routing
        elif prompt_lower.startswith(("видео", "ролик")):
            with st.spinner("Генерация видео..."):
                video_path, err = video_gen.generate(prompt)
                if err:
                    st.error(err)
                    st.session_state.messages.append({"role": "assistant", "type": "error", "content": err})
                elif video_path:
                    st.video(video_path)
                    st.session_state.messages.append({"role": "assistant", "type": "video", "content": video_path})

        # Text routing (fallback)
        else:
            if not st.session_state.chat_session:
                st.session_state.chat_session = get_chat_session(api_key)

            if st.session_state.chat_session:
                response = st.write_stream(stream_text_response(st.session_state.chat_session, prompt))
                st.session_state.messages.append({"role": "assistant", "type": "text", "content": response})
            else:
                st.error("Ошибка сессии чата. Проверьте API ключ.")
