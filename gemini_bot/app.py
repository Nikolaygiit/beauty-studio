import streamlit as st
import os
import sys

# Ensure modules can be imported when running directly
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gemini_bot.modules import text, image, music, video

st.set_page_config(page_title="Gemini Ultimate Bot", page_icon="🤖")
st.title("Gemini Ultimate Bot 🤖")

# --- Sidebar Configuration ---
with st.sidebar:
    st.header("Настройки")
    api_key = st.text_input("Введите ваш Google API Key", type="password")

    if st.button("Очистить историю чата"):
        for key in ['chat_history', 'chat_session', 'gemini_client', 'current_api_key']:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()

# --- State Management ---
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'current_api_key' not in st.session_state:
    st.session_state.current_api_key = None
if 'chat_session' not in st.session_state:
    st.session_state.chat_session = None

# Initialize/Re-initialize Gemini if API key changes
if api_key and api_key != st.session_state.current_api_key:
    client, session = text.init_chat_session(api_key)
    if session:
        st.session_state.gemini_client = client
        st.session_state.chat_session = session
        st.session_state.current_api_key = api_key
        st.success("API Key успешно установлен!")
    else:
         st.error("Не удалось инициализировать сессию. Проверьте API Key.")

# --- Render Chat History ---
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        if message["type"] == "text":
            st.markdown(message["content"])
        elif message["type"] == "image":
            st.image(message["content"])
        elif message["type"] == "audio":
            st.audio(message["content"])
        elif message["type"] == "video":
            st.video(message["content"])

# --- Main Chat Interface ---
if prompt := st.chat_input("Введите сообщение... (добавьте 'нарисуй', 'музыка', или 'видео' для генерации медиа)"):

    if not api_key:
         st.warning("Пожалуйста, введите Google API Key в боковой панели.")
         st.stop()

    # Add user message to state and UI
    st.session_state.chat_history.append({"role": "user", "type": "text", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # --- Routing ---
    prompt_lower = prompt.lower()

    with st.chat_message("assistant"):
        # Image Routing
        if any(keyword in prompt_lower for keyword in ['нарисуй', 'фото', 'изображение']):
            with st.spinner("Генерация изображения..."):
                image_url = image.generate_image(prompt)
                st.image(image_url)
                st.session_state.chat_history.append({"role": "assistant", "type": "image", "content": image_url})

        # Music Routing
        elif any(keyword in prompt_lower for keyword in ['музыка', 'песня', 'трек']):
             with st.spinner("Генерация музыки (это может занять время)..."):
                 audio_path, error = music.generate_music(prompt)
                 if error:
                     st.error(error)
                     st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": error})
                 elif audio_path:
                     st.audio(audio_path)
                     st.session_state.chat_history.append({"role": "assistant", "type": "audio", "content": audio_path})

        # Video Routing
        elif any(keyword in prompt_lower for keyword in ['видео', 'ролик']):
             with st.spinner("Генерация видео (это может занять время)..."):
                 video_result, error = video.generate_video(prompt)
                 if error:
                     st.error(error)
                     st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": error})
                 elif video_result and len(video_result) > 0:
                     video_path = video_result[0] if isinstance(video_result, tuple) else video_result
                     st.video(video_path)
                     st.session_state.chat_history.append({"role": "assistant", "type": "video", "content": video_path})

        # Text Routing (Default)
        else:
             if st.session_state.chat_session:
                 response_stream = text.generate_text_stream(st.session_state.chat_session, prompt)
                 full_response = st.write_stream(response_stream)
                 st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": full_response})
             else:
                 st.error("Сессия чата не инициализирована.")
