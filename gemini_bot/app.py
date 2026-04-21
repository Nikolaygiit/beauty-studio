import streamlit as st
from modules.text import init_chat_session, generate_text_stream
from modules.image import generate_image
from modules.music import generate_music
from modules.video import generate_video

# --- UI Setup ---
st.set_page_config(page_title="Gemini Ultimate Bot", page_icon="✨", layout="centered")
st.title("Gemini Ultimate Bot ✨")
st.write("Привет! Я могу общаться с тобой, а также генерировать изображения, музыку и видео.")

# --- Sidebar Configuration ---
with st.sidebar:
    st.header("Настройки")
    api_key = st.text_input("Введите ваш Google API Key", type="password")

    if st.button("Очистить историю чата"):
        st.session_state.chat_history = []
        st.session_state.chat_session = None
        st.session_state.gemini_client = None
        st.session_state.current_api_key = None
        st.rerun()

# --- Initialize Session State ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "chat_session" not in st.session_state:
    st.session_state.chat_session = None
if "gemini_client" not in st.session_state:
    st.session_state.gemini_client = None
if "current_api_key" not in st.session_state:
    st.session_state.current_api_key = None

# Reinitialize if API key changes
if api_key and api_key != st.session_state.current_api_key:
    client, session = init_chat_session(api_key)
    if session:
        st.session_state.gemini_client = client
        st.session_state.chat_session = session
        st.session_state.current_api_key = api_key
        st.session_state.chat_history = []  # Clear history on new key
    else:
        st.sidebar.error("Ошибка инициализации с предоставленным ключом.")

# --- Render Chat History ---
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        if message["type"] == "text":
            st.markdown(message["content"])
        elif message["type"] == "image":
            st.image(message["content"], caption="Сгенерированное изображение")
        elif message["type"] == "music":
            st.audio(message["content"])
        elif message["type"] == "video":
            st.video(message["content"])

# --- Chat Input ---
if prompt := st.chat_input("Напишите сообщение... (например, 'нарисуй кота' или 'сделай видео моря')"):
    if not st.session_state.chat_session:
        st.warning("Пожалуйста, введите валидный Google API Key в боковой панели.")
        st.stop()

    # Append user prompt
    st.session_state.chat_history.append({"role": "user", "type": "text", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    prompt_lower = prompt.lower()

    # Simple media routing based on Russian keywords
    is_image = any(kw in prompt_lower for kw in ['нарисуй', 'фото', 'изображение'])
    is_music = any(kw in prompt_lower for kw in ['музыка', 'песня', 'трек'])
    is_video = any(kw in prompt_lower for kw in ['видео', 'ролик'])

    with st.chat_message("assistant"):
        if is_image:
            with st.spinner("Генерирую изображение..."):
                url, error = generate_image(prompt)
                if error:
                    st.error(error)
                    st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": error})
                else:
                    st.image(url, caption="Сгенерированное изображение")
                    st.session_state.chat_history.append({"role": "assistant", "type": "image", "content": url})

        elif is_music:
            with st.spinner("Генерирую музыку..."):
                audio_path, error = generate_music(prompt)
                if error:
                    st.error(error)
                    st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": error})
                else:
                    st.audio(audio_path)
                    st.session_state.chat_history.append({"role": "assistant", "type": "music", "content": audio_path})

        elif is_video:
            with st.spinner("Генерирую видео..."):
                video_path, error = generate_video(prompt)
                if error:
                    st.error(error)
                    st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": error})
                else:
                    st.video(video_path)
                    st.session_state.chat_history.append({"role": "assistant", "type": "video", "content": video_path})

        else:
            # Fallback to Text Generation using Gemini
            with st.spinner("Печатает..."):
                message_placeholder = st.empty()
                full_response = ""
                # Streaming response
                for chunk in generate_text_stream(st.session_state.chat_session, prompt):
                    full_response += chunk
                    message_placeholder.markdown(full_response + "▌")
                message_placeholder.markdown(full_response)
                st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": full_response})
