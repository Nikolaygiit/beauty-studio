import streamlit as st
from gradio_client import Client
from modules.text import generate_text_stream
from modules.image import generate_image_url
from modules.music import generate_music
from modules.video import generate_video

# --- Конфигурация страницы ---
st.set_page_config(
    page_title="Gemini Ultimate Bot",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Gemini Ultimate Bot")
st.markdown("Добро пожаловать! Я могу генерировать текст, изображения, музыку и видео. "
            "Чтобы сгенерировать медиа, начните свой запрос со слов: **'нарисуй'** (изображение), "
            "**'музыка'** (аудио) или **'видео'** (видео).")

# --- Управление состоянием ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "gemini_history" not in st.session_state:
    st.session_state.gemini_history = []

# --- Сайдбар ---
with st.sidebar:
    st.header("Настройки")
    api_key = st.text_input("Введите ваш Google API Key", type="password")

    if st.button("Очистить историю чата"):
        st.session_state.messages = []
        st.session_state.gemini_history = []
        st.rerun()

    st.markdown("---")
    st.markdown("### Подсказки:")
    st.markdown("- **Текст:** Просто напишите любой вопрос.")
    st.markdown("- **Изображение:** `нарисуй кота в космосе`")
    st.markdown("- **Музыка:** `музыка веселая мелодия на пианино`")
    st.markdown("- **Видео:** `видео собака бежит по пляжу`")

# --- Инициализация клиентов (Кэширование) ---
@st.cache_resource
def get_music_client():
    try:
        return Client("sanchit-gandhi/musicgen-streaming")
    except Exception as e:
        st.error(f"Не удалось загрузить модель генерации музыки: {e}")
        return None

@st.cache_resource
def get_video_client():
    try:
        return Client("damo-vilab/modelscope-text-to-video-synthesis")
    except Exception as e:
        st.error(f"Не удалось загрузить модель генерации видео: {e}")
        return None

# Инициализируем клиентов в фоне
music_client = get_music_client()
video_client = get_video_client()


# --- Отображение истории чата ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg["type"] == "text":
            st.markdown(msg["content"])
        elif msg["type"] == "image":
            st.image(msg["content"], caption=msg.get("caption", ""))
        elif msg["type"] == "audio":
            st.audio(msg["content"])
        elif msg["type"] == "video":
            st.video(msg["content"])


# --- Обработка ввода пользователя ---
prompt = st.chat_input("Введите ваше сообщение...")

if prompt:
    # Проверка ключа (только для текста)
    is_media = prompt.lower().startswith(("нарисуй", "фото", "изображение", "музыка", "видео"))
    if not api_key and not is_media:
        st.info("Пожалуйста, введите Google API Key в боковой панели.")
        st.stop()

    # Добавляем сообщение пользователя в UI
    st.session_state.messages.append({"role": "user", "type": "text", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Определяем интент (intent)
    prompt_lower = prompt.lower()

    with st.chat_message("assistant"):
        # --- ГЕНЕРАЦИЯ ИЗОБРАЖЕНИЯ ---
        if prompt_lower.startswith(("нарисуй", "фото", "изображение")):
            # Удаляем префикс, игнорируя регистр
            clean_prompt = prompt
            for prefix in ("нарисуй", "фото", "изображение"):
                if prompt_lower.startswith(prefix):
                    clean_prompt = prompt[len(prefix):].strip()
                    break

            if not clean_prompt:
                clean_prompt = "beautiful landscape"

            with st.spinner("Создаю изображение..."):
                image_url = generate_image_url(clean_prompt)
                st.image(image_url, caption=clean_prompt)
                st.session_state.messages.append({
                    "role": "assistant", "type": "image", "content": image_url, "caption": clean_prompt
                })

        # --- ГЕНЕРАЦИЯ МУЗЫКИ ---
        elif prompt_lower.startswith("музыка"):
            clean_prompt = prompt[len("музыка"):].strip()
            if not clean_prompt:
                clean_prompt = "lofi hip hop beat"

            with st.spinner("Создаю музыку (это может занять время)..."):
                audio_file, error = generate_music(clean_prompt, music_client)
                if error:
                    st.error(error)
                    st.session_state.messages.append({"role": "assistant", "type": "text", "content": error})
                elif audio_file:
                    st.audio(audio_file)
                    st.session_state.messages.append({
                        "role": "assistant", "type": "audio", "content": audio_file
                    })

        # --- ГЕНЕРАЦИЯ ВИДЕО ---
        elif prompt_lower.startswith("видео"):
            clean_prompt = prompt[len("видео"):].strip()
            if not clean_prompt:
                clean_prompt = "a cat playing with a ball"

            with st.spinner("Создаю видео (это может занять время)..."):
                video_file_tuple, error = generate_video(clean_prompt, video_client)
                if error:
                    st.error(error)
                    st.session_state.messages.append({"role": "assistant", "type": "text", "content": error})
                elif video_file_tuple:
                    # video_file_tuple is often a path or a dict depending on gradio version, usually a string path
                    # Handle typical damo-vilab output which is a tuple where first element is path
                    video_path = video_file_tuple[0] if isinstance(video_file_tuple, tuple) else video_file_tuple
                    try:
                        st.video(video_path)
                        st.session_state.messages.append({
                            "role": "assistant", "type": "video", "content": video_path
                        })
                    except Exception as e:
                        st.error(f"Не удалось отобразить видео: {e}")

        # --- ГЕНЕРАЦИЯ ТЕКСТА (Gemini) ---
        else:
            with st.spinner("Думаю..."):
                try:
                    # Используем потоковый вывод через st.write_stream
                    # Функция generate_text_stream должна возвращать генератор
                    stream = generate_text_stream(prompt, api_key, history=st.session_state.gemini_history)

                    response_text = st.write_stream(stream)

                    # Обновляем историю сообщений
                    st.session_state.messages.append({"role": "assistant", "type": "text", "content": response_text})

                    # Обновляем историю для Gemini (сохраняем контекст)
                    st.session_state.gemini_history.append({"role": "user", "parts": [prompt]})
                    st.session_state.gemini_history.append({"role": "model", "parts": [response_text]})

                except Exception as e:
                    error_msg = f"Произошла ошибка: {str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "type": "text", "content": error_msg})
