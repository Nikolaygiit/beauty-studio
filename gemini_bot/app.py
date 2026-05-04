import streamlit as st
from modules.text import init_gemini, generate_text_stream
from modules.image import generate_image
from modules.music import generate_music
from modules.video import generate_video

# --- App Configuration ---
st.set_page_config(page_title="Gemini Ultimate Bot", page_icon="✨", layout="wide")
st.title("✨ Gemini Ultimate Bot")
st.markdown("Генерация текста, изображений, музыки и видео!")

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

# --- State Initialization ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "current_api_key" not in st.session_state or st.session_state.current_api_key != api_key:
    st.session_state.current_api_key = api_key
    st.session_state.gemini_client = None
    st.session_state.chat_session = None

if api_key and st.session_state.chat_session is None:
    client, session = init_gemini(api_key)
    if client and session:
        st.session_state.gemini_client = client
        st.session_state.chat_session = session
    else:
        st.sidebar.error("Ошибка инициализации Gemini API. Проверьте ключ.")

# --- Display Chat History ---
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        if message["type"] == "text":
            st.markdown(message["content"])
        elif message["type"] == "image":
            st.image(message["content"])
        elif message["type"] == "music":
            st.audio(message["content"])
        elif message["type"] == "video":
            st.video(message["content"])

# --- Chat Input & Routing Logic ---
if prompt := st.chat_input("Введите ваш запрос... (текст, фото, видео, музыка)"):
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.chat_history.append({"role": "user", "type": "text", "content": prompt})

    # Routing logic based on Russian keywords
    prompt_lower = prompt.lower()

    if any(keyword in prompt_lower for keyword in ["нарисуй", "фото", "изображение"]):
        with st.chat_message("assistant"):
            with st.spinner("Генерирую изображение..."):
                image_url, error = generate_image(prompt)
                if image_url:
                    st.image(image_url)
                    st.session_state.chat_history.append({"role": "assistant", "type": "image", "content": image_url})
                else:
                    st.error(error)
                    st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": error})

    elif any(keyword in prompt_lower for keyword in ["музыка", "песня", "трек"]):
         with st.chat_message("assistant"):
            with st.spinner("Генерирую музыку (может занять некоторое время)..."):
                music_path, error = generate_music(prompt)
                if music_path:
                    st.audio(music_path)
                    st.session_state.chat_history.append({"role": "assistant", "type": "music", "content": music_path})
                else:
                    st.error(error)
                    st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": error})

    elif any(keyword in prompt_lower for keyword in ["видео", "ролик"]):
         with st.chat_message("assistant"):
            with st.spinner("Генерирую видео (может занять некоторое время)..."):
                video_path, error = generate_video(prompt)
                if video_path:
                    st.video(video_path)
                    st.session_state.chat_history.append({"role": "assistant", "type": "video", "content": video_path})
                else:
                    st.error(error)
                    st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": error})

    else:
        # Default to text generation
        if not api_key:
            st.error("Пожалуйста, введите Google API Key в боковой панели.")
        elif st.session_state.chat_session:
            with st.chat_message("assistant"):
                full_response = st.write_stream(generate_text_stream(st.session_state.chat_session, prompt))
                st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": full_response})
        else:
             st.error("Чат-сессия не инициализирована. Проверьте API Key.")
