import streamlit as st
import google.generativeai as genai
from modules import text, image, music, video

st.set_page_config(page_title="Gemini Ultimate Bot", page_icon="🤖", layout="wide")

st.title("Gemini Ultimate Bot 🤖")
st.markdown("Добро пожаловать в универсальный бот на базе Gemini! Вы можете генерировать текст, изображения, музыку и видео.")

# Sidebar setup
st.sidebar.title("Настройки")
api_key = st.sidebar.text_input("Введите ваш Google API Key", type="password")

if api_key:
    genai.configure(api_key=api_key)
else:
    st.sidebar.warning("Пожалуйста, введите ваш Google API Key для продолжения работы с текстом.")

if st.sidebar.button("Очистить историю чата"):
    st.session_state.chat_history = []
    st.sidebar.success("История чата очищена!")

# Session state initialization for chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Caching heavy resources
@st.cache_resource
def get_music_generator():
    return music.init_generator()

@st.cache_resource
def get_video_generator():
    return video.init_generator()

# Option menu
tab_text, tab_image, tab_music, tab_video = st.tabs(["Текст", "Изображения", "Музыка", "Видео"])

with tab_text:
    st.header("Текстовый чат")
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    prompt = st.chat_input("Напишите сообщение...")
    if prompt:
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.chat_history.append({"role": "user", "content": prompt})

        if not api_key:
            st.error("Укажите API ключ в настройках для работы с Gemini.")
        else:
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                response = text.generate_text_stream(prompt, st.session_state.chat_history[:-1])

                full_response = ""
                for chunk in response:
                    full_response += chunk
                    message_placeholder.markdown(full_response + "▌")
                message_placeholder.markdown(full_response)

            st.session_state.chat_history.append({"role": "assistant", "content": full_response})

with tab_image:
    st.header("Генерация изображений")
    img_prompt = st.text_input("Опишите изображение (на английском для лучших результатов):")
    if st.button("Сгенерировать изображение"):
        if img_prompt:
            with st.spinner("Создаем изображение..."):
                img_url = image.generate_image(img_prompt)
                st.image(img_url, caption=img_prompt)
        else:
            st.warning("Пожалуйста, введите описание.")

with tab_music:
    st.header("Генерация музыки")
    music_prompt = st.text_area("Опишите желаемую музыку (на английском):", height=100)
    duration = st.slider("Длительность (секунды)", min_value=1, max_value=30, value=10)
    if st.button("Сгенерировать музыку"):
        if music_prompt:
            with st.spinner("Создаем музыку (это может занять время)..."):
                music_client = get_music_generator()
                audio_path = music.generate_music(music_client, music_prompt, duration)
                if audio_path:
                    st.audio(audio_path)
                else:
                    st.error("Произошла ошибка при генерации музыки.")
        else:
            st.warning("Пожалуйста, введите описание.")

with tab_video:
    st.header("Генерация видео")
    video_prompt = st.text_input("Опишите видео (на английском):")
    if st.button("Сгенерировать видео"):
        if video_prompt:
            with st.spinner("Создаем видео (это может занять значительное время)..."):
                video_client = get_video_generator()
                if isinstance(video_client, str): # Error returned during init
                    st.error(video_client)
                else:
                    video_path = video.generate_video(video_client, video_prompt)
                    if video_path and isinstance(video_path, str) and not video_path.startswith("Ошибка"):
                        st.video(video_path)
                    else:
                        st.error(video_path if isinstance(video_path, str) else "Произошла ошибка при генерации видео.")
        else:
            st.warning("Пожалуйста, введите описание.")
