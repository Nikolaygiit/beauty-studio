import streamlit as st
import os
from gradio_client import Client
from modules.text import get_gemini_client, init_chat_session, generate_text_stream
from modules.image import generate_image
from modules.music import generate_music
from modules.video import generate_video

# --- Caching Gradio Clients ---
@st.cache_resource
def get_music_client():
    try:
        return Client("sanchit-gandhi/musicgen-streaming")
    except Exception as e:
        return f"Ошибка инициализации музыки: {str(e)}"

@st.cache_resource
def get_video_client():
    try:
        return Client("damo-vilab/modelscope-text-to-video-synthesis")
    except Exception as e:
        if "RUNTIME_ERROR" in str(e):
            return "Ошибка инициализации видео: Сервис временно недоступен (RUNTIME_ERROR)."
        return f"Ошибка инициализации видео: {str(e)}"

# --- Initialize App ---
st.set_page_config(page_title="Gemini Ultimate Bot", page_icon="🤖")
st.title("🤖 Gemini Ultimate Bot")

# --- Sidebar ---
st.sidebar.title("Настройки")
api_key = st.sidebar.text_input("Введите GOOGLE API KEY", type="password")

if st.sidebar.button("Очистить историю чата"):
    st.session_state.chat_history = []
    st.session_state.chat_session = None
    st.session_state.gemini_client = None
    st.session_state.current_api_key = None
    st.rerun()

# --- Session State ---
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'current_api_key' not in st.session_state:
    st.session_state.current_api_key = None

# Update client and chat session if API key changes
if api_key and api_key != st.session_state.current_api_key:
    try:
        client = get_gemini_client(api_key)
        st.session_state.gemini_client = client
        st.session_state.chat_session = init_chat_session(client)
        st.session_state.current_api_key = api_key
        st.sidebar.success("API ключ успешно применен!")
    except Exception as e:
        st.sidebar.error(f"Ошибка API ключа: {str(e)}")
        st.session_state.current_api_key = None

# --- Main Chat UI ---
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if "media_type" in msg and "media_url" in msg:
            if msg["media_type"] == "image":
                st.image(msg["media_url"])
            elif msg["media_type"] == "audio":
                st.audio(msg["media_url"])
            elif msg["media_type"] == "video":
                st.video(msg["media_url"])

# --- User Input ---
prompt = st.chat_input("Введите сообщение (например: нарисуй кота, музыка для сна, видео космоса)")

if prompt:
    if not api_key:
        st.error("Пожалуйста, введите GOOGLE API KEY в боковой панели.")
    else:
        # Display user prompt
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Routing based on keywords
        prompt_lower = prompt.lower()

        if any(keyword in prompt_lower for keyword in ["нарисуй", "фото", "изображение"]):
            with st.chat_message("assistant"):
                with st.spinner("Генерация изображения..."):
                    img_url = generate_image(prompt)
                    st.markdown("Вот ваше изображение:")
                    st.image(img_url)
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": "Вот ваше изображение:",
                "media_type": "image",
                "media_url": img_url
            })

        elif any(keyword in prompt_lower for keyword in ["музыка", "песня", "трек"]):
            with st.chat_message("assistant"):
                with st.spinner("Генерация музыки..."):
                    music_client = get_music_client()
                    if isinstance(music_client, str): # Handle initialization error
                        st.error(music_client)
                        st.session_state.chat_history.append({"role": "assistant", "content": music_client})
                    else:
                        audio_res = generate_music(prompt, music_client)
                        if "Ошибка" in audio_res:
                            st.error(audio_res)
                            st.session_state.chat_history.append({"role": "assistant", "content": audio_res})
                        else:
                            st.markdown("Вот ваша музыка:")
                            st.audio(audio_res)
                            st.session_state.chat_history.append({
                                "role": "assistant",
                                "content": "Вот ваша музыка:",
                                "media_type": "audio",
                                "media_url": audio_res
                            })

        elif any(keyword in prompt_lower for keyword in ["видео", "ролик"]):
            with st.chat_message("assistant"):
                with st.spinner("Генерация видео..."):
                    video_client = get_video_client()
                    if isinstance(video_client, str): # Handle initialization error
                        st.error(video_client)
                        st.session_state.chat_history.append({"role": "assistant", "content": video_client})
                    else:
                        video_res = generate_video(prompt, video_client)
                        if "Ошибка" in video_res:
                            st.error(video_res)
                            st.session_state.chat_history.append({"role": "assistant", "content": video_res})
                        else:
                            st.markdown("Вот ваше видео:")
                            st.video(video_res)
                            st.session_state.chat_history.append({
                                "role": "assistant",
                                "content": "Вот ваше видео:",
                                "media_type": "video",
                                "media_url": video_res
                            })

        else:
            # Standard Text Generation
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                full_response = ""

                try:
                    if st.session_state.chat_session is None:
                        client = get_gemini_client(api_key)
                        st.session_state.gemini_client = client
                        st.session_state.chat_session = init_chat_session(client)

                    stream = generate_text_stream(st.session_state.chat_session, prompt)
                    for chunk in stream:
                        full_response += chunk
                        message_placeholder.markdown(full_response + "▌")
                    message_placeholder.markdown(full_response)
                except Exception as e:
                    full_response = f"Ошибка: {str(e)}"
                    message_placeholder.error(full_response)

            st.session_state.chat_history.append({"role": "assistant", "content": full_response})
