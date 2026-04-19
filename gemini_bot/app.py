import streamlit as st
from gradio_client import Client
import os
import sys

# Add the project root to the path so modules can be imported correctly
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from modules.text import generate_text_stream, init_chat_session
from modules.image import generate_image
from modules.music import generate_music
from modules.video import generate_video

# Define page configuration
st.set_page_config(page_title="Gemini Ultimate Bot", page_icon="🤖")
st.title("Gemini Ultimate Bot 🤖")

# Cache gradio clients to prevent recreation on re-runs
@st.cache_resource(show_spinner=False)
def get_music_client():
    try:
        return Client("sanchit-gandhi/musicgen-streaming")
    except Exception as e:
        return str(e)

@st.cache_resource(show_spinner=False)
def get_video_client():
    try:
        return Client("damo-vilab/modelscope-text-to-video-synthesis")
    except Exception as e:
        return str(e)

# Initialize Session State
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "chat_session" not in st.session_state:
    st.session_state.chat_session = None
if "gemini_client" not in st.session_state:
    st.session_state.gemini_client = None
if "current_api_key" not in st.session_state:
    st.session_state.current_api_key = ""

# Sidebar settings
with st.sidebar:
    st.header("Настройки")
    api_key = st.text_input("Введите ваш Google API Key", type="password", value=st.session_state.current_api_key)

    # Check if API key changed
    if api_key != st.session_state.current_api_key:
        st.session_state.current_api_key = api_key
        if api_key:
            client, chat = init_chat_session(api_key)
            if chat:
                st.session_state.gemini_client = client
                st.session_state.chat_session = chat
                st.success("API Key успешно применен и сессия создана!")
            else:
                st.error("Ошибка инициализации сессии с данным API Key.")

    if st.button("Очистить историю чата"):
        st.session_state.chat_history = []
        if st.session_state.current_api_key:
             client, chat = init_chat_session(st.session_state.current_api_key)
             st.session_state.gemini_client = client
             st.session_state.chat_session = chat
        st.rerun()

# Display chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        if message["type"] == "text":
            st.markdown(message["content"])
        elif message["type"] == "image":
            st.image(message["content"])
        elif message["type"] == "music":
            st.audio(message["content"])
        elif message["type"] == "video":
            # the result might be a tuple/dict depending on gradio output, usually it's a file path
            st.video(message["content"])

# Chat input
if prompt := st.chat_input("Введите сообщение (нарисуй..., музыка..., видео...)"):
    # Add user message to history
    st.session_state.chat_history.append({"role": "user", "type": "text", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    prompt_lower = prompt.lower()

    # Keyword Routing
    if any(keyword in prompt_lower for keyword in ["нарисуй", "фото", "изображение"]):
        with st.chat_message("assistant"):
            with st.spinner("Генерация изображения..."):
                url, error = generate_image(prompt)
                if url:
                    st.image(url)
                    st.session_state.chat_history.append({"role": "assistant", "type": "image", "content": url})
                else:
                    st.error(error)
                    st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": error})

    elif any(keyword in prompt_lower for keyword in ["музыка", "песня", "трек"]):
        with st.chat_message("assistant"):
            with st.spinner("Генерация музыки..."):
                music_client = get_music_client()
                if isinstance(music_client, str): # Error during initialization
                     error_msg = f"Ошибка инициализации клиента: {music_client}"
                     st.error(error_msg)
                     st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": error_msg})
                else:
                    audio_path, error = generate_music(prompt, music_client)
                    if audio_path:
                        st.audio(audio_path)
                        st.session_state.chat_history.append({"role": "assistant", "type": "music", "content": audio_path})
                    else:
                        st.error(error)
                        st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": error})

    elif any(keyword in prompt_lower for keyword in ["видео", "ролик"]):
        with st.chat_message("assistant"):
            with st.spinner("Генерация видео..."):
                video_client = get_video_client()
                if isinstance(video_client, str):
                    error_msg = f"Ошибка инициализации клиента: {video_client}"
                    st.error(error_msg)
                    st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": error_msg})
                else:
                    video_res, error = generate_video(prompt, video_client)
                    # Video result is often a dictionary with 'video' key in Gradio or a list.
                    # Modelscope text-to-video returns a dictionary or path.
                    # Assuming standard path or Gradio output structure.
                    if video_res:
                        try:
                            # Try unpacking if it's a dict containing the file path
                            video_path = video_res['video'] if isinstance(video_res, dict) and 'video' in video_res else video_res
                            # Handle case where result might be a tuple from gradio client
                            if isinstance(video_path, tuple) or isinstance(video_path, list):
                                video_path = video_path[0]

                            if isinstance(video_path, dict) and 'video' in video_path:
                                video_path = video_path['video']

                            st.video(video_path)
                            st.session_state.chat_history.append({"role": "assistant", "type": "video", "content": video_path})
                        except Exception as e:
                            err = f"Не удалось отобразить видео. Путь: {video_res}, Ошибка: {e}"
                            st.error(err)
                            st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": err})
                    else:
                        st.error(error)
                        st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": error})

    else:
        # Default text generation using Gemini
        with st.chat_message("assistant"):
            if not st.session_state.current_api_key:
                st.warning("Пожалуйста, введите Google API Key в боковой панели.")
            elif not st.session_state.chat_session:
                st.warning("Сессия чата не инициализирована. Проверьте API Key.")
            else:
                message_placeholder = st.empty()
                full_response = ""

                # We need to manually handle exceptions here because of stream rendering
                try:
                    for chunk in generate_text_stream(prompt, st.session_state.current_api_key, st.session_state.chat_session):
                        if chunk.startswith("Произошла ошибка") or chunk.startswith("Ошибка:"):
                            full_response += chunk
                            message_placeholder.error(full_response)
                        else:
                            full_response += chunk
                            message_placeholder.markdown(full_response + "▌")
                    message_placeholder.markdown(full_response)
                    st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": full_response})
                except Exception as e:
                     error_message = f"Произошла непредвиденная ошибка: {e}"
                     st.error(error_message)
                     st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": error_message})
