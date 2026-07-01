import streamlit as st
from modules.routing import get_route
from modules.text import get_gemini_client, init_chat_session, generate_text_stream
from modules.image import generate_image
from modules.music import get_music_client, generate_music
from modules.video import get_video_client, generate_video

# Streamlit Page Config
st.set_page_config(
    page_title="Gemini Ultimate Bot",
    page_icon="✨",
    layout="wide"
)

st.title("✨ Gemini Ultimate Bot")

# Sidebar Configuration
with st.sidebar:
    st.header("Настройки")
    api_key = st.text_input("Введите GOOGLE_API_KEY", type="password")

    if st.button("Очистить историю чата"):
        if 'chat_history' in st.session_state:
            del st.session_state.chat_history
        if 'chat_session' in st.session_state:
            del st.session_state.chat_session
        if 'gemini_client' in st.session_state:
            del st.session_state.gemini_client
        if 'current_api_key' in st.session_state:
            del st.session_state.current_api_key
        st.rerun()

# State Initialization
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "current_api_key" not in st.session_state or st.session_state.current_api_key != api_key:
    st.session_state.current_api_key = api_key
    if api_key:
        client, err = get_gemini_client(api_key)
        if err:
            st.error(err)
        else:
            st.session_state.gemini_client = client
            chat_session, chat_err = init_chat_session(client)
            if chat_err:
                st.error(chat_err)
            else:
                st.session_state.chat_session = chat_session
    else:
         if 'gemini_client' in st.session_state:
             del st.session_state.gemini_client
         if 'chat_session' in st.session_state:
             del st.session_state.chat_session

# Display Chat History
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

        # Display Multimodal Media
        if message.get("type") == "image" and message.get("media_path"):
            st.image(message["media_path"])
        elif message.get("type") == "music" and message.get("media_path"):
            st.audio(message["media_path"])
        elif message.get("type") == "video" and message.get("media_path"):
            st.video(message["media_path"])

# Chat Input
if prompt := st.chat_input("Напишите сообщение..."):
    # Render user prompt
    st.session_state.chat_history.append({"role": "user", "content": prompt, "type": "text"})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Route request
    route = get_route(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()

        # Determine Response based on Route
        if route == 'text':
            if 'chat_session' in st.session_state:
                full_response = ""
                # Stream the text
                for chunk in generate_text_stream(st.session_state.chat_session, prompt):
                    full_response += chunk
                    message_placeholder.markdown(full_response + "▌")
                message_placeholder.markdown(full_response)
                st.session_state.chat_history.append({"role": "assistant", "content": full_response, "type": "text"})
            else:
                msg = "Пожалуйста, введите корректный API ключ для генерации текста."
                message_placeholder.markdown(msg)
                st.session_state.chat_history.append({"role": "assistant", "content": msg, "type": "text"})

        elif route == 'image':
            with st.spinner("Генерация изображения..."):
                url, err = generate_image(prompt)
                if err:
                    st.error(err)
                    st.session_state.chat_history.append({"role": "assistant", "content": err, "type": "text"})
                else:
                    msg = "Вот ваше изображение:"
                    message_placeholder.markdown(msg)
                    st.image(url)
                    st.session_state.chat_history.append({"role": "assistant", "content": msg, "type": "image", "media_path": url})

        elif route == 'music':
            with st.spinner("Генерация музыки (это может занять некоторое время)..."):
                client, err = get_music_client()
                if err:
                    st.error(err)
                    st.session_state.chat_history.append({"role": "assistant", "content": err, "type": "text"})
                else:
                    media_path, gen_err = generate_music(client, prompt)
                    if gen_err:
                        st.error(gen_err)
                        st.session_state.chat_history.append({"role": "assistant", "content": gen_err, "type": "text"})
                    else:
                        msg = "Вот ваша музыка:"
                        message_placeholder.markdown(msg)
                        st.audio(media_path)
                        st.session_state.chat_history.append({"role": "assistant", "content": msg, "type": "music", "media_path": media_path})

        elif route == 'video':
            with st.spinner("Генерация видео (это может занять некоторое время)..."):
                client, err = get_video_client()
                if err:
                    st.error(err)
                    st.session_state.chat_history.append({"role": "assistant", "content": err, "type": "text"})
                else:
                    media_path, gen_err = generate_video(client, prompt)
                    if gen_err:
                        st.error(gen_err)
                        st.session_state.chat_history.append({"role": "assistant", "content": gen_err, "type": "text"})
                    else:
                        msg = "Вот ваше видео:"
                        message_placeholder.markdown(msg)
                        st.video(media_path)
                        st.session_state.chat_history.append({"role": "assistant", "content": msg, "type": "video", "media_path": media_path})
