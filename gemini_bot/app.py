import streamlit as st
from modules.text import init_gemini, generate_text_stream
from modules.image import generate_image_url
from modules.music import get_music_client, generate_music
from modules.video import get_video_client, generate_video

# --- Page Configuration ---
st.set_page_config(
    page_title="Gemini Ultimate Bot",
    page_icon="✨",
    layout="wide"
)

st.title("✨ Gemini Ultimate Bot")
st.markdown("Генерация текста, изображений, музыки и видео.")

# --- Session State Initialization ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Caching Resource-Heavy Clients ---
@st.cache_resource
def load_music_client():
    return get_music_client()

@st.cache_resource
def load_video_client():
    return get_video_client()

# --- Sidebar ---
st.sidebar.title("Настройки")
api_key = st.sidebar.text_input("Введите GOOGLE_API_KEY", type="password")

if st.sidebar.button("Clear Chat History", use_container_width=True):
    st.session_state.messages = []
    st.rerun()

generation_mode = st.sidebar.radio(
    "Выберите режим генерации",
    ("Текст", "Изображение", "Музыка", "Видео")
)

# --- Main Logic ---
if not api_key:
    st.warning("Пожалуйста, введите ваш GOOGLE_API_KEY в боковой панели.")
    st.stop()

# Initialize Gemini Model
try:
    gemini_model = init_gemini(api_key)
except Exception as e:
    st.error(f"Ошибка инициализации Gemini: {e}")
    st.stop()

# Display Chat History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg["type"] == "text":
            st.markdown(msg["content"])
        elif msg["type"] == "image":
            st.image(msg["content"])
        elif msg["type"] == "music":
            st.audio(msg["content"])
        elif msg["type"] == "video":
            st.video(msg["content"])

# Chat Input
if prompt := st.chat_input("Введите ваш запрос..."):
    # Append user message
    st.session_state.messages.append({"role": "user", "type": "text", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        if generation_mode == "Текст":
            # Build history for Gemini: ensuring strict alternation of "user" and "model" roles.
            # We map "assistant" to "model". We will only append pairs or ensure the last added role isn't the same.
            gemini_history = []
            for msg in st.session_state.messages[:-1]: # exclude the latest prompt
                if msg["type"] == "text":
                    role = "user" if msg["role"] == "user" else "model"
                    if not gemini_history or gemini_history[-1]["role"] != role:
                        gemini_history.append({"role": role, "parts": [msg["content"]]})
                    else:
                        # Combine messages from the same role to maintain alternation
                        gemini_history[-1]["parts"][0] += f"\n\n{msg['content']}"

            # Gemini strictly expects alternating sequence starting with "user".
            # If the history somehow starts with "model", or ends with "user" before we send our actual prompt,
            # this logic handles it gracefully by keeping alternating sequences.

            response_container = st.empty()
            full_response = ""

            with st.spinner("Генерация текста..."):
                stream = generate_text_stream(gemini_model, prompt, history=gemini_history)
                for chunk in stream:
                    full_response += chunk
                    response_container.markdown(full_response + "▌")
                response_container.markdown(full_response)

            st.session_state.messages.append({"role": "assistant", "type": "text", "content": full_response})

        elif generation_mode == "Изображение":
            with st.spinner("Генерация изображения..."):
                image_url = generate_image_url(prompt)
                st.image(image_url)
            st.session_state.messages.append({"role": "assistant", "type": "image", "content": image_url})

        elif generation_mode == "Музыка":
            music_client = load_music_client()
            with st.spinner("Генерация музыки (это может занять время)..."):
                audio_path, error = generate_music(music_client, prompt)
                if error:
                    st.error(error)
                elif audio_path:
                    st.audio(audio_path)
                    st.session_state.messages.append({"role": "assistant", "type": "music", "content": audio_path})
                else:
                    st.error("Не удалось сгенерировать музыку.")

        elif generation_mode == "Видео":
            video_client = load_video_client()
            with st.spinner("Генерация видео (это может занять значительное время)..."):
                video_path, error = generate_video(video_client, prompt)
                if error:
                    st.error(error)
                elif video_path:
                    st.video(video_path)
                    st.session_state.messages.append({"role": "assistant", "type": "video", "content": video_path})
                else:
                    st.error("Не удалось сгенерировать видео.")
