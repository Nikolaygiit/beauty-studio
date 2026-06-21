import streamlit as st
from modules.routing import route_prompt
from modules.text import get_gemini_client, init_chat_session, generate_text_stream
from modules.image import generate_image
from modules.music import generate_music
from modules.video import generate_video

# Config
st.set_page_config(page_title="Gemini Ultimate Bot", page_icon="✨")
st.title("✨ Gemini Ultimate Bot")

# Sidebar
with st.sidebar:
    st.header("Настройки")
    api_key = st.text_input("Введите GOOGLE_API_KEY", type="password")

    if st.button("Очистить историю чата"):
        if "chat_history" in st.session_state:
            st.session_state.chat_history = []
        if "chat_session" in st.session_state:
            del st.session_state.chat_session
        if "gemini_client" in st.session_state:
            del st.session_state.gemini_client
        st.rerun()

# State Management
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "current_api_key" not in st.session_state:
    st.session_state.current_api_key = None

# Reinitialize clients if API key changes
if api_key != st.session_state.current_api_key:
    st.session_state.current_api_key = api_key
    if api_key:
        try:
            client = get_gemini_client(api_key)
            st.session_state.gemini_client = client
            st.session_state.chat_session = init_chat_session(client)
        except Exception as e:
            st.sidebar.error(f"Ошибка API ключа: {str(e)}")
            if "gemini_client" in st.session_state:
                del st.session_state.gemini_client
            if "chat_session" in st.session_state:
                del st.session_state.chat_session

# Display History
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

# User Input
prompt = st.chat_input("Напишите что-нибудь...")

if prompt:
    if not api_key:
        st.error("Пожалуйста, введите GOOGLE_API_KEY в боковом меню.")
        st.stop()

    if "chat_session" not in st.session_state:
        st.error("Ошибка инициализации сессии чата. Проверьте API ключ.")
        st.stop()

    st.session_state.chat_history.append({"role": "user", "type": "text", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    route = route_prompt(prompt)

    with st.chat_message("assistant"):
        if route == "image":
            with st.spinner("Генерирую изображение..."):
                img_url, err = generate_image(prompt)
                if err:
                    st.error(err)
                    st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": err})
                elif img_url:
                    st.image(img_url)
                    st.session_state.chat_history.append({"role": "assistant", "type": "image", "content": img_url})

        elif route == "music":
            with st.spinner("Генерирую музыку (это может занять время)..."):
                audio_path, err = generate_music(prompt)
                if err:
                    st.error(err)
                    st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": err})
                elif audio_path:
                    st.audio(audio_path)
                    st.session_state.chat_history.append({"role": "assistant", "type": "music", "content": audio_path})

        elif route == "video":
            with st.spinner("Генерирую видео (это может занять время)..."):
                video_path, err = generate_video(prompt)
                if err:
                    st.error(err)
                    st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": err})
                elif video_path:
                    st.video(video_path)
                    st.session_state.chat_history.append({"role": "assistant", "type": "video", "content": video_path})

        else: # text
            response_placeholder = st.empty()
            full_response = ""
            try:
                for chunk in generate_text_stream(st.session_state.chat_session, prompt):
                    full_response += chunk
                    response_placeholder.markdown(full_response + "▌")
                response_placeholder.markdown(full_response)
                st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": full_response})
            except Exception as e:
                err_msg = f"Ошибка генерации текста: {str(e)}"
                st.error(err_msg)
                st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": err_msg})
