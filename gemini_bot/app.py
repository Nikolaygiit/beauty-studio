import streamlit as st
import os

from modules.text import init_client, start_chat, generate_text_stream
from modules.image import generate_image
from modules.music import generate_music
from modules.video import generate_video

# Streamlit config
st.set_page_config(page_title="Gemini Ultimate Bot", layout="wide")

# Sidebar
st.sidebar.title("Настройки")
api_key = st.sidebar.text_input("Введите GOOGLE_API_KEY", type="password")

if st.sidebar.button("Clear Chat History"):
    st.session_state.chat_history = []
    st.session_state.chat_session = None
    st.session_state.gemini_client = None
    st.session_state.current_api_key = None
    st.rerun()

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "chat_session" not in st.session_state:
    st.session_state.chat_session = None
if "gemini_client" not in st.session_state:
    st.session_state.gemini_client = None
if "current_api_key" not in st.session_state:
    st.session_state.current_api_key = None

st.title("Gemini Ultimate Bot")

if not api_key:
    st.warning("Пожалуйста, введите GOOGLE_API_KEY в боковой панели.")
    st.stop()

# Cache resource-heavy generators
@st.cache_resource
def get_music_generator():
    return True # Just a placeholder since Client is init inside generate_music

@st.cache_resource
def get_video_generator():
    return True # Just a placeholder since Client is init inside generate_video

get_music_generator()
get_video_generator()

# Initialize or re-initialize client if API key changed
if st.session_state.current_api_key != api_key:
    client, err = init_client(api_key)
    if err:
        st.error(f"Ошибка инициализации: {err}")
        st.stop()
    st.session_state.gemini_client = client
    st.session_state.current_api_key = api_key

    chat_session, chat_err = start_chat(client)
    if chat_err:
        st.error(f"Ошибка создания сессии: {chat_err}")
        st.stop()
    st.session_state.chat_session = chat_session

# Display chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        if message.get("type") == "image":
            st.image(message["content"])
        elif message.get("type") == "audio":
            st.audio(message["content"])
        elif message.get("type") == "video":
            st.video(message["content"])
        else:
            st.markdown(message["content"])

# User input
prompt = st.chat_input("Введите сообщение (используйте 'нарисуй', 'фото', 'музыка', 'видео' для медиа)...")

if prompt:
    # Display user prompt
    st.session_state.chat_history.append({"role": "user", "content": prompt, "type": "text"})
    with st.chat_message("user"):
        st.markdown(prompt)

    prompt_lower = prompt.lower()

    with st.chat_message("assistant"):
        # Image routing
        if "нарисуй" in prompt_lower or "фото" in prompt_lower or "изображение" in prompt_lower:
            with st.spinner("Генерирую изображение..."):
                url, err = generate_image(prompt)
                if err:
                    st.error(err)
                    st.session_state.chat_history.append({"role": "assistant", "content": err, "type": "text"})
                elif url:
                    st.image(url)
                    st.session_state.chat_history.append({"role": "assistant", "content": url, "type": "image"})

        # Music routing
        elif "музыка" in prompt_lower or "песня" in prompt_lower or "трек" in prompt_lower:
            with st.spinner("Генерирую музыку..."):
                audio_path, err = generate_music(prompt)
                if err:
                    st.error(err)
                    st.session_state.chat_history.append({"role": "assistant", "content": err, "type": "text"})
                elif audio_path:
                    st.audio(audio_path)
                    st.session_state.chat_history.append({"role": "assistant", "content": audio_path, "type": "audio"})

        # Video routing
        elif "видео" in prompt_lower or "ролик" in prompt_lower:
            with st.spinner("Генерирую видео..."):
                video_path, err = generate_video(prompt)
                if err:
                    st.error(err)
                    st.session_state.chat_history.append({"role": "assistant", "content": err, "type": "text"})
                elif video_path:
                    st.video(video_path)
                    st.session_state.chat_history.append({"role": "assistant", "content": video_path, "type": "video"})

        # Text routing (Gemini)
        else:
            if st.session_state.chat_session:
                response_placeholder = st.empty()
                full_response = ""
                for chunk in generate_text_stream(st.session_state.chat_session, prompt):
                    if chunk:
                        full_response += chunk
                        response_placeholder.markdown(full_response + "▌")
                response_placeholder.markdown(full_response)
                st.session_state.chat_history.append({"role": "assistant", "content": full_response, "type": "text"})
            else:
                st.error("Сессия чата не инициализирована.")
