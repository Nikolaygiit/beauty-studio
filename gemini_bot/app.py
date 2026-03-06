import streamlit as st
import google.generativeai as genai
from modules.text import get_gemini_model, generate_text_stream
from modules.image import generate_image
from modules.music import generate_music, get_music_client
from modules.video import generate_video, get_video_client

# Streamlit page config
st.set_page_config(
    page_title="Gemini Ultimate Bot",
    page_icon="🤖",
    layout="wide",
)

st.title("Gemini Ultimate Bot 🤖")
st.markdown("Добро пожаловать! Этот бот умеет генерировать текст, изображения, музыку и видео.")

# Sidebar
with st.sidebar:
    st.header("Настройки")
    api_key = st.text_input("Введите GOOGLE_API_KEY", type="password")

    if st.button("Очистить историю чата"):
        st.session_state.messages = []
        if "chat_session" in st.session_state:
            del st.session_state.chat_session
        st.rerun()

    mode = st.radio(
        "Выберите режим",
        ["Текст (Чат)", "Изображение", "Музыка", "Видео"]
    )

if not api_key:
    st.warning("Пожалуйста, введите GOOGLE_API_KEY в боковой панели.")
    st.stop()

# Configure GenAI
genai.configure(api_key=api_key)

# Initialize Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_session" not in st.session_state:
    model = get_gemini_model()
    # Create history respecting Gemini strict role alternation
    # The history format expected is:
    # [
    #   {"role": "user", "parts": ["text"]},
    #   {"role": "model", "parts": ["text"]}
    # ]
    # st.session_state.messages stores our chat log.
    # For now, start empty.
    st.session_state.chat_session = model.start_chat(history=[])

@st.cache_resource
def get_cached_music_client():
    return get_music_client()

@st.cache_resource
def get_cached_video_client():
    return get_video_client()

# App logic based on mode
if mode == "Текст (Чат)":
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Напишите сообщение..."):
        # Add user message to state
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate response
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""

            try:
                # Streaming the response
                for chunk in generate_text_stream(st.session_state.chat_session, prompt):
                    if hasattr(chunk, 'text'):
                        full_response += chunk.text
                    elif isinstance(chunk, str): # In case of our custom error generator
                        full_response += chunk
                    message_placeholder.markdown(full_response + "▌")
                message_placeholder.markdown(full_response)
            except Exception as e:
                full_response = f"Произошла ошибка: {str(e)}"
                message_placeholder.markdown(full_response)

        # Add assistant message to state
        st.session_state.messages.append({"role": "assistant", "content": full_response})

elif mode == "Изображение":
    st.subheader("Генерация изображений (Pollinations.ai)")
    prompt = st.text_input("Опишите изображение на английском языке:")
    if st.button("Сгенерировать"):
        if prompt:
            with st.spinner("Генерация изображения..."):
                try:
                    img = generate_image(prompt)
                    st.image(img, caption=prompt)
                except Exception as e:
                    st.error(f"Ошибка при генерации изображения: {e}")
        else:
            st.warning("Пожалуйста, введите описание.")

elif mode == "Музыка":
    st.subheader("Генерация музыки (MusicGen Streaming)")
    prompt = st.text_input("Опишите музыку на английском языке (например, '80s pop track with synth and instrumentals'):")
    if st.button("Сгенерировать музыку"):
        if prompt:
            with st.spinner("Генерация музыки..."):
                try:
                    client = get_cached_music_client()
                    audio_path = generate_music(client, prompt)
                    # The result is typically a tuple
                    if isinstance(audio_path, tuple):
                        st.audio(audio_path[0])
                    else:
                        st.audio(audio_path)
                except Exception as e:
                    st.error(f"Ошибка при генерации музыки: {e}")
        else:
            st.warning("Пожалуйста, введите описание.")

elif mode == "Видео":
    st.subheader("Генерация видео (ModelScope Text-to-Video)")
    prompt = st.text_input("Опишите видео на английском языке:")
    if st.button("Сгенерировать видео"):
        if prompt:
            with st.spinner("Генерация видео (это может занять некоторое время)..."):
                try:
                    client = get_cached_video_client()
                    video_path = generate_video(client, prompt)
                    st.video(video_path)
                except Exception as e:
                    st.error(f"Ошибка при генерации видео: {e}")
        else:
            st.warning("Пожалуйста, введите описание.")
