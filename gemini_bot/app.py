import streamlit as st
from modules import text, image, music, video

def initialize_session_state():
    """Initializes Streamlit session state variables."""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "chat_session" not in st.session_state:
        st.session_state.chat_session = None

def clear_chat_history():
    """Clears the visual chat history and resets the Gemini session."""
    st.session_state.messages = []
    if st.session_state.chat_session:
         # Need to recreate to get fresh history
         pass # Actually handled by checking API key later
    st.session_state.chat_session = None

def main():
    st.set_page_config(page_title="Gemini Ultimate Bot", page_icon="🤖", layout="wide")
    initialize_session_state()

    st.title("🤖 Gemini Ultimate Bot")
    st.markdown("Привет! Я лучший бот на базе моделей Gemini. Я умею генерировать текст, изображения, музыку и видео.")

    with st.sidebar:
        st.header("Настройки")
        api_key = st.text_input("Введите GOOGLE_API_KEY", type="password")
        if st.button("Очистить историю чата", key="clear_chat"):
            clear_chat_history()
            st.rerun()

    # Attempt to initialize chat session if key is provided and not already done
    if api_key and not st.session_state.chat_session:
        st.session_state.chat_session = text.init_chat_session(api_key)

    if not api_key:
        st.warning("Пожалуйста, введите ваш GOOGLE_API_KEY в боковой панели, чтобы начать.")
        return

    # Render previous messages
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            if msg["type"] == "text":
                st.markdown(msg["content"])
            elif msg["type"] == "image":
                st.image(msg["content"])
            elif msg["type"] == "audio":
                st.audio(msg["content"])
            elif msg["type"] == "video":
                st.video(msg["content"])

    # Handle user input
    if prompt := st.chat_input("Напишите сообщение..."):
        # Append user text
        st.session_state.messages.append({"role": "user", "type": "text", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            prompt_lower = prompt.lower().strip()

            # Routing based on keywords
            if prompt_lower.startswith(('нарисуй', 'фото', 'изображение')):
                with st.spinner("Создаю изображение..."):
                    img_url = image.generate_image_url(prompt)
                    st.image(img_url)
                    st.session_state.messages.append({"role": "assistant", "type": "image", "content": img_url})

            elif prompt_lower.startswith(('музыка', 'песня', 'трек')):
                with st.spinner("Генерирую музыку (это может занять время)..."):
                    audio_res = music.generate_music(prompt)
                    if isinstance(audio_res, str) and not audio_res.endswith('.wav'):
                        # This means it's an error string or not a file path
                        if 'Error' in audio_res or 'Ошибка' in audio_res:
                            st.error(audio_res)
                            st.session_state.messages.append({"role": "assistant", "type": "text", "content": audio_res})
                        else:
                            st.audio(audio_res)
                            st.session_state.messages.append({"role": "assistant", "type": "audio", "content": audio_res})
                    else:
                        st.audio(audio_res)
                        st.session_state.messages.append({"role": "assistant", "type": "audio", "content": audio_res})

            elif prompt_lower.startswith(('видео', 'ролик')):
                with st.spinner("Генерирую видео (это может занять продолжительное время)..."):
                    video_res = video.generate_video(prompt)
                    if isinstance(video_res, str) and ('Error' in video_res or 'Ошибка' in video_res or 'недоступен' in video_res):
                        st.error(video_res)
                        st.session_state.messages.append({"role": "assistant", "type": "text", "content": video_res})
                    else:
                        st.video(video_res)
                        st.session_state.messages.append({"role": "assistant", "type": "video", "content": video_res})
            else:
                # Regular text chat
                stream = text.generate_text_stream(prompt, st.session_state.chat_session)
                response_text = st.write_stream(stream)
                st.session_state.messages.append({"role": "assistant", "type": "text", "content": response_text})

if __name__ == "__main__":
    main()
