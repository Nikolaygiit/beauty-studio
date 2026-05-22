import streamlit as st
from google import genai
import os

from modules.text import initialize_chat, generate_text_stream
from modules.image import generate_image_url
from modules.music import generate_music
from modules.video import generate_video

# Streamlit App Configuration
st.set_page_config(page_title="Gemini Ultimate Bot", page_icon="🤖", layout="wide")

# Initialize session state variables
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "chat_session" not in st.session_state:
    st.session_state.chat_session = None
if "gemini_client" not in st.session_state:
    st.session_state.gemini_client = None
if "current_api_key" not in st.session_state:
    st.session_state.current_api_key = ""

# Sidebar UI
with st.sidebar:
    st.title("Настройки")
    api_key = st.text_input("Введите ваш Google API Key", type="password", value=st.session_state.current_api_key)

    if st.button("Очистить историю чата"):
        st.session_state.chat_history = []
        st.session_state.chat_session = None
        st.session_state.gemini_client = None
        st.session_state.current_api_key = ""
        st.rerun()

# Update client and chat session if API key changes
if api_key and api_key != st.session_state.current_api_key:
    try:
        client = genai.Client(api_key=api_key)
        st.session_state.gemini_client = client
        st.session_state.chat_session = initialize_chat(client)
        st.session_state.current_api_key = api_key
        st.sidebar.success("API ключ успешно установлен!")
    except Exception as e:
        st.sidebar.error(f"Ошибка инициализации Gemini: {e}")
        st.session_state.gemini_client = None
        st.session_state.chat_session = None
        st.session_state.current_api_key = ""

st.title("🤖 Gemini Ultimate Bot")
st.caption("Чат-бот с генерацией текста, изображений, музыки и видео")

if not st.session_state.current_api_key:
    st.info("Пожалуйста, введите ваш Google API Key в боковой панели, чтобы начать.")
    st.stop()

# Display chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message.get("type") == "image":
            st.image(message["media"])
        elif message.get("type") == "audio":
            st.audio(message["media"])
        elif message.get("type") == "video":
            st.video(message["media"])

# Chat input and routing
if prompt := st.chat_input("Введите ваше сообщение (или попросите 'нарисуй', 'музыка', 'видео')..."):
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        prompt_lower = prompt.lower()

        # Image routing
        if any(keyword in prompt_lower for keyword in ["нарисуй", "фото", "изображение"]):
            st.markdown(f"Генерирую изображение по запросу: *{prompt}*...")
            image_url = generate_image_url(prompt)
            st.image(image_url)
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": f"Вот ваше изображение по запросу: *{prompt}*",
                "type": "image",
                "media": image_url
            })

        # Music routing (accounting for morphology: музык, песн, трек)
        elif any(keyword in prompt_lower for keyword in ["музык", "песн", "трек"]):
            with st.spinner(f"Генерирую музыку по запросу: *{prompt}*... Это может занять некоторое время."):
                audio_path, error = generate_music(prompt)

                if error:
                    st.error(error)
                    st.session_state.chat_history.append({"role": "assistant", "content": error})
                elif audio_path:
                    st.audio(audio_path)
                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": f"Вот ваша музыка по запросу: *{prompt}*",
                        "type": "audio",
                        "media": audio_path
                    })

        # Video routing
        elif any(keyword in prompt_lower for keyword in ["видео", "ролик"]):
            with st.spinner(f"Генерирую видео по запросу: *{prompt}*... Это может занять некоторое время."):
                video_path, error = generate_video(prompt)

                if error:
                    st.error(error)
                    st.session_state.chat_history.append({"role": "assistant", "content": error})
                elif video_path:
                    st.video(video_path)
                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": f"Вот ваше видео по запросу: *{prompt}*",
                        "type": "video",
                        "media": video_path
                    })

        # Text routing (default)
        else:
            message_placeholder = st.empty()
            full_response = ""

            # Use generate_text_stream from text module
            if st.session_state.chat_session:
                for chunk_text in generate_text_stream(st.session_state.chat_session, prompt):
                    full_response += chunk_text
                    message_placeholder.markdown(full_response + "▌")

                message_placeholder.markdown(full_response)
                st.session_state.chat_history.append({"role": "assistant", "content": full_response})
            else:
                 st.error("Сессия чата не инициализирована.")
