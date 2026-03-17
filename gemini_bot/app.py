import streamlit as st
from modules.text import init_chat_session, generate_text_stream
from modules.image import generate_image_url
from modules.music import get_music_client, generate_music
from modules.video import get_video_client, generate_video

# Настройка страницы
st.set_page_config(page_title="Gemini Ultimate Bot", page_icon="🤖", layout="wide")
st.title("🤖 Gemini Ultimate Bot")

# Кэширование тяжелых клиентов
@st.cache_resource
def load_music_client():
    return get_music_client()

@st.cache_resource
def load_video_client():
    return get_video_client()

# Боковая панель для ввода API ключа и настроек
with st.sidebar:
    st.header("Настройки")
    api_key = st.text_input("Введите ваш GOOGLE_API_KEY", type="password")
    if st.button("Очистить историю чата"):
        st.session_state.chat_session = None
        st.session_state.messages = []
        st.rerun()

# Инициализация сессии
if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_session" not in st.session_state:
    st.session_state.chat_session = None

if api_key and st.session_state.chat_session is None:
    st.session_state.chat_session = init_chat_session(api_key)

# Отображение истории чата
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["type"] == "text":
            st.markdown(message["content"])
        elif message["type"] == "image":
            st.image(message["content"])
        elif message["type"] == "audio":
            st.audio(message["content"])
        elif message["type"] == "video":
            st.video(message["content"])
        elif message["type"] == "error":
            st.error(message["content"])

# Обработка пользовательского ввода
if prompt := st.chat_input("Введите сообщение (напр., 'нарисуй кота', 'музыка 80s pop', 'видео машина едет')"):
    # Проверка наличия API ключа
    if not api_key:
        st.warning("Пожалуйста, введите GOOGLE_API_KEY в боковой панели.")
        st.stop()

    # Добавление сообщения пользователя в историю
    st.session_state.messages.append({"role": "user", "type": "text", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    prompt_lower = prompt.lower()

    # Роутинг: Изображение
    if prompt_lower.startswith(("нарисуй", "фото", "изображение")):
        # Убираем ключевое слово
        clean_prompt = prompt
        for kw in ["нарисуй ", "нарисуй", "фото ", "фото", "изображение ", "изображение"]:
            if prompt_lower.startswith(kw):
                clean_prompt = prompt[len(kw):].strip()
                break

        with st.chat_message("assistant"):
            st.markdown(f"Генерирую изображение по запросу: *{clean_prompt}*...")
            image_url = generate_image_url(clean_prompt)
            st.image(image_url)
            st.session_state.messages.append({"role": "assistant", "type": "image", "content": image_url})

    # Роутинг: Музыка
    elif prompt_lower.startswith(("музыка", "песня", "мелодия")):
        clean_prompt = prompt
        for kw in ["музыка ", "музыка", "песня ", "песня", "мелодия ", "мелодия"]:
            if prompt_lower.startswith(kw):
                clean_prompt = prompt[len(kw):].strip()
                break

        with st.chat_message("assistant"):
            with st.spinner(f"Создаю музыку: *{clean_prompt}*..."):
                music_client = load_music_client()
                audio_path, error = generate_music(music_client, clean_prompt)

                if error:
                    st.error(error)
                    st.session_state.messages.append({"role": "assistant", "type": "error", "content": error})
                elif audio_path:
                    st.audio(audio_path)
                    st.session_state.messages.append({"role": "assistant", "type": "audio", "content": audio_path})

    # Роутинг: Видео
    elif prompt_lower.startswith(("видео", "ролик")):
        clean_prompt = prompt
        for kw in ["видео ", "видео", "ролик ", "ролик"]:
            if prompt_lower.startswith(kw):
                clean_prompt = prompt[len(kw):].strip()
                break

        with st.chat_message("assistant"):
            with st.spinner(f"Создаю видео: *{clean_prompt}*..."):
                video_client = load_video_client()
                video_path, error = generate_video(video_client, clean_prompt)

                if error:
                    st.error(error)
                    st.session_state.messages.append({"role": "assistant", "type": "error", "content": error})
                elif video_path:
                    st.video(video_path)
                    st.session_state.messages.append({"role": "assistant", "type": "video", "content": video_path})

    # Роутинг: Текст (Gemini)
    else:
        with st.chat_message("assistant"):
            if st.session_state.chat_session:
                response_placeholder = st.empty()
                full_response = ""

                for chunk in generate_text_stream(st.session_state.chat_session, prompt):
                    full_response += chunk
                    response_placeholder.markdown(full_response + "▌")

                response_placeholder.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "type": "text", "content": full_response})
            else:
                st.error("Сессия чата не инициализирована. Проверьте ваш API ключ.")
