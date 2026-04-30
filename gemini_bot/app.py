import streamlit as st
from modules.text import get_gemini_client, start_chat_session
from modules.image import generate_image_url
from modules.music import generate_music
from modules.video import generate_video

# --- Layout & Configuration ---
st.set_page_config(
    page_title="Gemini Ultimate Bot",
    page_icon="🤖",
    layout="wide",
)

st.title("🤖 Gemini Ultimate Bot")
st.markdown("Лучший бот на базе Gemini: генерация текста, изображений, музыки и видео!")

# --- Sidebar Configuration ---
with st.sidebar:
    st.header("Настройки")
    api_key = st.text_input("Введите GOOGLE_API_KEY", type="password")

    st.markdown("---")
    st.markdown("### Возможности:")
    st.markdown("- **Текст**: Обычное общение с Gemini-2.0-flash.")
    st.markdown("- **Изображения**: Напишите 'нарисуй', 'фото' или 'изображение' в промпте.")
    st.markdown("- **Музыка**: Напишите 'музыка', 'песня' или 'трек' в промпте.")
    st.markdown("- **Видео**: Напишите 'видео' или 'ролик' в промпте.")
    st.markdown("---")

    if st.button("Очистить историю чата"):
        st.session_state.chat_history = []
        if api_key:
            client = get_gemini_client(api_key)
            st.session_state.gemini_client = client
            st.session_state.chat_session = start_chat_session(client)
        else:
            st.session_state.chat_session = None
            st.session_state.gemini_client = None
        st.rerun()

# --- Session State Management ---
if "current_api_key" not in st.session_state or st.session_state.current_api_key != api_key:
    st.session_state.current_api_key = api_key
    st.session_state.chat_history = []
    if api_key:
        client = get_gemini_client(api_key)
        st.session_state.gemini_client = client
        st.session_state.chat_session = start_chat_session(client)
    else:
        st.session_state.chat_session = None
        st.session_state.gemini_client = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- Display Chat History ---
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        if msg["type"] == "text":
            st.markdown(msg["content"])
        elif msg["type"] == "image":
            st.image(msg["content"], caption="Сгенерированное изображение")
        elif msg["type"] == "music":
            st.audio(msg["content"])
        elif msg["type"] == "video":
            st.video(msg["content"])

# --- User Input & Routing ---
prompt = st.chat_input("Введите ваш запрос...")

if prompt:
    if not api_key:
        st.warning("Пожалуйста, введите ваш GOOGLE_API_KEY в боковом меню.")
        st.stop()

    # 1. Display User Message
    st.chat_message("user").markdown(prompt)
    st.session_state.chat_history.append({"role": "user", "type": "text", "content": prompt})

    # 2. Determine Request Type based on Russian keywords
    prompt_lower = prompt.lower()

    if any(kw in prompt_lower for kw in ["нарисуй", "фото", "изображение"]):
        # IMAGE GENERATION
        with st.chat_message("assistant"):
            with st.spinner("Создаю изображение..."):
                img_url = generate_image_url(prompt)
                st.image(img_url, caption="Сгенерированное изображение")
                st.session_state.chat_history.append({"role": "assistant", "type": "image", "content": img_url})

    elif any(kw in prompt_lower for kw in ["музыка", "песня", "трек"]):
        # MUSIC GENERATION
        with st.chat_message("assistant"):
            with st.spinner("Создаю музыку (это может занять время)..."):
                audio_path, error_msg = generate_music(prompt)
                if error_msg:
                    st.error(error_msg)
                    st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": error_msg})
                elif audio_path:
                    st.audio(audio_path)
                    st.session_state.chat_history.append({"role": "assistant", "type": "music", "content": audio_path})
                else:
                    msg = "Не удалось получить аудио."
                    st.error(msg)
                    st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": msg})

    elif any(kw in prompt_lower for kw in ["видео", "ролик"]):
        # VIDEO GENERATION
        with st.chat_message("assistant"):
            with st.spinner("Создаю видео (пожалуйста, подождите, может занять несколько минут)..."):
                video_path, error_msg = generate_video(prompt)
                if error_msg:
                    st.error(error_msg)
                    st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": error_msg})
                elif video_path:
                    st.video(video_path)
                    st.session_state.chat_history.append({"role": "assistant", "type": "video", "content": video_path})
                else:
                    msg = "Не удалось получить видео."
                    st.error(msg)
                    st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": msg})

    else:
        # TEXT GENERATION
        with st.chat_message("assistant"):
            with st.spinner("Генерирую ответ..."):
                try:
                    response = st.session_state.chat_session.send_message(prompt)
                    st.markdown(response.text)
                    st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": response.text})
                except Exception as e:
                    error_msg = f"Ошибка при обращении к Gemini API: {str(e)}"
                    st.error(error_msg)
                    st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": error_msg})
