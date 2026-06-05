import streamlit as st
import time
from modules.routing import route_prompt
from modules.text import get_text_client, create_chat_session, generate_text_stream
from modules.image import generate_image
from modules.music import generate_music
from modules.video import generate_video

# Streamlit App Configuration
st.set_page_config(page_title="Gemini Ultimate Bot", page_icon="✨", layout="centered")

st.title("✨ Gemini Ultimate Bot")
st.markdown("Генерация текста, изображений, музыки и видео с помощью ИИ.")

# Sidebar setup
st.sidebar.title("Настройки")
api_key = st.sidebar.text_input("Введите ваш Google API Key", type="password")

def clear_chat_history():
    st.session_state.chat_history = []
    st.session_state.chat_session = None
    st.session_state.gemini_client = None
    st.session_state.current_api_key = None

st.sidebar.button("Очистить историю чата", on_click=clear_chat_history)

# Initialize Session State
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "chat_session" not in st.session_state:
    st.session_state.chat_session = None
if "gemini_client" not in st.session_state:
    st.session_state.gemini_client = None
if "current_api_key" not in st.session_state:
    st.session_state.current_api_key = None

# Update client and session if API key changes
if api_key and api_key != st.session_state.current_api_key:
    try:
        client = get_text_client(api_key)
        st.session_state.gemini_client = client
        st.session_state.chat_session = create_chat_session(client)
        st.session_state.current_api_key = api_key
    except Exception as e:
        st.sidebar.error(f"Ошибка при инициализации API: {e}")

# Display Chat History
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        if message["type"] == "text":
            st.markdown(message["content"])
        elif message["type"] == "image":
            st.image(message["content"])
        elif message["type"] == "music":
            st.audio(message["content"], format="audio/wav")
            if "prompt" in message:
                st.caption(f"Промпт: {message['prompt']}")
        elif message["type"] == "video":
            st.video(message["content"])
            if "prompt" in message:
                st.caption(f"Промпт: {message['prompt']}")
        elif message["type"] == "error":
            st.error(message["content"])

# User Input
if prompt := st.chat_input("Введите ваш запрос..."):
    # Add user message to history
    st.session_state.chat_history.append({"role": "user", "type": "text", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    route = route_prompt(prompt)

    with st.chat_message("assistant"):
        if route == 'text':
            if not st.session_state.chat_session:
                 st.error("Пожалуйста, введите Google API Key в боковой панели.")
            else:
                 with st.spinner("Генерация ответа..."):
                     stream = generate_text_stream(st.session_state.chat_session, prompt)
                     response_placeholder = st.empty()
                     full_response = ""
                     for chunk in stream:
                         full_response += chunk
                         response_placeholder.markdown(full_response + "▌")
                     response_placeholder.markdown(full_response)
                     st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": full_response})

        elif route == 'image':
             with st.spinner("Генерация изображения..."):
                  url = generate_image(prompt)
                  st.image(url)
                  st.session_state.chat_history.append({"role": "assistant", "type": "image", "content": url})

        elif route == 'music':
             with st.spinner("Генерация музыки (это может занять несколько минут)..."):
                  audio_path, error = generate_music(prompt)
                  if error:
                       st.error(error)
                       st.session_state.chat_history.append({"role": "assistant", "type": "error", "content": error})
                  else:
                       st.audio(audio_path, format="audio/wav")
                       st.session_state.chat_history.append({"role": "assistant", "type": "music", "content": audio_path, "prompt": prompt})

        elif route == 'video':
             with st.spinner("Генерация видео (это может занять несколько минут)..."):
                  video_path, error = generate_video(prompt)
                  if error:
                       st.error(error)
                       st.session_state.chat_history.append({"role": "assistant", "type": "error", "content": error})
                  else:
                       st.video(video_path)
                       st.session_state.chat_history.append({"role": "assistant", "type": "video", "content": video_path, "prompt": prompt})
