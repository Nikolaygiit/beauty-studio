import streamlit as st
import os

from modules.text import init_gemini_client, generate_text_stream
from modules.image import generate_image_url
from modules.music import init_music_client, generate_music
from modules.video import init_video_client, generate_video

# Настройка страницы
st.set_page_config(page_title="Gemini Ultimate Bot", page_icon="🤖", layout="wide")
st.title("🤖 Gemini Ultimate Bot")
st.markdown("Универсальный бот: генерация текста, изображений, музыки и видео.")

# --- Кэширование тяжелых клиентов (Music, Video) ---
@st.cache_resource
def get_music_client():
    return init_music_client()

@st.cache_resource
def get_video_client():
    return init_video_client()

# --- Состояние сессии (Session State) ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "chat_session" not in st.session_state:
    st.session_state.chat_session = None
if "gemini_client" not in st.session_state:
    st.session_state.gemini_client = None
if "current_api_key" not in st.session_state:
    st.session_state.current_api_key = ""

# --- Боковая панель (Sidebar) ---
st.sidebar.header("Настройки")
api_key_input = st.sidebar.text_input("Введите GOOGLE_API_KEY", type="password", value=st.session_state.current_api_key)

if st.sidebar.button("Очистить историю чата"):
    st.session_state.chat_history = []
    st.session_state.chat_session = None
    st.session_state.gemini_client = None
    st.session_state.current_api_key = ""
    st.rerun()

# --- Инициализация Gemini Client ---
if api_key_input and api_key_input != st.session_state.current_api_key:
    st.session_state.current_api_key = api_key_input
    try:
        client, chat = init_gemini_client(api_key_input)
        st.session_state.gemini_client = client
        st.session_state.chat_session = chat
        st.sidebar.success("✅ API ключ успешно подключен!")
    except Exception as e:
        st.sidebar.error(f"Ошибка подключения: {e}")

# Проверка наличия API ключа
if not st.session_state.gemini_client:
    st.warning("Пожалуйста, введите GOOGLE_API_KEY в боковой панели, чтобы начать.")
    st.stop()

# --- Отображение истории чата ---
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

# --- Обработка ввода (Routing) ---
prompt = st.chat_input("Введите ваш запрос...")
if prompt:
    prompt_lower = prompt.lower()

    # Показываем сообщение пользователя
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.chat_history.append({"role": "user", "type": "text", "content": prompt})

    with st.chat_message("assistant"):
        # Роутинг (Изображения)
        if any(word in prompt_lower for word in ['нарисуй', 'фото', 'изображение']):
            st.info("🎨 Генерирую изображение...")
            image_url = generate_image_url(prompt)
            st.image(image_url)
            st.session_state.chat_history.append({"role": "assistant", "type": "image", "content": image_url})

        # Роутинг (Музыка)
        elif any(word in prompt_lower for word in ['музыка', 'песня', 'трек']):
            st.info("🎵 Генерирую музыку (это может занять некоторое время)...")
            client = get_music_client()
            audio_path, error = generate_music(client, prompt)
            if error:
                st.error(error)
                st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": error})
            else:
                # В случае успеха audio_path это кортеж (путь_к_аудио, путь_к_видео/картинке и т.д.)
                if isinstance(audio_path, tuple) and len(audio_path) > 0:
                    audio_file = audio_path[0]
                else:
                    audio_file = audio_path
                st.audio(audio_file)
                st.session_state.chat_history.append({"role": "assistant", "type": "audio", "content": audio_file})

        # Роутинг (Видео)
        elif any(word in prompt_lower for word in ['видео', 'ролик']):
            st.info("🎬 Генерирую видео (это может занять значительное время)...")
            client = get_video_client()
            video_path, error = generate_video(client, prompt)
            if error:
                st.error(error)
                st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": error})
            else:
                 # В случае успеха result это словарь с ключом 'video'
                if isinstance(video_path, dict) and 'video' in video_path:
                    v_path = video_path['video']
                else:
                    v_path = video_path
                st.video(v_path)
                st.session_state.chat_history.append({"role": "assistant", "type": "video", "content": v_path})

        # Роутинг (Текст по умолчанию)
        else:
            message_placeholder = st.empty()
            full_response = ""
            for chunk in generate_text_stream(st.session_state.chat_session, prompt):
                full_response += chunk
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
            st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": full_response})
