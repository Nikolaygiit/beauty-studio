import streamlit as st
from modules.text import get_chat_session, generate_text
from modules.image import generate_image_url
from modules.music import get_music_client, generate_music
from modules.video import get_video_client, generate_video

# --- Caching Heavy Resources ---
@st.cache_resource
def load_music_client():
    return get_music_client()

@st.cache_resource
def load_video_client():
    return get_video_client()

# --- Page Config ---
st.set_page_config(page_title="Gemini Ultimate Bot", page_icon="🤖", layout="wide")
st.title("🤖 Gemini Ultimate Bot")
st.write("Привет! Я универсальный бот. Я могу общаться, рисовать картинки, создавать музыку и видео.")

# --- Sidebar ---
with st.sidebar:
    st.header("Настройки")
    api_key = st.text_input("Введите GOOGLE_API_KEY", type="password")
    if st.button("Очистить историю чата"):
        st.session_state.chat_history = []
        if 'chat_session' in st.session_state:
            del st.session_state.chat_session
        st.success("История очищена!")

# --- Session State Initialization ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "api_key" not in st.session_state:
    st.session_state.api_key = ""

if api_key != st.session_state.api_key:
    st.session_state.api_key = api_key
    if api_key:
        st.session_state.chat_session = get_chat_session(api_key)
    elif "chat_session" in st.session_state:
        del st.session_state.chat_session
elif api_key and "chat_session" not in st.session_state:
    st.session_state.chat_session = get_chat_session(api_key)

# --- Display Chat History ---
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        if message["type"] == "text":
            st.markdown(message["content"])
        elif message["type"] == "image":
            st.image(message["content"])
        elif message["type"] == "music":
            st.audio(message["content"])
        elif message["type"] == "video":
            st.video(message["content"])

# --- Routing Logic ---
def route_request(prompt_lower):
    if any(keyword in prompt_lower for keyword in ['нарисуй', 'фото', 'изображение']):
        return "image"
    elif any(keyword in prompt_lower for keyword in ['музыка', 'песня', 'трек']):
        return "music"
    elif any(keyword in prompt_lower for keyword in ['видео', 'ролик']):
        return "video"
    else:
        return "text"

# --- Main Chat Input ---
if prompt := st.chat_input("Напишите сообщение..."):
    # Append user message
    st.session_state.chat_history.append({"role": "user", "type": "text", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    prompt_lower = prompt.lower()
    intent = route_request(prompt_lower)

    with st.chat_message("assistant"):
        if intent == "image":
            with st.spinner("Создаю изображение..."):
                image_url = generate_image_url(prompt)
                st.image(image_url)
                st.session_state.chat_history.append({"role": "assistant", "type": "image", "content": image_url})

        elif intent == "music":
            with st.spinner("Создаю музыку (это может занять время)..."):
                client = load_music_client()
                error, audio_path = generate_music(client, prompt)
                if error:
                    st.error(error)
                    st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": error})
                elif audio_path:
                    st.audio(audio_path)
                    st.session_state.chat_history.append({"role": "assistant", "type": "music", "content": audio_path})

        elif intent == "video":
            with st.spinner("Создаю видео (это может занять время)..."):
                client = load_video_client()
                error, video_path = generate_video(client, prompt)
                if error:
                    st.error(error)
                    st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": error})
                elif video_path:
                    st.video(video_path)
                    st.session_state.chat_history.append({"role": "assistant", "type": "video", "content": video_path})

        else: # Text fallback
            if not api_key:
                warning_msg = "Пожалуйста, введите GOOGLE_API_KEY в боковой панели для текстового чата."
                st.warning(warning_msg)
                st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": warning_msg})
            elif st.session_state.chat_session:
                with st.spinner("Думаю..."):
                    response_text = generate_text(st.session_state.chat_session, prompt)
                    st.markdown(response_text)
                    st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": response_text})
            else:
                error_msg = "Не удалось инициализировать чат с предоставленным ключом."
                st.error(error_msg)
                st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": error_msg})
