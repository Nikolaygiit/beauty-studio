import streamlit as st
import os

from modules.text import init_gemini_client, init_chat_session
from modules.image import generate_image
from modules.music import generate_music
from modules.video import generate_video

def main():
    st.set_page_config(page_title="Gemini Ultimate Bot", page_icon="🤖")
    st.title("Gemini Ultimate Bot 🤖")

    # Sidebar for API Key and Settings
    with st.sidebar:
        st.header("Настройки (Settings)")
        api_key = st.text_input("Введите GOOGLE_API_KEY", type="password")

        if st.button("Очистить историю чата (Clear Chat History)"):
            if "chat_history" in st.session_state:
                del st.session_state.chat_history
            if "chat_session" in st.session_state:
                del st.session_state.chat_session
            if "current_api_key" in st.session_state:
                st.session_state.current_api_key = None
            st.rerun()

    # Session State Initialization
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    if "current_api_key" not in st.session_state:
        st.session_state.current_api_key = None

    if api_key:
        if st.session_state.current_api_key != api_key:
            try:
                st.session_state.gemini_client = init_gemini_client(api_key)
                st.session_state.chat_session = init_chat_session(st.session_state.gemini_client)
                st.session_state.current_api_key = api_key
            except Exception as e:
                st.error(f"Ошибка при инициализации Gemini API: {str(e)}")
                return
    else:
        st.warning("Пожалуйста, введите ваш GOOGLE_API_KEY в боковой панели, чтобы начать.")
        return

    # Render Chat History
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            if message["type"] == "text":
                st.markdown(message["content"])
            elif message["type"] == "image":
                st.image(message["content"], caption="Сгенерированное изображение")
            elif message["type"] == "audio":
                st.audio(message["content"])
            elif message["type"] == "video":
                st.video(message["content"])
            elif message["type"] == "error":
                st.error(message["content"])

    # Chat Input
    if prompt := st.chat_input("Введите сообщение..."):
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.chat_history.append({"role": "user", "type": "text", "content": prompt})

        prompt_lower = prompt.lower()

        with st.chat_message("assistant"):
            # Route to Media Generators
            if any(keyword in prompt_lower for keyword in ['нарисуй', 'фото', 'изображение']):
                with st.spinner("Создаю изображение..."):
                    media_url, err = generate_image(prompt)
                    if media_url:
                        st.image(media_url, caption="Сгенерированное изображение")
                        st.session_state.chat_history.append({"role": "assistant", "type": "image", "content": media_url})
                    else:
                        st.error(err)
                        st.session_state.chat_history.append({"role": "assistant", "type": "error", "content": err})

            elif any(keyword in prompt_lower for keyword in ['музык', 'песн', 'трек']):
                with st.spinner("Создаю музыку... (это может занять некоторое время)"):
                    media_path, err = generate_music(prompt)
                    if media_path:
                        st.audio(media_path)
                        st.session_state.chat_history.append({"role": "assistant", "type": "audio", "content": media_path})
                    else:
                        st.error(err)
                        st.session_state.chat_history.append({"role": "assistant", "type": "error", "content": err})

            elif any(keyword in prompt_lower for keyword in ['видео', 'ролик']):
                with st.spinner("Создаю видео... (это может занять значительное время)"):
                    media_path, err = generate_video(prompt)
                    if media_path:
                        st.video(media_path)
                        st.session_state.chat_history.append({"role": "assistant", "type": "video", "content": media_path})
                    else:
                        st.error(err)
                        st.session_state.chat_history.append({"role": "assistant", "type": "error", "content": err})

            # Route to Text Generation
            else:
                try:
                    response_placeholder = st.empty()
                    full_response = ""

                    response_stream = st.session_state.chat_session.send_message_stream(prompt)
                    for chunk in response_stream:
                        if chunk.text:
                            full_response += chunk.text
                            response_placeholder.markdown(full_response + "▌")

                    response_placeholder.markdown(full_response)
                    st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": full_response})

                except Exception as e:
                    error_msg = f"Ошибка генерации текста: {str(e)}"
                    st.error(error_msg)
                    st.session_state.chat_history.append({"role": "assistant", "type": "error", "content": error_msg})

if __name__ == "__main__":
    main()
