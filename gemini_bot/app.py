import streamlit as st
from modules.text import get_gemini_client, get_chat_session, generate_text_stream
from modules.image import generate_image_url
from modules.music import get_music_client, generate_music
from modules.video import get_video_client, generate_video

# --- Layout and Configuration ---
st.set_page_config(page_title="Gemini Ultimate Bot", page_icon="✨", layout="centered")

st.title("✨ Gemini Ultimate Bot")
st.markdown("Ваш умный помощник для генерации текста, изображений, музыки и видео!")

# --- Sidebar Configuration ---
with st.sidebar:
    st.header("Настройки")
    api_key = st.text_input("Введите ваш Google API Key", type="password")

    if st.button("Очистить историю чата"):
        st.session_state.chat_history = []
        st.session_state.chat_session = None
        st.session_state.gemini_client = None
        st.session_state.current_api_key = None
        st.rerun()

# --- Session State Initialization ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "current_api_key" not in st.session_state:
    st.session_state.current_api_key = None

# Re-initialize client if API key changes
if api_key and api_key != st.session_state.current_api_key:
    st.session_state.current_api_key = api_key
    try:
        st.session_state.gemini_client = get_gemini_client(api_key)
        st.session_state.chat_session = get_chat_session(st.session_state.gemini_client)
    except Exception as e:
        st.sidebar.error(f"Ошибка инициализации: {e}")

# --- Initialize Resource Heavy Clients ---
music_client = get_music_client()
video_client = get_video_client()

# --- Main Chat UI ---
# Display history
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

        # Display rich media if present
        if "media_type" in msg:
            if msg["media_type"] == "image":
                st.image(msg["media_content"])
            elif msg["media_type"] == "audio":
                st.audio(msg["media_content"])
            elif msg["media_type"] == "video":
                st.video(msg["media_content"])

# User input handling
if prompt := st.chat_input("Напишите сообщение (напр., 'нарисуй кота', 'музыка для релакса', 'видео океана')"):

    if not api_key:
        st.error("Пожалуйста, введите Google API Key в боковой панели!")
        st.stop()

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.chat_history.append({"role": "user", "content": prompt})

    # Routing logic
    prompt_lower = prompt.lower()

    with st.chat_message("assistant"):
        message_placeholder = st.empty()

        # IMAGE ROUTING
        if any(kw in prompt_lower for kw in ['нарисуй', 'фото', 'изображение']):
            st.markdown("Генерация изображения...")
            img_url = generate_image_url(prompt)
            st.image(img_url)
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": "Вот ваше изображение:",
                "media_type": "image",
                "media_content": img_url
            })

        # MUSIC ROUTING
        elif any(kw in prompt_lower for kw in ['музыка', 'песня', 'трек']):
            st.markdown("Генерация музыки (это может занять некоторое время)...")
            audio_path, error = generate_music(music_client, prompt)
            if error:
                st.error(f"Ошибка генерации музыки: {error}")
                st.session_state.chat_history.append({"role": "assistant", "content": f"Ошибка: {error}"})
            else:
                st.audio(audio_path)
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": "Вот ваша музыка:",
                    "media_type": "audio",
                    "media_content": audio_path
                })

        # VIDEO ROUTING
        elif any(kw in prompt_lower for kw in ['видео', 'ролик']):
            st.markdown("Генерация видео (это может занять некоторое время)...")
            video_path, error = generate_video(video_client, prompt)
            if error:
                st.error(f"Ошибка генерации видео: {error}")
                st.session_state.chat_history.append({"role": "assistant", "content": f"Ошибка: {error}"})
            else:
                st.video(video_path)
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": "Вот ваше видео:",
                    "media_type": "video",
                    "media_content": video_path
                })

        # TEXT ROUTING
        else:
            if not st.session_state.chat_session:
                st.error("Чат сессия не инициализирована.")
                st.stop()

            full_response = ""
            for chunk_text in generate_text_stream(st.session_state.chat_session, prompt):
                full_response += chunk_text
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)

            st.session_state.chat_history.append({"role": "assistant", "content": full_response})
