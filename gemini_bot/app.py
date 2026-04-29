import streamlit as st
from modules.text import get_chat_session, generate_text
from modules.image import generate_image
from modules.music import generate_music
from modules.video import generate_video

st.set_page_config(page_title="Gemini Ultimate Bot", page_icon="✨", layout="centered")

# --- Session State Initialization ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "chat_session" not in st.session_state:
    st.session_state.chat_session = None
if "gemini_client" not in st.session_state:
    st.session_state.gemini_client = None
if "current_api_key" not in st.session_state:
    st.session_state.current_api_key = ""

# --- Sidebar Configuration ---
with st.sidebar:
    st.title("Настройки ⚙️")
    api_key = st.text_input("Введите GOOGLE_API_KEY", type="password", value=st.session_state.current_api_key)

    if api_key != st.session_state.current_api_key:
        st.session_state.current_api_key = api_key
        st.session_state.chat_session = None
        st.session_state.gemini_client = None
        st.session_state.chat_history = []

    if st.button("Очистить историю чата"):
        st.session_state.chat_history = []
        st.session_state.chat_session = None
        st.session_state.gemini_client = None

# --- Main App ---
st.title("✨ Gemini Ultimate Bot")
st.markdown("Генерация текста, изображений, музыки и видео!")

# Initialize Chat Session if API Key is provided
if st.session_state.current_api_key and st.session_state.chat_session is None:
    client, chat_session, error_msg = get_chat_session(st.session_state.current_api_key)
    if error_msg:
        st.error(error_msg)
    else:
        st.session_state.gemini_client = client
        st.session_state.chat_session = chat_session
        st.success("Gemini API успешно подключен!")
elif not st.session_state.current_api_key:
    st.info("Пожалуйста, введите ваш Google API Key в боковой панели.")

# --- Display Chat History ---
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

# --- Cached Wrappers for Heavy Generators ---
@st.cache_resource(show_spinner=False)
def cached_generate_music(prompt):
    return generate_music(prompt)

@st.cache_resource(show_spinner=False)
def cached_generate_video(prompt):
    return generate_video(prompt)

# --- Handle User Input ---
if prompt := st.chat_input("Напишите сообщение..."):
    # Добавляем сообщение пользователя в историю
    st.session_state.chat_history.append({"role": "user", "type": "text", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        prompt_lower = prompt.lower()

        # --- Routing Logic ---
        # Изображение
        if any(keyword in prompt_lower for keyword in ['нарисуй', 'фото', 'изображение']):
            with st.spinner("Генерация изображения..."):
                image_url, error = generate_image(prompt)
                if error:
                    st.error(error)
                else:
                    st.image(image_url)
                    st.session_state.chat_history.append({"role": "assistant", "type": "image", "content": image_url})

        # Музыка
        elif any(keyword in prompt_lower for keyword in ['музыка', 'песня', 'трек']):
            with st.spinner("Генерация музыки (это может занять время)..."):
                audio_path, error = cached_generate_music(prompt)
                if error:
                    st.error(error)
                else:
                    st.audio(audio_path)
                    st.session_state.chat_history.append({"role": "assistant", "type": "audio", "content": audio_path})

        # Видео
        elif any(keyword in prompt_lower for keyword in ['видео', 'ролик']):
            with st.spinner("Генерация видео (это может занять время)..."):
                video_path, error = cached_generate_video(prompt)
                if error:
                    st.error(error)
                else:
                    st.video(video_path)
                    st.session_state.chat_history.append({"role": "assistant", "type": "video", "content": video_path})

        # Текст (Default)
        else:
            if st.session_state.chat_session:
                with st.spinner("Генерация текста..."):
                    text_response = generate_text(st.session_state.chat_session, prompt)
                    st.markdown(text_response)
                    st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": text_response})
            else:
                st.warning("Для текстовых ответов требуется Google API Key.")
