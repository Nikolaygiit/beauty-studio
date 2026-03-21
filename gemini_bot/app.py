import streamlit as st
import os

from modules.text import get_gemini_client, init_chat_session, generate_text_stream
from modules.image import generate_image
from modules.music import get_music_generator
from modules.video import get_video_generator

# Установим конфигурацию страницы
st.set_page_config(page_title="Gemini Ultimate Bot", page_icon="🤖", layout="wide")

# Заголовок приложения
st.title("🤖 Gemini Ultimate Bot")
st.markdown("Добро пожаловать в лучшего бота с генерацией текста, изображений, музыки и видео! \n*Подсказка: чтобы сгенерировать медиа, начните запрос со слов: `нарисуй`, `музыка` или `видео`.*")

# Инициализируем генераторы тяжелых медиа один раз на запуск (кешируем)
@st.cache_resource
def load_music_generator():
    return get_music_generator()

@st.cache_resource
def load_video_generator():
    return get_video_generator()

music_gen = load_music_generator()
video_gen = load_video_generator()

# Сайдбар для настроек и очистки истории
with st.sidebar:
    st.header("Настройки")
    api_key = st.text_input("Введи свой Google Gemini API Key:", type="password", help="Получить ключ можно в Google AI Studio")

    if st.button("Очистить историю чата", use_container_width=True):
        st.session_state.messages = []
        if "chat_session" in st.session_state:
            del st.session_state.chat_session
        st.success("История очищена!")

# Проверяем наличие API-ключа
if not api_key:
    st.warning("Пожалуйста, введи API ключ Gemini в боковой панели, чтобы начать!")
    st.stop()

# Инициализируем клиент Gemini и сессию чата в session_state, если их нет
if "gemini_client" not in st.session_state or st.session_state.get("current_api_key") != api_key:
    client_or_err = get_gemini_client(api_key)
    if isinstance(client_or_err, str):
        st.error(client_or_err)
        st.stop()
    else:
        st.session_state.gemini_client = client_or_err
        st.session_state.current_api_key = api_key
        st.session_state.chat_session = init_chat_session(client_or_err)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Отображаем историю чата (сохраняем медиа в истории)
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg.get("type") == "image":
            st.image(msg["content"], use_container_width=True)
        elif msg.get("type") == "audio":
            if os.path.exists(msg["content"]):
                st.audio(msg["content"])
            else:
                st.error("Аудиофайл не найден.")
        elif msg.get("type") == "video":
            if os.path.exists(msg["content"]):
                st.video(msg["content"])
            else:
                st.error("Видеофайл не найден.")
        else:
            st.markdown(msg["content"])

# Поле ввода пользователя
if prompt := st.chat_input("Напиши сообщение..."):
    # Добавляем запрос пользователя в историю и отображаем
    st.session_state.messages.append({"role": "user", "content": prompt, "type": "text"})
    with st.chat_message("user"):
        st.markdown(prompt)

    prompt_lower = prompt.lower()

    # Роутинг медиа генерации на основе ключевых слов

    # Изображения
    if prompt_lower.startswith("нарисуй") or prompt_lower.startswith("фото") or prompt_lower.startswith("изображение"):
        with st.chat_message("assistant"):
            with st.spinner("Рисую шедевр... 🎨"):
                # Получаем запрос для картинки, удаляя триггер
                clean_prompt = prompt.replace("нарисуй", "", 1).replace("фото", "", 1).replace("изображение", "", 1).strip()
                if not clean_prompt:
                    clean_prompt = "beautiful landscape"

                image_url = generate_image(clean_prompt)
                st.image(image_url, use_container_width=True)
                st.session_state.messages.append({"role": "assistant", "content": image_url, "type": "image"})

    # Музыка
    elif prompt_lower.startswith("музыка") or prompt_lower.startswith("песня") or prompt_lower.startswith("трек"):
        with st.chat_message("assistant"):
            with st.spinner("Пишу хит... 🎵"):
                # Получаем запрос для музыки, удаляя триггер
                clean_prompt = prompt.replace("музыка", "", 1).replace("песня", "", 1).replace("трек", "", 1).strip()
                if not clean_prompt:
                    clean_prompt = "upbeat energetic pop synth track"

                result = music_gen.generate(clean_prompt)

                if isinstance(result, str) and (result.startswith("Ошибка") or result.startswith("Произошла ошибка")):
                    st.error(result)
                    st.session_state.messages.append({"role": "assistant", "content": result, "type": "text"})
                else:
                    # result - путь к аудио файлу
                    st.audio(result)
                    st.session_state.messages.append({"role": "assistant", "content": result, "type": "audio"})

    # Видео
    elif prompt_lower.startswith("видео") or prompt_lower.startswith("ролик"):
        with st.chat_message("assistant"):
            with st.spinner("Монтирую видео... 🎥 (может занять время)"):
                clean_prompt = prompt.replace("видео", "", 1).replace("ролик", "", 1).strip()
                if not clean_prompt:
                    clean_prompt = "A robot waving its hand"

                # Вызываем инкапсулированный метод генерации видео
                result = video_gen.generate(clean_prompt)

                if isinstance(result, str) and (result.startswith("The model is currently unavailable") or result.startswith("Произошла ошибка")):
                    st.error(result)
                    st.session_state.messages.append({"role": "assistant", "content": result, "type": "text"})
                else:
                    # result - путь к видео файлу
                    st.video(result)
                    st.session_state.messages.append({"role": "assistant", "content": result, "type": "video"})

    # Обычный текст (Gemini)
    else:
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""

            with st.spinner("Думаю... 🧠"):
                stream = generate_text_stream(st.session_state.chat_session, prompt)

                for chunk in stream:
                    full_response += chunk
                    message_placeholder.markdown(full_response + "▌")

                message_placeholder.markdown(full_response)

            st.session_state.messages.append({"role": "assistant", "content": full_response, "type": "text"})
