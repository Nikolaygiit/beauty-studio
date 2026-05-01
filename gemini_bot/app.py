import streamlit as st
from modules.text import get_gemini_client_and_chat, generate_text_stream
from modules.image import generate_image
from modules.music import generate_music
from modules.video import generate_video

# Page configuration
st.set_page_config(page_title="Gemini Ultimate Bot", page_icon="🤖", layout="wide")

st.title("Gemini Ultimate Bot 🤖")
st.markdown("Умный бот на базе Gemini 2.0 с возможностью генерации текста, картинок, музыки и видео.")

# --- Sidebar ---
with st.sidebar:
    st.header("Настройки")
    api_key = st.text_input("Введите GOOGLE_API_KEY", type="password", key="api_key_input")

    if st.button("Очистить историю чата", use_container_width=True):
        st.session_state.chat_history = []
        st.session_state.chat_session = None
        st.session_state.gemini_client = None
        st.session_state.current_api_key = None
        st.rerun()

    st.markdown("---")
    st.markdown("""
    **Подсказки по генерации:**
    *   **Фото/Картинки:** используйте слова "нарисуй", "фото" или "изображение".
    *   **Музыка/Треки:** используйте слова "музыка", "песня" или "трек".
    *   **Видео:** используйте слова "видео" или "ролик".
    *   В остальных случаях ответит текст от Gemini.
    """)

# --- State Initialization ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "current_api_key" not in st.session_state:
    st.session_state.current_api_key = None

# Re-initialize Gemini if API key changes or isn't set yet
if api_key and api_key != st.session_state.current_api_key:
    client, chat = get_gemini_client_and_chat(api_key)
    if chat:
        st.session_state.gemini_client = client
        st.session_state.chat_session = chat
        st.session_state.current_api_key = api_key
        # Keep history, but chat session is new (to allow key change without losing UI history)

# --- Display Chat History ---
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        if msg["type"] == "text":
            st.markdown(msg["content"])
        elif msg["type"] == "image":
            st.image(msg["content"], caption=msg.get("caption", "Сгенерированное изображение"))
        elif msg["type"] == "audio":
            st.audio(msg["content"])
        elif msg["type"] == "video":
            st.video(msg["content"])
        elif msg["type"] == "error":
            st.error(msg["content"])

# --- Chat Input ---
if prompt := st.chat_input("Напишите ваш запрос..."):
    # Add user message to history
    st.session_state.chat_history.append({"role": "user", "type": "text", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    # Check for keywords
    prompt_lower = prompt.lower()

    with st.chat_message("assistant"):
        # IMAGE ROUTING
        if any(keyword in prompt_lower for keyword in ["нарисуй", "фото", "изображение"]):
            with st.spinner("Создаю изображение..."):
                image_url = generate_image(prompt)
                st.image(image_url, caption=prompt)
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "type": "image",
                    "content": image_url,
                    "caption": prompt
                })

        # MUSIC ROUTING
        elif any(keyword in prompt_lower for keyword in ["музыка", "песня", "трек"]):
            with st.spinner("Сочиняю музыку (это может занять время)..."):
                audio_path, error = generate_music(prompt)
                if error:
                    st.error(error)
                    st.session_state.chat_history.append({"role": "assistant", "type": "error", "content": error})
                elif audio_path:
                    st.audio(audio_path)
                    st.session_state.chat_history.append({"role": "assistant", "type": "audio", "content": audio_path})
                else:
                    st.error("Не удалось сгенерировать музыку.")

        # VIDEO ROUTING
        elif any(keyword in prompt_lower for keyword in ["видео", "ролик"]):
            with st.spinner("Генерирую видео (это может занять время)..."):
                video_path, error = generate_video(prompt)
                if error:
                    st.error(error)
                    st.session_state.chat_history.append({"role": "assistant", "type": "error", "content": error})
                elif video_path:
                    st.video(video_path)
                    st.session_state.chat_history.append({"role": "assistant", "type": "video", "content": video_path})
                else:
                     st.error("Не удалось сгенерировать видео.")

        # TEXT ROUTING
        else:
            if not st.session_state.get("chat_session"):
                error_msg = "Пожалуйста, введите корректный GOOGLE_API_KEY в настройках."
                st.error(error_msg)
                st.session_state.chat_history.append({"role": "assistant", "type": "error", "content": error_msg})
            else:
                stream = generate_text_stream(st.session_state.chat_session, prompt)
                response_text = st.write_stream(stream)
                st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": response_text})
