import streamlit as st
from modules.text import get_gemini_client, initialize_chat, generate_text_stream
from modules.image import generate_image_url
from modules.music import initialize_music_client, generate_music
from modules.video import initialize_video_client, generate_video

# --- STREAMLIT PAGE CONFIGURATION ---
st.set_page_config(page_title="Gemini Ultimate Bot", page_icon="🤖", layout="wide")

st.title("Gemini Ultimate Bot 🤖")
st.markdown("Универсальный бот с генерацией текста, изображений, музыки и видео.")

# --- SIDEBAR CONFIGURATION ---
with st.sidebar:
    st.header("Настройки")
    api_key = st.text_input("Введите GOOGLE_API_KEY", type="password")
    st.markdown("---")

    if st.button("Очистить историю чата", use_container_width=True):
        st.session_state.chat_session = None
        st.session_state.messages = []
        st.rerun()

    st.markdown("### Поддерживаемые команды")
    st.markdown("- **Текст**: Обычный запрос")
    st.markdown("- **Изображение**: Начни с *нарисуй*, *фото*, *изображение*")
    st.markdown("- **Музыка**: Начни с *музыка*, *песня*, *трек*")
    st.markdown("- **Видео**: Начни с *видео*, *ролик*")

# --- CACHING RESOURCE-HEAVY CLIENTS ---
@st.cache_resource
def get_music_client():
    return initialize_music_client()

@st.cache_resource
def get_video_client():
    return initialize_video_client()

# --- INITIALIZE SESSION STATE ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat_session" not in st.session_state:
    st.session_state.chat_session = None

# --- DISPLAY CHAT HISTORY ---
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

# --- HANDLE USER INPUT ---
if prompt := st.chat_input("Введите ваш запрос..."):
    # Check if API key is provided
    if not api_key:
        st.warning("Пожалуйста, введите GOOGLE_API_KEY в боковой панели.")
        st.stop()

    # Initialize Gemini chat session if not already initialized
    if st.session_state.chat_session is None:
        gemini_client = get_gemini_client(api_key)
        if gemini_client is None:
            st.error("Не удалось инициализировать клиент Gemini. Проверьте ваш API ключ.")
            st.stop()
        st.session_state.chat_session = initialize_chat(gemini_client)
        if st.session_state.chat_session is None:
            st.error("Не удалось создать сессию чата Gemini.")
            st.stop()

    # Display user prompt
    st.session_state.messages.append({"role": "user", "type": "text", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    prompt_lower = prompt.lower().strip()

    # --- ROUTING LOGIC ---
    with st.chat_message("assistant"):
        # Image Routing
        if any(prompt_lower.startswith(keyword) for keyword in ['нарисуй', 'фото', 'изображение']):
            with st.spinner("Генерирую изображение..."):
                image_url = generate_image_url(prompt)
                st.image(image_url)
                st.session_state.messages.append({"role": "assistant", "type": "image", "content": image_url})

        # Music Routing
        elif any(prompt_lower.startswith(keyword) for keyword in ['музыка', 'песня', 'трек']):
            with st.spinner("Генерирую музыку..."):
                music_client = get_music_client()
                audio_path, error = generate_music(music_client, prompt)
                if error:
                    st.error(error)
                    st.session_state.messages.append({"role": "assistant", "type": "text", "content": error})
                elif audio_path:
                    # Gradio client returns a tuple for audio, the actual file path is the first element
                    actual_audio_path = audio_path[0] if isinstance(audio_path, tuple) else audio_path
                    st.audio(actual_audio_path)
                    st.session_state.messages.append({"role": "assistant", "type": "audio", "content": actual_audio_path})
                else:
                    st.error("Не удалось сгенерировать музыку.")

        # Video Routing
        elif any(prompt_lower.startswith(keyword) for keyword in ['видео', 'ролик']):
            with st.spinner("Генерирую видео..."):
                video_client = get_video_client()
                video_path, error = generate_video(video_client, prompt)
                if error:
                    st.error(error)
                    st.session_state.messages.append({"role": "assistant", "type": "text", "content": error})
                elif video_path:
                     # Gradio client returns a dictionary for video, the actual file path is inside 'video'
                    actual_video_path = video_path.get('video') if isinstance(video_path, dict) else video_path
                    st.video(actual_video_path)
                    st.session_state.messages.append({"role": "assistant", "type": "video", "content": actual_video_path})
                else:
                    st.error("Не удалось сгенерировать видео.")

        # Text Routing (Default)
        else:
             with st.spinner("Генерирую текст..."):
                response_placeholder = st.empty()
                full_response = ""

                # We use send_message_stream with google-genai client.chats.create
                try:
                    stream = st.session_state.chat_session.send_message_stream(prompt)
                    for chunk in stream:
                        if chunk.text:
                            full_response += chunk.text
                            response_placeholder.markdown(full_response + "▌")
                    response_placeholder.markdown(full_response)
                    st.session_state.messages.append({"role": "assistant", "type": "text", "content": full_response})
                except Exception as e:
                    error_msg = f"Произошла ошибка при генерации текста: {e}"
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "type": "text", "content": error_msg})
