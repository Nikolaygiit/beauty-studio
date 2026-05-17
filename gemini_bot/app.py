import streamlit as st
from google import genai
from gradio_client import Client
import time

from modules import text, image, music, video

st.set_page_config(page_title="Gemini Ultimate Bot", page_icon="🤖")

st.title("Gemini Ultimate Bot 🤖")

# --- Стилизация ---
st.markdown("""
<style>
.stChatMessage {
    padding: 1rem;
    border-radius: 0.5rem;
    margin-bottom: 1rem;
}
</style>
""", unsafe_allow_html=True)

# --- Инициализация клиентов ---

@st.cache_resource(show_spinner=False)
def get_music_client():
    try:
        return Client("sanchit-gandhi/musicgen-streaming")
    except Exception as e:
        return f"Ошибка загрузки музыкальной модели: {str(e)}"

@st.cache_resource(show_spinner=False)
def get_video_client():
    try:
        return Client("damo-vilab/modelscope-text-to-video-synthesis")
    except Exception as e:
        return f"Ошибка загрузки видео модели: {str(e)}"

# --- Сайдбар ---
with st.sidebar:
    st.header("Настройки")
    api_key = st.text_input("Введите GOOGLE_API_KEY", type="password")

    if st.button("Очистить историю чата", type="primary"):
        st.session_state.chat_history = []
        if "chat_session" in st.session_state:
            del st.session_state.chat_session
        if "gemini_client" in st.session_state:
            del st.session_state.gemini_client
        st.rerun()

# --- Состояние сессии ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "current_api_key" not in st.session_state:
    st.session_state.current_api_key = ""

# Переинициализация Gemini, если ключ изменился
if api_key and api_key != st.session_state.current_api_key:
    st.session_state.current_api_key = api_key
    try:
        st.session_state.gemini_client = genai.Client(api_key=api_key)
        # Инициализируем сессию только для текста, история хранится в chat_history
        st.session_state.chat_session = text.init_chat_session(st.session_state.gemini_client)
    except Exception as e:
         st.sidebar.error(f"Ошибка API ключа: {e}")
         if "gemini_client" in st.session_state:
             del st.session_state.gemini_client
         if "chat_session" in st.session_state:
             del st.session_state.chat_session

# --- Отображение истории ---
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        if msg["type"] == "text":
            st.markdown(msg["content"])
        elif msg["type"] == "image":
            st.image(msg["content"])
        elif msg["type"] == "audio":
            st.audio(msg["content"])
        elif msg["type"] == "video":
            st.video(msg["content"])
        elif msg["type"] == "error":
            st.error(msg["content"])

# --- Ввод пользователя ---
if prompt := st.chat_input("Введите ваш запрос..."):
    if not api_key:
        st.info("Пожалуйста, введите GOOGLE_API_KEY в боковой панели.")
        st.stop()

    if "chat_session" not in st.session_state:
        st.error("Ошибка инициализации чата. Проверьте API ключ.")
        st.stop()

    st.session_state.chat_history.append({"role": "user", "type": "text", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    prompt_lower = prompt.lower()

    with st.chat_message("assistant"):
        # Роутинг на основе ключевых слов (как указано в памяти)
        if any(word in prompt_lower for word in ['нарисуй', 'фото', 'изображение']):
            with st.spinner("Создаю изображение..."):
                img_url, err = image.generate_image_url(prompt)
                if err:
                    st.error(f"Ошибка генерации: {err}")
                    st.session_state.chat_history.append({"role": "assistant", "type": "error", "content": f"Ошибка генерации: {err}"})
                else:
                    st.image(img_url)
                    st.session_state.chat_history.append({"role": "assistant", "type": "image", "content": img_url})

        elif any(word in prompt_lower for word in ['музыка', 'песня', 'трек']):
            with st.spinner("Создаю музыку... (это может занять некоторое время)"):
                m_client = get_music_client()
                if isinstance(m_client, str):
                    st.error(m_client)
                    st.session_state.chat_history.append({"role": "assistant", "type": "error", "content": m_client})
                else:
                    audio_path, err = music.generate_music(m_client, prompt)
                    if err:
                        st.error(f"Ошибка генерации: {err}")
                        st.session_state.chat_history.append({"role": "assistant", "type": "error", "content": f"Ошибка генерации: {err}"})
                    else:
                        st.audio(audio_path)
                        st.session_state.chat_history.append({"role": "assistant", "type": "audio", "content": audio_path})

        elif any(word in prompt_lower for word in ['видео', 'ролик']):
            with st.spinner("Создаю видео... (это может занять несколько минут)"):
                v_client = get_video_client()
                if isinstance(v_client, str):
                    st.error(v_client)
                    st.session_state.chat_history.append({"role": "assistant", "type": "error", "content": v_client})
                else:
                    video_path, err = video.generate_video(v_client, prompt)
                    if err:
                        st.error(f"Ошибка генерации: {err}")
                        st.session_state.chat_history.append({"role": "assistant", "type": "error", "content": f"Ошибка генерации: {err}"})
                    else:
                        st.video(video_path)
                        st.session_state.chat_history.append({"role": "assistant", "type": "video", "content": video_path})
        else:
            # Генерация текста
            message_placeholder = st.empty()
            full_response = ""
            response_stream, err = text.send_message_stream(st.session_state.chat_session, prompt)

            if err:
                st.error(f"Ошибка от Gemini: {err}")
                st.session_state.chat_history.append({"role": "assistant", "type": "error", "content": f"Ошибка от Gemini: {err}"})
            elif response_stream:
                for chunk in response_stream:
                    if chunk.text:
                        full_response += chunk.text
                        message_placeholder.markdown(full_response + "▌")
                message_placeholder.markdown(full_response)
                st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": full_response})
