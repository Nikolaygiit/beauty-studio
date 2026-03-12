import streamlit as st
from modules import text, image, music, video
import re

st.set_page_config(page_title="Gemini Ultimate Bot", layout="wide")
st.title("Gemini Ultimate Bot")

# Sidebar for configuration
with st.sidebar:
    st.header("Настройки")
    api_key = st.text_input("Введите ваш Google API Key", type="password")
    if st.button("Очистить историю чата"):
        st.session_state.chat_session = None
        st.session_state.messages = []
        st.rerun()

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat_session" not in st.session_state:
    st.session_state.chat_session = None

# Initialize Gemini if API key is provided
if api_key:
    text.initialize_chat(api_key)
else:
    st.warning("Пожалуйста, введите ваш Google API Key в боковой панели, чтобы начать.")

# Load resource-heavy models
music_client = music.get_music_client()
video_client = video.get_video_client()

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["type"] == "text":
            st.markdown(message["content"])
        elif message["type"] == "image":
            st.image(message["content"])
        elif message["type"] == "audio":
            st.audio(message["content"])
        elif message["type"] == "video":
            st.video(message["content"])

# Chat input
if prompt := st.chat_input("Введите сообщение..."):
    # Add user message to UI
    st.session_state.messages.append({"role": "user", "type": "text", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Route request based on keywords
    prompt_lower = prompt.lower()

    # Image Generation
    if any(prompt_lower.startswith(word) for word in ["нарисуй", "фото", "изображение"]):
        # Extract prompt text after keyword
        pattern = r"^(нарисуй|фото|изображение)\s+(.+)$"
        match = re.match(pattern, prompt, re.IGNORECASE)
        img_prompt = match.group(2) if match else prompt

        with st.chat_message("assistant"):
            with st.spinner("Генерация изображения..."):
                img_result = image.generate_image(img_prompt)
                if isinstance(img_result, str):
                    st.error(img_result)
                    st.session_state.messages.append({"role": "assistant", "type": "text", "content": img_result})
                else:
                    st.image(img_result)
                    st.session_state.messages.append({"role": "assistant", "type": "image", "content": img_result})

    # Music Generation
    elif any(prompt_lower.startswith(word) for word in ["музыка", "создай музыку", "песня"]):
        pattern = r"^(музыка|создай музыку|песня)\s+(.+)$"
        match = re.match(pattern, prompt, re.IGNORECASE)
        music_prompt = match.group(2) if match else prompt

        with st.chat_message("assistant"):
            with st.spinner("Генерация музыки..."):
                music_result = music.generate_music(music_prompt, music_client)
                if isinstance(music_result, str) and music_result.startswith("Ошибка"):
                     st.error(music_result)
                     st.session_state.messages.append({"role": "assistant", "type": "text", "content": music_result})
                else:
                    st.audio(music_result)
                    st.session_state.messages.append({"role": "assistant", "type": "audio", "content": music_result})

    # Video Generation
    elif any(prompt_lower.startswith(word) for word in ["видео", "создай видео", "сделай видео"]):
        pattern = r"^(видео|создай видео|сделай видео)\s+(.+)$"
        match = re.match(pattern, prompt, re.IGNORECASE)
        video_prompt = match.group(2) if match else prompt

        with st.chat_message("assistant"):
            with st.spinner("Генерация видео..."):
                video_result = video.generate_video(video_prompt, video_client)
                if isinstance(video_result, str) and video_result.startswith("Ошибка"):
                     st.error(video_result)
                     st.session_state.messages.append({"role": "assistant", "type": "text", "content": video_result})
                else:
                    st.video(video_result)
                    st.session_state.messages.append({"role": "assistant", "type": "video", "content": video_result})

    # Text Generation (Default)
    else:
        if not api_key:
            st.error("Пожалуйста, введите Google API Key для текстовых запросов.")
        elif st.session_state.chat_session:
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                full_response = ""
                try:
                    for chunk in text.generate_text(prompt):
                        full_response += chunk.text
                        message_placeholder.markdown(full_response + "▌")
                    message_placeholder.markdown(full_response)
                    st.session_state.messages.append({"role": "assistant", "type": "text", "content": full_response})
                except Exception as e:
                    st.error(f"Произошла ошибка: {e}")
                    st.session_state.messages.append({"role": "assistant", "type": "text", "content": f"Произошла ошибка: {e}"})
