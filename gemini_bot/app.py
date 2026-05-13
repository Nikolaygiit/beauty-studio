import streamlit as st
from modules.text import initialize_chat, generate_text_stream
from modules.image import generate_image_url
from modules.music import generate_music
from modules.video import generate_video

# --- Constants & Configuration ---
IMAGE_KEYWORDS = ['нарисуй', 'фото', 'изображение']
MUSIC_KEYWORDS = ['музыка', 'песня', 'трек']
VIDEO_KEYWORDS = ['видео', 'ролик']

st.set_page_config(page_title="Gemini Ultimate Bot", page_icon="🤖")
st.title("Gemini Ultimate Bot 🤖")

# --- Sidebar & Setup ---
with st.sidebar:
    st.header("Настройки")
    api_key = st.text_input("Введите ваш Google API Key", type="password")

    if st.button("Очистить историю чата"):
        for key in ['chat_history', 'chat_session', 'gemini_client', 'current_api_key']:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()

# --- Session State Management ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Re-initialize Gemini client if the API key changes or is not set
if "current_api_key" not in st.session_state or st.session_state.current_api_key != api_key:
    st.session_state.current_api_key = api_key
    st.session_state.gemini_client = None
    st.session_state.chat_session = None

if api_key and st.session_state.gemini_client is None:
    client, chat = initialize_chat(api_key)
    if client:
        st.session_state.gemini_client = client
        st.session_state.chat_session = chat
    else:
        st.error(chat) # Show error message

# --- Chat UI ---
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "image_url" in message:
            st.image(message["image_url"])
        if "audio_path" in message:
            st.audio(message["audio_path"])
        if "video_path" in message:
            st.video(message["video_path"])

if prompt := st.chat_input("Введите ваш запрос..."):
    if not api_key:
        st.warning("Пожалуйста, введите Google API Key в боковой панели.")
    elif st.session_state.chat_session is None:
         st.warning("Клиент Gemini не инициализирован. Проверьте API ключ.")
    else:
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.chat_history.append({"role": "user", "content": prompt})

        # Determine media type based on keywords (using 'in' operator for natural phrasing)
        prompt_lower = prompt.lower()
        is_image = any(kw in prompt_lower for kw in IMAGE_KEYWORDS)
        is_music = any(kw in prompt_lower for kw in MUSIC_KEYWORDS)
        is_video = any(kw in prompt_lower for kw in VIDEO_KEYWORDS)

        # Process request
        with st.chat_message("assistant"):
            if is_image:
                st.markdown("Генерирую изображение...")
                url, err = generate_image_url(prompt)
                if err:
                    st.error(err)
                    st.session_state.chat_history.append({"role": "assistant", "content": f"Ошибка: {err}"})
                else:
                    st.image(url)
                    st.session_state.chat_history.append({"role": "assistant", "content": "Вот ваше изображение:", "image_url": url})

            elif is_music:
                with st.spinner("Генерирую музыку..."):
                    audio_path, err = generate_music(prompt)
                    if err:
                        st.error(err)
                        st.session_state.chat_history.append({"role": "assistant", "content": f"Ошибка: {err}"})
                    else:
                        st.audio(audio_path)
                        st.session_state.chat_history.append({"role": "assistant", "content": "Вот ваша музыка:", "audio_path": audio_path})

            elif is_video:
                with st.spinner("Генерирую видео..."):
                    video_path, err = generate_video(prompt)
                    if err:
                        st.error(err)
                        st.session_state.chat_history.append({"role": "assistant", "content": f"Ошибка: {err}"})
                    else:
                        st.video(video_path)
                        st.session_state.chat_history.append({"role": "assistant", "content": "Вот ваше видео:", "video_path": video_path})

            else:
                # Text generation
                response_placeholder = st.empty()
                full_response = ""
                for chunk_text in generate_text_stream(st.session_state.chat_session, prompt):
                    if chunk_text:
                        full_response += chunk_text
                        response_placeholder.markdown(full_response + "▌")
                response_placeholder.markdown(full_response)
                st.session_state.chat_history.append({"role": "assistant", "content": full_response})
