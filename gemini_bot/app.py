import streamlit as st

from modules.routing import get_route
from modules.text import get_gemini_client, create_chat_session, generate_text_stream
from modules.image import generate_image
from modules.music import generate_music
from modules.video import generate_video

# Config setup
st.set_page_config(page_title="Gemini Ultimate Bot", page_icon="🤖", layout="wide")

st.title("🤖 Gemini Ultimate Bot")
st.write("Привет! Я могу общаться с тобой, а также генерировать изображения, музыку и видео по твоему запросу.")

# Sidebar setup
with st.sidebar:
    st.header("Настройки")
    api_key = st.text_input("Введите GOOGLE_API_KEY", type="password")

    st.markdown("---")
    if st.button("Очистить историю чата", use_container_width=True):
        if "chat_history" in st.session_state:
            st.session_state.chat_history = []
        if "chat_session" in st.session_state:
            del st.session_state.chat_session
        if "gemini_client" in st.session_state:
            del st.session_state.gemini_client
        if "current_api_key" in st.session_state:
            st.session_state.current_api_key = None
        st.rerun()

# State initialization
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "current_api_key" not in st.session_state:
    st.session_state.current_api_key = None

# Update API key logic
if api_key and api_key != st.session_state.current_api_key:
    st.session_state.current_api_key = api_key
    st.session_state.gemini_client = get_gemini_client(api_key)
    st.session_state.chat_session = create_chat_session(st.session_state.gemini_client)
    st.success("API ключ успешно применен!")

# Render chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        if message["type"] == "text":
            st.markdown(message["content"])
        elif message["type"] == "image":
            st.image(message["content"])
        elif message["type"] == "music":
            st.audio(message["content"])
        elif message["type"] == "video":
            st.video(message["content"])
        elif message["type"] == "error":
            st.error(message["content"])

# User Input
if prompt := st.chat_input("Напишите сообщение..."):
    # Add user message to history
    st.session_state.chat_history.append({"role": "user", "type": "text", "content": prompt})

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Require API key for all actions currently (even if only text needs it, to simplify)
    if not st.session_state.current_api_key:
        with st.chat_message("assistant"):
            error_msg = "Пожалуйста, введите GOOGLE_API_KEY в боковой панели."
            st.error(error_msg)
            st.session_state.chat_history.append({"role": "assistant", "type": "error", "content": error_msg})
        st.stop()

    route = get_route(prompt)

    with st.chat_message("assistant"):
        if route == "image":
            with st.spinner("Генерирую изображение..."):
                url, error = generate_image(prompt)
                if url:
                    st.image(url)
                    st.session_state.chat_history.append({"role": "assistant", "type": "image", "content": url})
                else:
                    st.error(error)
                    st.session_state.chat_history.append({"role": "assistant", "type": "error", "content": error})

        elif route == "music":
            with st.spinner("Генерирую музыку..."):
                audio_path, error = generate_music(prompt)
                if audio_path:
                    st.audio(audio_path)
                    st.session_state.chat_history.append({"role": "assistant", "type": "music", "content": audio_path})
                else:
                    st.error(error)
                    st.session_state.chat_history.append({"role": "assistant", "type": "error", "content": error})

        elif route == "video":
            with st.spinner("Генерирую видео..."):
                video_path, error = generate_video(prompt)
                if video_path:
                    st.video(video_path)
                    st.session_state.chat_history.append({"role": "assistant", "type": "video", "content": video_path})
                else:
                    st.error(error)
                    st.session_state.chat_history.append({"role": "assistant", "type": "error", "content": error})

        else: # text
            if "chat_session" not in st.session_state:
                st.session_state.chat_session = create_chat_session(st.session_state.gemini_client)

            with st.spinner("Печатаю ответ..."):
                stream = generate_text_stream(st.session_state.chat_session, prompt)

                # We need to collect the full text to save in history
                full_text = ""
                placeholder = st.empty()
                error_occurred = False

                for chunk_text, error in stream:
                    if error:
                        st.error(error)
                        st.session_state.chat_history.append({"role": "assistant", "type": "error", "content": error})
                        error_occurred = True
                        break

                    if chunk_text:
                        full_text += chunk_text
                        placeholder.markdown(full_text + "▌")

                if not error_occurred:
                    placeholder.markdown(full_text)
                    st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": full_text})
