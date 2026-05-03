import streamlit as st
from modules import text, image, music, video

st.set_page_config(page_title="Gemini Ultimate Bot", page_icon="🤖")

st.title("🤖 Gemini Ultimate Bot")
st.write("Привет! Я могу генерировать текст, изображения, музыку и видео. Введите ваш запрос ниже.")

# Initialize session state
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
    api_key = st.text_input("GOOGLE_API_KEY", type="password", value=st.session_state.current_api_key)

    if api_key != st.session_state.current_api_key:
        st.session_state.current_api_key = api_key
        st.session_state.gemini_client = text.get_gemini_client(api_key)
        if st.session_state.gemini_client:
            st.session_state.chat_session = text.initialize_chat_session(st.session_state.gemini_client)
            st.success("API ключ обновлен!")
        else:
            st.session_state.chat_session = None

    if st.button("Clear Chat History"):
        st.session_state.chat_history = []
        if st.session_state.gemini_client:
            st.session_state.chat_session = text.initialize_chat_session(st.session_state.gemini_client)
        st.rerun()

# Display chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        if message["type"] == "text":
            st.markdown(message["content"])
        elif message["type"] == "image":
            st.image(message["content"])
        elif message["type"] == "audio":
            st.audio(message["content"])
        elif message["type"] == "video":
            st.video(message["content"])
        elif message["type"] == "error":
            st.error(message["content"])

# User input
prompt = st.chat_input("Напишите сообщение...")

if prompt:
    # Add user message to history and display
    st.session_state.chat_history.append({"role": "user", "type": "text", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    prompt_lower = prompt.lower()

    with st.chat_message("assistant"):
        # Image routing
        if any(keyword in prompt_lower for keyword in ['нарисуй', 'фото', 'изображение']):
            with st.spinner("Генерирую изображение..."):
                image_url = image.generate_image(prompt)
                st.image(image_url)
                st.session_state.chat_history.append({"role": "assistant", "type": "image", "content": image_url})

        # Music routing
        elif any(keyword in prompt_lower for keyword in ['музыка', 'песня', 'трек']):
            with st.spinner("Генерирую музыку... (Это может занять некоторое время)"):
                audio_path, error = music.generate_music(prompt)
                if audio_path:
                    st.audio(audio_path)
                    st.session_state.chat_history.append({"role": "assistant", "type": "audio", "content": audio_path})
                else:
                    st.error(error)
                    st.session_state.chat_history.append({"role": "assistant", "type": "error", "content": error})

        # Video routing
        elif any(keyword in prompt_lower for keyword in ['видео', 'ролик']):
            with st.spinner("Генерирую видео... (Это может занять некоторое время)"):
                video_path, error = video.generate_video(prompt)
                if video_path:
                    st.video(video_path)
                    st.session_state.chat_history.append({"role": "assistant", "type": "video", "content": video_path})
                else:
                    st.error(error)
                    st.session_state.chat_history.append({"role": "assistant", "type": "error", "content": error})

        # Text routing
        else:
            if not st.session_state.chat_session:
                msg = "Пожалуйста, введите валидный GOOGLE_API_KEY в боковой панели для генерации текста."
                st.error(msg)
                st.session_state.chat_history.append({"role": "assistant", "type": "error", "content": msg})
            else:
                with st.spinner("Думаю..."):
                    stream = text.generate_text_stream(st.session_state.chat_session, prompt)
                    response_container = st.empty()
                    full_response = ""
                    for chunk in stream:
                        full_response += chunk
                        response_container.markdown(full_response + "▌")
                    response_container.markdown(full_response)
                    st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": full_response})
