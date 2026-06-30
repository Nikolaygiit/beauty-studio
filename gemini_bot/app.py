import streamlit as st
import traceback

from modules.text import get_gemini_client, initialize_chat_session
from modules.image import generate_image
from modules.music import generate_music
from modules.video import generate_video
from modules.routing import get_route

def reset_session():
    st.session_state.chat_history = []
    st.session_state.chat_session = None
    st.session_state.gemini_client = None

def main():
    st.title("Gemini Ultimate Bot 🤖")
    st.write("Генерация текста, изображений, музыки и видео")

    # Sidebar
    with st.sidebar:
        api_key = st.text_input("Введите GOOGLE_API_KEY", type="password", key="api_key_input")
        if st.button("Clear Chat History"):
            reset_session()
            st.rerun()

    # Init session state
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "current_api_key" not in st.session_state:
        st.session_state.current_api_key = ""
    if "gemini_client" not in st.session_state:
        st.session_state.gemini_client = None
    if "chat_session" not in st.session_state:
        st.session_state.chat_session = None

    if api_key != st.session_state.current_api_key:
        st.session_state.current_api_key = api_key
        st.session_state.gemini_client, err = get_gemini_client(api_key)
        if err:
            st.error(err)
            st.session_state.chat_session = None
        else:
            st.session_state.chat_session = initialize_chat_session(st.session_state.gemini_client)
            if not st.session_state.chat_session:
                st.error("Ошибка при инициализации чата.")
                st.session_state.gemini_client = None

    if not st.session_state.gemini_client:
        st.info("Пожалуйста, введите ваш Google API Key в боковой панели, чтобы начать.")
        return

    # Render Chat History
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["text"])

            m_type = message.get("type", "text")
            m_path = message.get("media_path")

            if m_type == "image" and m_path:
                st.image(m_path)
            elif m_type == "music" and m_path:
                st.audio(m_path)
            elif m_type == "video" and m_path:
                st.video(m_path)

    # Chat Input
    if prompt := st.chat_input("Напишите ваш запрос..."):
        # Add user message
        st.session_state.chat_history.append({"role": "user", "text": prompt, "type": "text"})
        with st.chat_message("user"):
            st.markdown(prompt)

        route = get_route(prompt)

        with st.chat_message("assistant"):
            if route == "text":
                message_placeholder = st.empty()
                full_response = ""
                try:
                    response_stream = st.session_state.chat_session.send_message_stream(prompt)
                    for chunk in response_stream:
                        if chunk.text:
                            full_response += chunk.text
                            message_placeholder.markdown(full_response + "▌")
                    message_placeholder.markdown(full_response)
                    st.session_state.chat_history.append({"role": "assistant", "text": full_response, "type": "text"})
                except Exception as e:
                    st.error(f"Произошла ошибка при генерации текста: {e}")
                    traceback.print_exc()

            elif route == "image":
                with st.spinner("Создаю изображение..."):
                    img_url, err = generate_image(prompt)
                    if err:
                        st.error(err)
                    else:
                        st.markdown(f"Вот ваше изображение по запросу: {prompt}")
                        st.image(img_url)
                        st.session_state.chat_history.append({
                            "role": "assistant",
                            "text": f"Вот ваше изображение по запросу: {prompt}",
                            "type": "image",
                            "media_path": img_url
                        })

            elif route == "music":
                with st.spinner("Создаю музыку..."):
                    music_path, err = generate_music(prompt)
                    if err:
                        st.error(err)
                    else:
                        st.markdown(f"Вот ваша музыка по запросу: {prompt}")
                        st.audio(music_path)
                        st.session_state.chat_history.append({
                            "role": "assistant",
                            "text": f"Вот ваша музыка по запросу: {prompt}",
                            "type": "music",
                            "media_path": music_path
                        })

            elif route == "video":
                with st.spinner("Создаю видео..."):
                    video_path, err = generate_video(prompt)
                    if err:
                        st.error(err)
                    else:
                        st.markdown(f"Вот ваше видео по запросу: {prompt}")
                        st.video(video_path)
                        st.session_state.chat_history.append({
                            "role": "assistant",
                            "text": f"Вот ваше видео по запросу: {prompt}",
                            "type": "video",
                            "media_path": video_path
                        })

if __name__ == "__main__":
    main()
