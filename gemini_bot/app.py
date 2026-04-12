import streamlit as st

# Setup page layout
st.set_page_config(page_title="Gemini Ultimate Bot", layout="wide")

from modules import text, image, music, video

def reset_session_state():
    """Resets the chat session and history state."""
    st.session_state.chat_history = []
    st.session_state.chat_session = None
    st.session_state.gemini_client = None

def main():
    st.title("Gemini Ultimate Bot: Мультимедийный помощник")

    # Initialize state
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "chat_session" not in st.session_state:
        st.session_state.chat_session = None
    if "gemini_client" not in st.session_state:
        st.session_state.gemini_client = None
    if "current_api_key" not in st.session_state:
        st.session_state.current_api_key = ""

    # Sidebar configuration
    with st.sidebar:
        st.header("Настройки")
        api_key = st.text_input("Введите ваш Google API Key", type="password")
        if st.button("Очистить историю чата"):
            reset_session_state()
            st.rerun()

    # Re-initialize Gemini client if API key changes or is first set
    if api_key and (api_key != st.session_state.current_api_key or st.session_state.chat_session is None):
        client, session = text.initialize_chat_session(api_key)
        if client and session:
            st.session_state.gemini_client = client
            st.session_state.chat_session = session
            st.session_state.current_api_key = api_key
            st.success("API ключ успешно применен!")
        else:
            st.error("Не удалось инициализировать сессию. Проверьте ваш API ключ.")

    # Display chat history
    for message in st.session_state.chat_history:
        role = message["role"]
        content = message["content"]
        media_type = message.get("media_type")
        media_data = message.get("media_data")

        with st.chat_message(role):
            if role == "user":
                st.markdown(content)
            else:
                if media_type == "text":
                    st.markdown(content)
                elif media_type == "image":
                    st.markdown(content)
                    st.image(media_data)
                elif media_type == "music":
                    st.markdown(content)
                    st.audio(media_data)
                elif media_type == "video":
                    st.markdown(content)
                    st.video(media_data)

    # Chat input
    if prompt := st.chat_input("Введите ваш запрос..."):
        if not st.session_state.chat_session:
            st.error("Пожалуйста, введите валидный Google API Key в боковой панели.")
            return

        # Add user message to history
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Routing based on keywords
        prompt_lower = prompt.lower()

        with st.chat_message("assistant"):
            if any(kw in prompt_lower for kw in ['нарисуй', 'фото', 'изображение']):
                with st.spinner("Генерация изображения..."):
                    img_url = image.generate_image_url(prompt)
                    response_text = "Вот ваше изображение:"
                    st.markdown(response_text)
                    st.image(img_url)
                    st.session_state.chat_history.append({"role": "assistant", "content": response_text, "media_type": "image", "media_data": img_url})

            elif any(kw in prompt_lower for kw in ['музыка', 'песня', 'трек']):
                with st.spinner("Генерация музыки (это может занять несколько минут)..."):
                    err, audio_path = music.generate_music(prompt)
                    if err:
                        st.error(err)
                        st.session_state.chat_history.append({"role": "assistant", "content": err, "media_type": "text"})
                    else:
                        response_text = "Вот ваша музыка:"
                        st.markdown(response_text)
                        st.audio(audio_path)
                        st.session_state.chat_history.append({"role": "assistant", "content": response_text, "media_type": "music", "media_data": audio_path})

            elif any(kw in prompt_lower for kw in ['видео', 'ролик']):
                with st.spinner("Генерация видео (это может занять продолжительное время)..."):
                    err, video_path = video.generate_video(prompt)
                    if err:
                        st.error(err)
                        st.session_state.chat_history.append({"role": "assistant", "content": err, "media_type": "text"})
                    else:
                        response_text = "Вот ваше видео:"
                        st.markdown(response_text)
                        st.video(video_path)
                        st.session_state.chat_history.append({"role": "assistant", "content": response_text, "media_type": "video", "media_data": video_path})

            else:
                with st.spinner("Размышляю..."):
                    response_text = text.generate_text_response(st.session_state.chat_session, prompt)
                    st.markdown(response_text)
                    st.session_state.chat_history.append({"role": "assistant", "content": response_text, "media_type": "text"})

if __name__ == "__main__":
    main()
