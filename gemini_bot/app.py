import streamlit as st
from modules.text import generate_text_stream
from modules.image import generate_image
from modules.music import MusicGenerator
from modules.video import VideoGenerator

st.set_page_config(page_title="Gemini Ultimate Bot", page_icon="✨", layout="wide")

# Initialize generators efficiently via cache
@st.cache_resource
def get_music_generator():
    return MusicGenerator()

@st.cache_resource
def get_video_generator():
    return VideoGenerator()

# UI Layout: Sidebar
st.sidebar.title("Настройки")
api_key = st.sidebar.text_input("Введите GOOGLE_API_KEY", type="password")

if st.sidebar.button("Очистить историю чата"):
    st.session_state.chat_history = []
    st.sidebar.success("История чата очищена!")

# Initialize chat history in session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Main Layout
st.title("✨ Gemini Ultimate Bot ✨")
st.markdown("Добро пожаловать! Здесь вы можете генерировать **текст, изображения, музыку и видео** в одном приложении.")

tab_text, tab_image, tab_music, tab_video = st.tabs(["Текст", "Изображение", "Музыка", "Видео"])

# TAB: TEXT
with tab_text:
    st.header("💬 Текстовый чат с Gemini")

    # Display chat history
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat Input
    if prompt := st.chat_input("Напишите сообщение...", key="text_chat"):
        if not api_key:
            st.error("Пожалуйста, введите GOOGLE_API_KEY в боковой панели слева.")
        else:
            # Display user message
            with st.chat_message("user"):
                st.markdown(prompt)

            # Add to history (internal format needs to be formatted for generativeai)
            # but we can pass the history list to text.py. Actually, genai format differs,
            # so we'll store role/parts locally.
            genai_history = []
            for msg in st.session_state.chat_history:
                role = "user" if msg["role"] == "user" else "model"
                genai_history.append({"role": role, "parts": [msg["content"]]})

            st.session_state.chat_history.append({"role": "user", "content": prompt})

            # Display assistant response
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                full_response = ""

                # Stream the response
                with st.spinner("Бот печатает..."):
                    stream = generate_text_stream(prompt, api_key, genai_history)
                    for chunk in stream:
                        full_response += chunk
                        message_placeholder.markdown(full_response + "▌")

                message_placeholder.markdown(full_response)

            st.session_state.chat_history.append({"role": "assistant", "content": full_response})

# TAB: IMAGE
with tab_image:
    st.header("🖼️ Генерация Изображений")
    st.markdown("Создавайте изображения по текстовому описанию (Pollinations.ai).")

    image_prompt = st.text_input("Опишите изображение (желательно на английском):", key="image_prompt")
    if st.button("Сгенерировать Изображение"):
        if image_prompt:
            with st.spinner("Создаю шедевр..."):
                result = generate_image(image_prompt)
                if isinstance(result, str):
                    st.error(result)
                else:
                    st.image(result, caption=image_prompt)
        else:
            st.warning("Пожалуйста, введите запрос.")

# TAB: MUSIC
with tab_music:
    st.header("🎵 Генерация Музыки")
    st.markdown("Создайте музыку по описанию (MusicGen).")

    music_prompt = st.text_input("Опишите музыку (желательно на английском):", key="music_prompt")
    audio_length = st.slider("Длина аудио (сек)", 5.0, 30.0, 15.0, step=1.0)

    if st.button("Сгенерировать Музыку"):
        if music_prompt:
            with st.spinner("Пишу музыку... (это может занять некоторое время)"):
                music_gen = get_music_generator()
                audio_path, error = music_gen.generate(music_prompt, audio_length_in_s=audio_length)

                if error:
                    st.error(error)
                elif audio_path:
                    st.success("Музыка готова!")
                    st.audio(audio_path)
                else:
                    st.error("Неизвестная ошибка.")
        else:
            st.warning("Пожалуйста, введите запрос.")

# TAB: VIDEO
with tab_video:
    st.header("🎬 Генерация Видео")
    st.markdown("Создайте видео по описанию (ModelScope).")

    video_prompt = st.text_input("Опишите видео (желательно на английском):", key="video_prompt")

    if st.button("Сгенерировать Видео"):
        if video_prompt:
            with st.spinner("Снимаю видео... (может занять несколько минут)"):
                video_gen = get_video_generator()
                video_path, error = video_gen.generate(video_prompt)

                if error:
                    st.error(error)
                elif video_path:
                    # Modelscope predict result sometimes returns a dictionary, check if it's dict
                    if isinstance(video_path, dict) and 'video' in video_path:
                         video_file = video_path['video']
                    else:
                         video_file = video_path
                    st.success("Видео готово!")
                    st.video(video_file)
                else:
                    st.error("Неизвестная ошибка.")
        else:
            st.warning("Пожалуйста, введите запрос.")
