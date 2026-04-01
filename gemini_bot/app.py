import streamlit as st
import traceback

st.set_page_config(page_title="Gemini Ultimate Bot", layout="wide")

st.title("Gemini Ultimate Bot")

st.sidebar.title("Настройки")
api_key = st.sidebar.text_input("Введите ваш Google API Key", type="password")

if st.sidebar.button("Clear Chat History"):
    st.session_state.chat_session = None
    st.session_state.messages = []
    st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "media" in message:
            if message["media"]["type"] == "image":
                st.image(message["media"]["url"])
            elif message["media"]["type"] == "audio":
                st.audio(message["media"]["path"])
            elif message["media"]["type"] == "video":
                st.video(message["media"]["path"])

if prompt := st.chat_input("Введите сообщение..."):
    if not api_key:
        st.warning("Пожалуйста, введите Google API Key в боковой панели.")
        st.stop()

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        prompt_lower = prompt.lower()

        try:
            if any(keyword in prompt_lower for keyword in ['нарисуй', 'фото', 'изображение']):
                from modules.image import generate_image
                message_placeholder.markdown("Генерирую изображение...")
                image_url = generate_image(prompt)
                message_placeholder.markdown("Вот ваше изображение:")
                st.image(image_url)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": "Вот ваше изображение:",
                    "media": {"type": "image", "url": image_url}
                })
            elif any(keyword in prompt_lower for keyword in ['музыка', 'песня', 'трек']):
                from modules.music import generate_music
                message_placeholder.markdown("Генерирую музыку...")
                audio_path = generate_music(prompt)
                if isinstance(audio_path, str) and audio_path.startswith("Ошибка"):
                    message_placeholder.error(audio_path)
                    st.session_state.messages.append({"role": "assistant", "content": audio_path})
                else:
                    message_placeholder.markdown("Вот ваша музыка:")
                    st.audio(audio_path)
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": "Вот ваша музыка:",
                        "media": {"type": "audio", "path": audio_path}
                    })
            elif any(keyword in prompt_lower for keyword in ['видео', 'ролик']):
                from modules.video import generate_video
                message_placeholder.markdown("Генерирую видео...")
                video_path = generate_video(prompt)
                if isinstance(video_path, str) and video_path.startswith("Ошибка"):
                    message_placeholder.error(video_path)
                    st.session_state.messages.append({"role": "assistant", "content": video_path})
                else:
                    message_placeholder.markdown("Вот ваше видео:")
                    st.video(video_path)
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": "Вот ваше видео:",
                        "media": {"type": "video", "path": video_path}
                    })
            else:
                from modules.text import generate_text
                response_stream = generate_text(prompt, api_key)
                full_response = ""
                for chunk in response_stream:
                    full_response += chunk
                    message_placeholder.markdown(full_response + "▌")
                message_placeholder.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})

        except Exception as e:
            st.error(f"Произошла ошибка: {str(e)}")
            st.code(traceback.format_exc())
