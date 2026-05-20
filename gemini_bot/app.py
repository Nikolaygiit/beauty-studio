import streamlit as st
from modules.text import get_gemini_client
from modules.image import generate_image
from modules.music import generate_music
from modules.video import generate_video

# --- App Config ---
st.set_page_config(page_title="Gemini Ultimate Bot", page_icon="🤖", layout="centered")
st.title("🤖 Gemini Ultimate Bot")
st.markdown("Универсальный помощник: текст, код, генерация фото, музыки и видео!")

# --- Sidebar & Initialization ---
with st.sidebar:
    st.header("Настройки")
    api_key = st.text_input("Введите ваш Google API Key", type="password")

    if st.button("Очистить историю чата", use_container_width=True):
        st.session_state.chat_history = []
        # Re-initialize session to clear context if API key is present
        if st.session_state.get('current_api_key'):
            client, chat = get_gemini_client(st.session_state.current_api_key)
            st.session_state.gemini_client = client
            st.session_state.chat_session = chat
        st.rerun()

    st.markdown("---")
    st.markdown("""
    **Подсказки для медиа:**
    - 🎨 **Фото:** "нарисуй", "фото", "изображение"
    - 🎵 **Музыка:** "музык", "песн", "трек"
    - 🎬 **Видео:** "видео", "ролик"
    """)

# --- Session State Management ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "chat_session" not in st.session_state:
    st.session_state.chat_session = None
if "gemini_client" not in st.session_state:
    st.session_state.gemini_client = None
if "current_api_key" not in st.session_state:
    st.session_state.current_api_key = None

# Handle API Key updates
if api_key and api_key != st.session_state.current_api_key:
    client, chat = get_gemini_client(api_key)
    if client and chat:
        st.session_state.gemini_client = client
        st.session_state.chat_session = chat
        st.session_state.current_api_key = api_key
        st.sidebar.success("API Key успешно подключен!")
    else:
        st.sidebar.error("Ошибка при инициализации API Key.")

# --- Render Chat History ---
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        # Check if media exists and display it
        if "media" in message:
            media_type = message["media"]["type"]
            media_src = message["media"]["src"]
            if media_type == "image":
                st.image(media_src)
            elif media_type == "audio":
                st.audio(media_src)
            elif media_type == "video":
                st.video(media_src)

# --- Chat Input ---
if prompt := st.chat_input("Введите сообщение (или запрос на генерацию)..."):
    if not st.session_state.gemini_client:
        st.warning("Пожалуйста, введите Google API Key в боковой панели.")
        st.stop()

    # Add user message to history
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    prompt_lower = prompt.lower()

    # --- Routing ---
    with st.chat_message("assistant"):
        media_data = None

        # 1. Image Routing
        if any(keyword in prompt_lower for keyword in ["нарисуй", "фото", "изображение"]):
            with st.spinner("Генерация изображения... 🎨"):
                url, error = generate_image(prompt)
                if not error:
                    st.image(url)
                    media_data = {"type": "image", "src": url}
                    response_text = f"Вот ваше изображение по запросу: *{prompt}*"
                    st.markdown(response_text)
                else:
                    response_text = error
                    st.error(error)

        # 2. Music Routing
        elif any(keyword in prompt_lower for keyword in ["музык", "песн", "трек"]):
            with st.spinner("Генерация музыки... 🎵 (Это может занять некоторое время)"):
                audio_path, error = generate_music(prompt)
                if not error:
                    st.audio(audio_path)
                    media_data = {"type": "audio", "src": audio_path}
                    response_text = f"Музыка сгенерирована по запросу: *{prompt}*"
                    st.markdown(response_text)
                else:
                    response_text = error
                    st.error(error)

        # 3. Video Routing
        elif any(keyword in prompt_lower for keyword in ["видео", "ролик"]):
            with st.spinner("Генерация видео... 🎬 (Это может занять несколько минут)"):
                video_path, error = generate_video(prompt)
                if not error:
                    st.video(video_path)
                    media_data = {"type": "video", "src": video_path}
                    response_text = f"Видео сгенерировано по запросу: *{prompt}*"
                    st.markdown(response_text)
                else:
                    response_text = error
                    st.error(error)

        # 4. Text Routing (Default)
        else:
            try:
                # Use Gemini chat session
                response_stream = st.session_state.chat_session.send_message_stream(prompt)

                # Create empty placeholder for streaming text
                message_placeholder = st.empty()
                full_response = ""

                for chunk in response_stream:
                    if chunk.text:
                        full_response += chunk.text
                        message_placeholder.markdown(full_response + "▌")

                # Final update without cursor
                message_placeholder.markdown(full_response)
                response_text = full_response

            except Exception as e:
                response_text = f"Произошла ошибка при общении с Gemini: {str(e)}"
                st.error(response_text)

        # Save assistant response to history
        assistant_message = {"role": "assistant", "content": response_text}
        if media_data:
            assistant_message["media"] = media_data

        st.session_state.chat_history.append(assistant_message)
