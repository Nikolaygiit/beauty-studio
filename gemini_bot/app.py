import streamlit as st
from modules.text import init_chat_session, generate_text_stream
from modules.image import generate_image_url
from modules.music import generate_music
from modules.video import generate_video
import os

st.set_page_config(page_title="Gemini Ultimate Bot", layout="wide")
st.title("Gemini Ultimate Bot")

# Sidebar configuration
with st.sidebar:
    st.header("Настройки")
    api_key = st.text_input("Введите GOOGLE_API_KEY", type="password")

    if st.button("Clear Chat History"):
        if "chat_session" in st.session_state:
            del st.session_state["chat_session"]
        st.session_state.messages = []
        st.rerun()

# Initialize session state for messages if not present
if "messages" not in st.session_state:
    st.session_state.messages = []

# Initialize Gemini chat session if API key is provided and session doesn't exist
if api_key and "chat_session" not in st.session_state:
    chat_result = init_chat_session(api_key)
    if isinstance(chat_result, str):
        st.error(chat_result)
    else:
        st.session_state.chat_session = chat_result

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["type"] == "text":
            st.markdown(message["content"])
        elif message["type"] == "image":
            st.image(message["content"])
        elif message["type"] == "music":
            st.audio(message["content"])
        elif message["type"] == "video":
            st.video(message["content"])

# User input processing
if prompt := st.chat_input("Введите сообщение..."):
    # Add user message to history and display
    st.session_state.messages.append({"role": "user", "type": "text", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    prompt_lower = prompt.lower()

    # Check for media generation keywords
    is_image = any(prompt_lower.startswith(kw) for kw in ["нарисуй", "фото", "изображение"])
    is_video = prompt_lower.startswith("видео")
    is_music = prompt_lower.startswith("музыка")

    with st.chat_message("assistant"):
        if is_image:
            # Strip keyword and generate image
            for kw in ["нарисуй", "фото", "изображение"]:
                if prompt_lower.startswith(kw):
                    clean_prompt = prompt[len(kw):].strip()
                    break

            with st.spinner("Генерация изображения..."):
                image_url = generate_image_url(clean_prompt)

            if image_url.startswith("http"):
                st.image(image_url)
                st.session_state.messages.append({"role": "assistant", "type": "image", "content": image_url})
            else:
                st.error(image_url)
                st.session_state.messages.append({"role": "assistant", "type": "text", "content": image_url})

        elif is_video:
            clean_prompt = prompt[len("видео"):].strip()
            with st.spinner("Генерация видео..."):
                video_path, error = generate_video(clean_prompt)

            if error:
                st.error(error)
                st.session_state.messages.append({"role": "assistant", "type": "text", "content": error})
            else:
                st.video(video_path)
                st.session_state.messages.append({"role": "assistant", "type": "video", "content": video_path})

        elif is_music:
            clean_prompt = prompt[len("музыка"):].strip()
            with st.spinner("Генерация музыки..."):
                music_path, error = generate_music(clean_prompt)

            if error:
                st.error(error)
                st.session_state.messages.append({"role": "assistant", "type": "text", "content": error})
            else:
                st.audio(music_path)
                st.session_state.messages.append({"role": "assistant", "type": "music", "content": music_path})

        else:
            # Text generation
            if "chat_session" not in st.session_state:
                st.error("Пожалуйста, введите GOOGLE_API_KEY в боковой панели.")
            else:
                with st.spinner("Генерация текста..."):
                    stream = generate_text_stream(st.session_state.chat_session, prompt)
                    response = st.write_stream(stream)
                st.session_state.messages.append({"role": "assistant", "type": "text", "content": response})
