import streamlit as st
from PIL import Image
import os

from modules import text, image, music, video

st.set_page_config(page_title="Gemini Ultimate Bot", layout="wide")

def main():
    st.title("Gemini Ultimate Bot")

    with st.sidebar:
        st.header("Настройки")
        api_key = st.text_input("Введите GOOGLE_API_KEY", type="password")

        if st.button("Очистить историю чата"):
            if 'chat_session' in st.session_state:
                del st.session_state.chat_session
            st.rerun()

    if not api_key:
        st.warning("Пожалуйста, введите ваш Google API Key в боковой панели.")
        return

    # Initialize chat session if needed
    if 'chat_session' not in st.session_state:
        st.session_state.chat_session = text.init_chat_session(api_key)

    # Render chat history
    for message in st.session_state.chat_session.get_history():
        with st.chat_message(message["role"]):
            if "text" in message:
                st.markdown(message["text"])
            elif "image" in message:
                st.image(message["image"], caption=message.get("caption", ""))
            elif "audio" in message:
                st.audio(message["audio"])
            elif "video" in message:
                st.video(message["video"])
            elif "error" in message:
                st.error(message["error"])

    # Input prompt
    if prompt := st.chat_input("Введите ваш запрос..."):
        # Routing logic based on keywords
        prompt_lower = prompt.lower().strip()

        # Display user prompt
        with st.chat_message("user"):
            st.markdown(prompt)

        # Add user message to local history tracker (model tracking done in module if text)
        # But only if it's a media generation request (text handles it differently inside module logic if we wish)
        # For simplicity, let's keep it consistent: we add user message to our generic UI history list.
        st.session_state.chat_session.add_to_history({"role": "user", "text": prompt})

        if prompt_lower.startswith(("нарисуй", "фото", "изображение")):
            with st.chat_message("assistant"):
                with st.spinner("Генерация изображения..."):
                    img_url = image.generate_image(prompt)
                    st.image(img_url, caption=prompt)
                    st.session_state.chat_session.add_to_history({
                        "role": "assistant",
                        "image": img_url,
                        "caption": prompt
                    })

        elif prompt_lower.startswith(("музыка", "песня", "трек")):
            with st.chat_message("assistant"):
                with st.spinner("Генерация музыки..."):
                    audio_path = music.generate_music(prompt)
                    if audio_path:
                        st.audio(audio_path)
                        st.session_state.chat_session.add_to_history({
                            "role": "assistant",
                            "audio": audio_path
                        })
                    else:
                        st.error("Не удалось сгенерировать музыку.")

        elif prompt_lower.startswith(("видео", "ролик")):
            with st.chat_message("assistant"):
                with st.spinner("Генерация видео..."):
                    video_result = video.generate_video(prompt)
                    if isinstance(video_result, str) and video_result.endswith(".mp4"): # rudimentary check
                        st.video(video_result)
                        st.session_state.chat_session.add_to_history({
                            "role": "assistant",
                            "video": video_result
                        })
                    elif video_result:
                        # Error case
                        st.error(video_result)
                        st.session_state.chat_session.add_to_history({
                            "role": "assistant",
                            "error": video_result
                        })
                    else:
                        st.error("Не удалось сгенерировать видео.")

        else:
            # Text generation
            with st.chat_message("assistant"):
                try:
                    # We pass the prompt to the generator
                    response_placeholder = st.empty()
                    full_response = ""
                    for chunk in st.session_state.chat_session.send_message_stream(prompt):
                        full_response += chunk
                        response_placeholder.markdown(full_response + "▌")
                    response_placeholder.markdown(full_response)
                    st.session_state.chat_session.add_to_history({"role": "assistant", "text": full_response})
                except Exception as e:
                    st.error(f"Ошибка при генерации текста: {e}")
                    st.session_state.chat_session.add_to_history({"role": "assistant", "error": f"Ошибка: {e}"})

if __name__ == "__main__":
    main()
