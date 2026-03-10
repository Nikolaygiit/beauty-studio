import streamlit as st
from PIL import Image

# Import our custom modules
from modules.text import generate_text_stream
from modules.image import generate_image
from modules.music import generate_music
from modules.video import generate_video

# --- App Configuration ---
st.set_page_config(
    page_title="Gemini Ultimate Bot",
    page_icon="✨",
    layout="wide",
)

st.title("✨ Gemini Ultimate Bot")
st.markdown("Универсальный бот для генерации текста, изображений, музыки и видео.")

# --- Sidebar Configuration ---
with st.sidebar:
    st.header("Настройки")
    api_key = st.text_input("Введите GOOGLE_API_KEY", type="password", help="Ключ нужен для работы текстовой модели Gemini.")

    st.divider()

    # "Clear Chat History" button logic handling
    if st.button("Очистить историю чата"):
        st.session_state.chat_history = []
        st.rerun()

generation_type = st.radio(
    "Выберите режим генерации",
    ["Текст (Чат)", "Изображение", "Музыка", "Видео"],
    horizontal=True
)
st.divider()

# --- Initialize Session State ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- Render Chat History for Text Mode ---
if generation_type == "Текст (Чат)":
    for message in st.session_state.chat_history:
        role = "user" if message["role"] == "user" else "assistant"
        with st.chat_message(role):
            st.markdown(message["parts"][0])

# --- Main Logic ---
prompt = st.chat_input("Введите ваш запрос...")

if prompt:
    if generation_type == "Текст (Чат)":
        with st.chat_message("user"):
            st.markdown(prompt)

        if not api_key:
            with st.chat_message("assistant"):
                st.error("Пожалуйста, введите GOOGLE_API_KEY в боковой панели.")
        else:
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                full_response = ""
                try:
                    for chunk in generate_text_stream(prompt, api_key, st.session_state.chat_history):
                        # Catch error chunk
                        if chunk.startswith("Произошла ошибка"):
                            st.error(chunk)
                            break
                        full_response += chunk
                        message_placeholder.markdown(full_response + "▌")
                    if full_response:
                        message_placeholder.markdown(full_response)
                except Exception as e:
                    st.error(f"Произошла ошибка: {str(e)}")

    elif generation_type == "Изображение":
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            with st.spinner("Генерация изображения..."):
                result = generate_image(prompt)
                if isinstance(result, str):
                    st.error(result)
                else:
                    st.image(result, caption=prompt)

    elif generation_type == "Музыка":
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            with st.spinner("Генерация музыки (это может занять некоторое время)..."):
                result = generate_music(prompt)
                if isinstance(result, str) and result.startswith("Произошла ошибка"):
                    st.error(result)
                elif result:
                    st.audio(result)

    elif generation_type == "Видео":
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            with st.spinner("Генерация видео (это может занять несколько минут)..."):
                result = generate_video(prompt)
                if isinstance(result, str) and (result.startswith("Произошла ошибка") or result.startswith("Ошибка инициализации")):
                    st.error(result)
                elif result:
                    st.video(result)
