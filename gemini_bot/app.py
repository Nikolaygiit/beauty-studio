import streamlit as st
from modules.routing import get_route
from modules.text import setup_chat_session
from modules.image import generate_image_url
from modules.music import generate_music
from modules.video import generate_video

st.set_page_config(page_title="Gemini Ultimate Bot", page_icon="✨")
st.title("Gemini Ultimate Bot")

with st.sidebar:
    st.header("Настройки")
    api_key = st.text_input("Введите GOOGLE_API_KEY", type="password")

    if st.button("Clear Chat History"):
        if 'chat_history' in st.session_state:
            del st.session_state['chat_history']
        if 'chat_session' in st.session_state:
            del st.session_state['chat_session']
        if 'gemini_client' in st.session_state:
            del st.session_state['gemini_client']
        st.rerun()

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        if message["type"] == "text":
            st.markdown(message["content"])
        elif message["type"] == "image":
            st.image(message["content"])
            st.markdown(message["content"])
        elif message["type"] == "music":
            st.audio(message["content"])
        elif message["type"] == "video":
            st.video(message["content"])

if prompt := st.chat_input("Введите ваш запрос..."):
    if not api_key:
        st.warning("Пожалуйста, введите GOOGLE_API_KEY в боковой панели.")
        st.stop()

    st.session_state.chat_history.append({"role": "user", "type": "text", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    if 'current_api_key' not in st.session_state or st.session_state.current_api_key != api_key:
        st.session_state.current_api_key = api_key
        try:
            client, chat_session = setup_chat_session(api_key)
            st.session_state.gemini_client = client
            st.session_state.chat_session = chat_session
        except Exception as e:
            st.error(f"Ошибка настройки сессии Gemini: {e}")
            st.stop()

    route = get_route(prompt)

    with st.chat_message("assistant"):
        if route == 'text':
            try:
                response_stream = st.session_state.chat_session.send_message_stream(prompt)
                full_response = ""
                message_placeholder = st.empty()
                for chunk in response_stream:
                    if chunk.text:
                        full_response += chunk.text
                        message_placeholder.markdown(full_response + "▌")
                message_placeholder.markdown(full_response)
                st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": full_response})
            except Exception as e:
                st.error(f"Ошибка генерации текста: {e}")

        elif route == 'image':
            with st.spinner("Генерация изображения..."):
                image_url = generate_image_url(prompt)
                st.image(image_url)
                st.markdown(image_url)
                st.session_state.chat_history.append({"role": "assistant", "type": "image", "content": image_url})

        elif route == 'music':
            with st.spinner("Генерация музыки..."):
                music_path, error = generate_music(prompt)
                if error:
                    st.error(error)
                elif music_path:
                    st.audio(music_path)
                    st.session_state.chat_history.append({"role": "assistant", "type": "music", "content": music_path})

        elif route == 'video':
            with st.spinner("Генерация видео..."):
                video_path, error = generate_video(prompt)
                if error:
                    st.error(error)
                elif video_path:
                    st.video(video_path)
                    st.session_state.chat_history.append({"role": "assistant", "type": "video", "content": video_path})
