import streamlit as st
import os

# Import modules
from modules.text import get_chat_session, generate_text_stream
from modules.image import generate_image_url
from modules.music import generate_music
from modules.video import generate_video

# --- Caching Resource Heavy Models ---
@st.cache_resource(show_spinner=False)
def cached_generate_music(prompt):
    return generate_music(prompt)

@st.cache_resource(show_spinner=False)
def cached_generate_video(prompt):
    return generate_video(prompt)

# --- Configuration ---
st.set_page_config(page_title="Gemini Ultimate Bot", page_icon="🤖", layout="wide")
st.title("🤖 Gemini Ultimate Bot")
st.subheader("Генерация текста, изображений, музыки и видео")

# --- Initialize Session State ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "chat_session" not in st.session_state:
    st.session_state.chat_session = None
if "gemini_client" not in st.session_state:
    st.session_state.gemini_client = None
if "current_api_key" not in st.session_state:
    st.session_state.current_api_key = ""

# --- Sidebar ---
with st.sidebar:
    st.header("Настройки")
    api_key = st.text_input("Введите GOOGLE_API_KEY", type="password", value=st.session_state.current_api_key)

    if st.button("Очистить историю чата"):
        st.session_state.chat_history = []
        st.session_state.chat_session = None
        st.session_state.gemini_client = None
        st.session_state.current_api_key = ""
        st.rerun()

# --- Main Logic ---
if not api_key:
    st.info("Пожалуйста, введите ваш Google API Key в боковой панели, чтобы начать.")
    st.stop()

# Initialize or Re-initialize chat session if API key changes
if st.session_state.chat_session is None or api_key != st.session_state.current_api_key:
    client, chat = get_chat_session(api_key)
    if chat:
        st.session_state.gemini_client = client
        st.session_state.chat_session = chat
        st.session_state.current_api_key = api_key
        st.success("Gemini API успешно подключен!")
    else:
        st.stop()

# --- Display Chat History ---
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "image" in message:
            st.image(message["image"])
        if "audio" in message:
            st.audio(message["audio"])
        if "video" in message:
            st.video(message["video"])

# --- Chat Input ---
if prompt := st.chat_input("Напишите сообщение (для генерации медиа используйте слова: нарисуй, музыка, видео)..."):
    # Add user message to history
    st.session_state.chat_history.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        prompt_lower = prompt.lower()

        # --- Media Routing based on Russian Keywords ---

        # IMAGE GENERATION
        if any(keyword in prompt_lower for keyword in ['нарисуй', 'фото', 'изображение']):
            with st.spinner("Генерация изображения..."):
                image_url = generate_image_url(prompt)
                st.markdown("Вот ваше изображение:")
                st.image(image_url)
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": "Вот ваше изображение:",
                    "image": image_url
                })

        # MUSIC GENERATION
        elif any(keyword in prompt_lower for keyword in ['музыка', 'песня', 'трек']):
            with st.spinner("Генерация музыки (это может занять некоторое время)..."):
                audio_path, error = cached_generate_music(prompt)
                if error:
                    st.error(error)
                    st.session_state.chat_history.append({"role": "assistant", "content": error})
                elif audio_path:
                    st.markdown("Вот ваша музыка:")
                    st.audio(audio_path)
                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": "Вот ваша музыка:",
                        "audio": audio_path
                    })

        # VIDEO GENERATION
        elif any(keyword in prompt_lower for keyword in ['видео', 'ролик']):
            with st.spinner("Генерация видео (это может занять некоторое время)..."):
                video_path, error = cached_generate_video(prompt)
                if error:
                    st.error(error)
                    st.session_state.chat_history.append({"role": "assistant", "content": error})
                elif video_path:
                    st.markdown("Вот ваше видео:")
                    st.video(video_path)
                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": "Вот ваше видео:",
                        "video": video_path
                    })

        # TEXT GENERATION (Default)
        else:
            with st.spinner("Думаю..."):
                message_placeholder = st.empty()
                full_response = ""

                # Stream the response
                for chunk in generate_text_stream(st.session_state.chat_session, prompt):
                    full_response += chunk
                    message_placeholder.markdown(full_response + "▌")

                message_placeholder.markdown(full_response)

                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": full_response
                })