import streamlit as st
from modules.routing import get_media_route
from modules.text import get_gemini_client, get_chat_session
from modules.image import generate_image
from modules.music import generate_music
from modules.video import generate_video

# Streamlit App Configuration
st.set_page_config(page_title="Gemini Ultimate Bot", layout="wide")
st.title("Gemini Ultimate Bot")

# Initialize Session State Variables
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "chat_session" not in st.session_state:
    st.session_state.chat_session = None
if "gemini_client" not in st.session_state:
    st.session_state.gemini_client = None
if "current_api_key" not in st.session_state:
    st.session_state.current_api_key = ""

# Sidebar
with st.sidebar:
    st.header("Настройки")
    api_key = st.text_input("Введите GOOGLE_API_KEY", type="password")

    if st.button("Clear Chat History"):
        st.session_state.chat_history = []
        st.session_state.chat_session = None
        st.session_state.gemini_client = None
        # We keep the current API key to easily reinitialize, or clear it if needed.
        # But generally we just reset the session.
        st.rerun()

# Handle API Key updates
if api_key != st.session_state.current_api_key:
    st.session_state.current_api_key = api_key
    if api_key:
        client, err = get_gemini_client(api_key)
        if err:
            st.sidebar.error(err)
            st.session_state.gemini_client = None
            st.session_state.chat_session = None
        else:
            st.session_state.gemini_client = client
            chat, err2 = get_chat_session(client)
            if err2:
                st.sidebar.error(err2)
                st.session_state.chat_session = None
            else:
                st.session_state.chat_session = chat
                st.sidebar.success("Успешно подключено к Gemini API")
    else:
        st.session_state.gemini_client = None
        st.session_state.chat_session = None

# Display Chat History
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        if message["type"] == "text":
            st.markdown(message["content"])
        elif message["type"] == "image":
            st.markdown(message["content"])
            if message.get("media_path"):
                st.image(message["media_path"])
        elif message["type"] == "music":
            st.markdown(message["content"])
            if message.get("media_path"):
                st.audio(message["media_path"])
        elif message["type"] == "video":
            st.markdown(message["content"])
            if message.get("media_path"):
                st.video(message["media_path"])

# Chat Input
if prompt := st.chat_input("Напишите что-нибудь..."):
    # Render user message immediately
    st.session_state.chat_history.append({"role": "user", "type": "text", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Determine route
    route = get_media_route(prompt)

    # Bot response container
    with st.chat_message("assistant"):
        if route == "text":
            if not st.session_state.chat_session:
                st.error("Пожалуйста, введите GOOGLE_API_KEY в настройках.")
                st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": "Пожалуйста, введите GOOGLE_API_KEY в настройках."})
            else:
                try:
                    response_placeholder = st.empty()
                    full_response = ""
                    # Stream the response
                    response_stream = st.session_state.chat_session.send_message_stream(prompt)
                    for chunk in response_stream:
                        if chunk.text:
                            full_response += chunk.text
                            response_placeholder.markdown(full_response + "▌")
                    response_placeholder.markdown(full_response)
                    st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": full_response})
                except Exception as e:
                    error_msg = f"Произошла ошибка при генерации текста: {e}"
                    st.error(error_msg)
                    st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": error_msg})

        elif route == "image":
            with st.spinner("Генерация изображения..."):
                url, err = generate_image(prompt)
                if err:
                    st.error(err)
                    st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": err})
                else:
                    st.image(url)
                    msg_content = "Вот ваше изображение:"
                    st.session_state.chat_history.append({"role": "assistant", "type": "image", "content": msg_content, "media_path": url})

        elif route == "music":
            with st.spinner("Генерация музыки... Это может занять некоторое время."):
                audio_path, err = generate_music(prompt)
                if err:
                    st.error(err)
                    st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": err})
                else:
                    st.audio(audio_path)
                    msg_content = "Вот ваша музыка:"
                    st.session_state.chat_history.append({"role": "assistant", "type": "music", "content": msg_content, "media_path": audio_path})

        elif route == "video":
            with st.spinner("Генерация видео... Это может занять некоторое время."):
                video_path, err = generate_video(prompt)
                if err:
                    st.error(err)
                    st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": err})
                else:
                    st.video(video_path)
                    msg_content = "Вот ваше видео:"
                    st.session_state.chat_history.append({"role": "assistant", "type": "video", "content": msg_content, "media_path": video_path})
