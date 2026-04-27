import streamlit as st
import re
from modules.text import init_chat_session, generate_text_stream
from modules.image import generate_image
from modules.music import generate_music
from modules.video import generate_video

# --- Настройки страницы ---
st.set_page_config(
    page_title="Gemini Ultimate Bot",
    page_icon="✨",
    layout="wide"
)

# --- Инициализация State ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "chat_session" not in st.session_state:
    st.session_state.chat_session = None
if "gemini_client" not in st.session_state:
    st.session_state.gemini_client = None
if "current_api_key" not in st.session_state:
    st.session_state.current_api_key = ""

# --- Кэшированные функции генерации медиа (чтобы избежать ре-инициализации при ререндере) ---
@st.cache_resource
def cached_generate_music(prompt):
    return generate_music(prompt)

@st.cache_resource
def cached_generate_video(prompt):
    return generate_video(prompt)

# --- Боковая панель ---
with st.sidebar:
    st.title("⚙️ Настройки")
    api_key = st.text_input("Введите GOOGLE_API_KEY", type="password")

    if api_key != st.session_state.current_api_key:
        if api_key:
            client, chat = init_chat_session(api_key)
            if client:
                st.session_state.gemini_client = client
                st.session_state.chat_session = chat
                st.session_state.current_api_key = api_key
                st.success("API ключ принят и сессия инициализирована!")
            else:
                st.error(chat) # chat contains the error message here
        else:
            st.session_state.chat_session = None
            st.session_state.gemini_client = None
            st.session_state.current_api_key = ""

    if st.button("Очистить историю чата"):
        st.session_state.chat_history = []
        if api_key:
             client, chat = init_chat_session(api_key)
             st.session_state.chat_session = chat
             st.session_state.gemini_client = client
        st.rerun()

    st.markdown("---")
    st.markdown("""
    **Поддерживаемые команды:**
    - Обычный текст для общения.
    - Включите **нарисуй**, **фото**, **изображение** для генерации картинок.
    - Включите **музыка**, **песня**, **трек** для генерации аудио.
    - Включите **видео**, **ролик** для генерации видео.
    """)

# --- Основной интерфейс ---
st.title("✨ Gemini Ultimate Bot")

if not st.session_state.current_api_key:
    st.warning("Пожалуйста, введите ваш Google API Key в боковой панели, чтобы начать.")
    st.stop()

# Отображение истории
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        if msg["type"] == "text":
            st.markdown(msg["content"])
        elif msg["type"] == "image":
            st.image(msg["content"], caption="Сгенерированное изображение")
        elif msg["type"] == "audio":
            st.audio(msg["content"], format="audio/wav")
            st.markdown(f"**Аудио промпт:** {msg['prompt']}")
        elif msg["type"] == "video":
            st.video(msg["content"])
            st.markdown(f"**Видео промпт:** {msg['prompt']}")

# Ввод пользователя
prompt = st.chat_input("Введите ваш запрос...")

if prompt:
    # Добавляем запрос пользователя в историю
    st.session_state.chat_history.append({"role": "user", "type": "text", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    prompt_lower = prompt.lower()

    # --- Маршрутизация запросов ---
    with st.chat_message("assistant"):
        # 1. Проверка на Изображение
        if any(word in prompt_lower for word in ["нарисуй", "фото", "изображение"]):
            with st.spinner("Создаю изображение..."):
                img_url, err = generate_image(prompt)
                if err:
                    st.error(err)
                    st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": f"❌ {err}"})
                else:
                    st.image(img_url, caption="Сгенерированное изображение")
                    st.session_state.chat_history.append({"role": "assistant", "type": "image", "content": img_url, "prompt": prompt})

        # 2. Проверка на Музыку
        elif any(word in prompt_lower for word in ["музыка", "песня", "трек"]):
             with st.spinner("Создаю музыку (это может занять некоторое время)..."):
                # Удаляем триггерные слова из промпта для лучшей генерации, хотя модель может и сама справиться
                audio_path, err = cached_generate_music(prompt)
                if err:
                    st.error(err)
                    st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": f"❌ {err}"})
                else:
                    st.audio(audio_path, format="audio/wav")
                    st.session_state.chat_history.append({"role": "assistant", "type": "audio", "content": audio_path, "prompt": prompt})

        # 3. Проверка на Видео
        elif any(word in prompt_lower for word in ["видео", "ролик"]):
             with st.spinner("Создаю видео (это занимает несколько минут)..."):
                video_path, err = cached_generate_video(prompt)
                if err:
                    st.error(err)
                    st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": f"❌ {err}"})
                else:
                    st.video(video_path)
                    st.session_state.chat_history.append({"role": "assistant", "type": "video", "content": video_path, "prompt": prompt})

        # 4. Обычный текстовый запрос к Gemini
        else:
             with st.spinner("Думаю..."):
                 response_stream, err = generate_text_stream(st.session_state.chat_session, prompt)
                 if err:
                     st.error(err)
                     st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": f"❌ {err}"})
                 else:
                     # Для Streamlit используем st.write_stream, если поддерживается,
                     # или собираем чанки вручную.
                     # API google-genai response - это итератор
                     full_response = ""
                     message_placeholder = st.empty()

                     try:
                         for chunk in response_stream:
                             if chunk.text:
                                 full_response += chunk.text
                                 message_placeholder.markdown(full_response + "▌")
                         message_placeholder.markdown(full_response)
                         st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": full_response})
                     except Exception as stream_err:
                         st.error(f"Ошибка при получении потока: {stream_err}")
                         st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": f"❌ Ошибка генерации: {stream_err}"})
