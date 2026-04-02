import streamlit as st
from modules import text, image, music, video

st.set_page_config(page_title="Gemini Ultimate Bot", layout="wide")

st.sidebar.title("Настройки")
api_key = st.sidebar.text_input("Введите GOOGLE_API_KEY", type="password")

if st.sidebar.button("Clear Chat History"):
    if "chat_session" in st.session_state:
        del st.session_state["chat_session"]
    if "messages" in st.session_state:
        del st.session_state["messages"]
    st.rerun()

st.title("Gemini Ultimate Bot")
st.write("Генерация текста, изображений, музыки и видео")

if not api_key:
    st.warning("Пожалуйста, введите GOOGLE_API_KEY в боковой панели.")
    st.stop()

if "chat_session" not in st.session_state:
    try:
        st.session_state.chat_session = text.init_chat_session(api_key)
    except Exception as e:
        st.error(f"Ошибка инициализации сессии: {e}")
        st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "image_url" in message:
            st.image(message["image_url"])
        if "audio_file" in message:
            st.audio(message["audio_file"])
        if "video_file" in message:
            st.video(message["video_file"])

if prompt := st.chat_input("Введите ваш запрос..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    prompt_lower = prompt.lower()
    message_data = {"role": "assistant", "content": ""}

    with st.chat_message("assistant"):
        if any(keyword in prompt_lower for keyword in ["нарисуй", "фото", "изображение"]):
            st.markdown(f"Генерирую изображение по запросу: {prompt}")
            image_url = image.get_image_url(prompt)
            st.image(image_url)
            message_data["content"] = f"Сгенерировано изображение по запросу: {prompt}"
            message_data["image_url"] = image_url

        elif any(keyword in prompt_lower for keyword in ["музыка", "песня", "трек"]):
            st.markdown(f"Генерирую музыку по запросу: {prompt}")
            audio_result = music.generate_music(prompt)
            if isinstance(audio_result, str) and audio_result.startswith("Ошибка"):
                st.error(audio_result)
                message_data["content"] = audio_result
            else:
                st.audio(audio_result)
                message_data["content"] = f"Сгенерирована музыка по запросу: {prompt}"
                message_data["audio_file"] = audio_result

        elif any(keyword in prompt_lower for keyword in ["видео", "ролик"]):
            st.markdown(f"Генерирую видео по запросу: {prompt}")
            video_result = video.generate_video(prompt)
            if isinstance(video_result, str) and video_result.startswith("Ошибка"):
                st.error(video_result)
                message_data["content"] = video_result
            else:
                st.video(video_result)
                message_data["content"] = f"Сгенерировано видео по запросу: {prompt}"
                message_data["video_file"] = video_result

        else:
            response = text.get_gemini_response(st.session_state.chat_session, prompt)
            st.markdown(response)
            message_data["content"] = response

    st.session_state.messages.append(message_data)
