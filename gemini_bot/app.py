import streamlit as st
import re
from modules.text import init_gemini_client
from modules.image import generate_image
from modules.music import generate_music
from modules.video import generate_video

# --- App Configuration ---
st.set_page_config(page_title="Gemini Ultimate Bot", page_icon="✨", layout="centered")

st.title("✨ Gemini Ultimate Bot")
st.markdown("Бот, который может генерировать **текст, изображения, музыку и видео**! Введите запрос.")

# --- Sidebar & Setup ---
with st.sidebar:
    st.header("Настройки")
    api_key = st.text_input("Введите GOOGLE_API_KEY", type="password")

    if st.button("Очистить историю чата"):
        for key in ["chat_history", "chat_session", "gemini_client", "current_api_key"]:
            if key in st.session_state:
                del st.session_state[key]
        st.success("История очищена!")
        st.rerun()

# --- Session State Management ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "current_api_key" not in st.session_state or st.session_state.current_api_key != api_key:
    if api_key:
        client, chat = init_gemini_client(api_key)
        if client and chat:
            st.session_state.gemini_client = client
            st.session_state.chat_session = chat
            st.session_state.current_api_key = api_key
            st.session_state.chat_history = []
    else:
        st.info("Пожалуйста, введите GOOGLE_API_KEY в боковой панели, чтобы начать.")
        st.stop()

# --- Display Chat History ---
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        if msg["type"] == "text":
            st.markdown(msg["content"])
        elif msg["type"] == "image":
            st.image(msg["content"])
        elif msg["type"] == "audio":
            st.audio(msg["content"])
        elif msg["type"] == "video":
            st.video(msg["content"])

# --- Chat Interface & Routing ---
prompt = st.chat_input("Ваш запрос (например, 'нарисуй кота' или 'сделай видео моря')")

if prompt:
    # Display user prompt
    st.session_state.chat_history.append({"role": "user", "type": "text", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    prompt_lower = prompt.lower()

    # Keyword detection
    is_image = any(kw in prompt_lower for kw in ["нарисуй", "фото", "изображение"])
    is_music = any(kw in prompt_lower for kw in ["музык", "песн", "песен", "трек"])
    is_video = any(kw in prompt_lower for kw in ["видео", "ролик"])

    with st.chat_message("assistant"):
        if is_image:
            with st.spinner("Генерирую изображение..."):
                url, err = generate_image(prompt)
                if url:
                    st.image(url)
                    st.session_state.chat_history.append({"role": "assistant", "type": "image", "content": url})
                else:
                    st.error(err)

        elif is_music:
            with st.spinner("Генерирую музыку..."):
                audio_path, err = generate_music(prompt)
                if audio_path:
                    st.audio(audio_path)
                    st.session_state.chat_history.append({"role": "assistant", "type": "audio", "content": audio_path})
                else:
                    st.error(err)

        elif is_video:
            with st.spinner("Генерирую видео..."):
                video_path, err = generate_video(prompt)
                if video_path:
                    st.video(video_path)
                    st.session_state.chat_history.append({"role": "assistant", "type": "video", "content": video_path})
                else:
                    st.error(err)

        else:
            # Text Generation
            if "chat_session" in st.session_state:
                with st.spinner("Думаю..."):
                    try:
                        response_stream = st.session_state.chat_session.send_message_stream(prompt)
                        message_placeholder = st.empty()
                        full_response = ""

                        for chunk in response_stream:
                            if chunk.text:
                                full_response += chunk.text
                                message_placeholder.markdown(full_response + "▌")

                        message_placeholder.markdown(full_response)
                        st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": full_response})
                    except Exception as e:
                        st.error(f"Ошибка при обращении к Gemini: {str(e)}")
            else:
                st.error("Чат не инициализирован. Проверьте API ключ.")
