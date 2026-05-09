import streamlit as st
import time
from modules.text import get_gemini_client, initialize_chat_session, generate_text_stream
from modules.image import generate_image
from modules.music import generate_music
from modules.video import generate_video

# --- UI Setup ---
st.set_page_config(page_title="Gemini Ultimate Bot", page_icon="✨", layout="wide")
st.title("✨ Gemini Ultimate Bot")
st.markdown("Генерация текста, изображений, музыки и видео!")

# --- State Management ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "chat_session" not in st.session_state:
    st.session_state.chat_session = None
if "gemini_client" not in st.session_state:
    st.session_state.gemini_client = None
if "current_api_key" not in st.session_state:
    st.session_state.current_api_key = ""

# --- Sidebar ---
st.sidebar.header("Настройки API")
api_key_input = st.sidebar.text_input("Введите Google API Key:", type="password", value=st.session_state.current_api_key)

def reset_chat():
    st.session_state.chat_history = []
    st.session_state.chat_session = None
    st.session_state.gemini_client = None
    st.session_state.current_api_key = ""
    st.rerun()

st.sidebar.button("Очистить историю чата", on_click=reset_chat)

# Initialize client if key changes
if api_key_input and api_key_input != st.session_state.current_api_key:
    st.session_state.current_api_key = api_key_input
    st.session_state.gemini_client = get_gemini_client(api_key_input)
    if st.session_state.gemini_client:
        st.session_state.chat_session = initialize_chat_session(st.session_state.gemini_client)
    st.session_state.chat_history = []

# --- Helper logic for routing ---
def determine_media_type(prompt: str) -> str:
    prompt_lower = prompt.lower()
    if any(keyword in prompt_lower for keyword in ['нарисуй', 'фото', 'изображение']):
        return "image"
    elif any(keyword in prompt_lower for keyword in ['музыка', 'песня', 'трек']):
        return "music"
    elif any(keyword in prompt_lower for keyword in ['видео', 'ролик']):
        return "video"
    return "text"

# --- Main App Execution ---
# Display previous chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        if message["type"] == "text":
            st.markdown(message["content"])
        elif message["type"] == "image":
            st.markdown(f"Вот ваше изображение по запросу: '{message['prompt']}'")
            st.image(message["content"])
        elif message["type"] == "music":
            st.markdown(f"Вот ваша музыка по запросу: '{message['prompt']}'")
            st.audio(message["content"])
        elif message["type"] == "video":
            st.markdown(f"Вот ваше видео по запросу: '{message['prompt']}'")
            st.video(message["content"])

# Prompt Input
if prompt := st.chat_input("Введите ваш запрос... (например: 'нарисуй кота', 'сочини музыку')"):

    # 1. Add user message to history and show it
    st.session_state.chat_history.append({"role": "user", "type": "text", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Check if API key is present
    if not st.session_state.chat_session:
        error_msg = "Пожалуйста, введите валидный Google API Key в боковой панели, чтобы использовать бота."
        with st.chat_message("assistant"):
            st.error(error_msg)
        st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": error_msg})
    else:
        # 3. Route to the right generator
        media_type = determine_media_type(prompt)

        with st.chat_message("assistant"):
            if media_type == "text":
                with st.spinner("Генерация текста..."):
                    stream = generate_text_stream(st.session_state.chat_session, prompt)

                    if isinstance(stream, str):
                         # An error string was returned
                         st.error(stream)
                         st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": stream})
                    else:
                         # Successfully returned a generator stream
                         response_placeholder = st.empty()
                         full_response = ""
                         for chunk in stream:
                             if chunk.text:
                                 full_response += chunk.text
                             response_placeholder.markdown(full_response + "▌")
                         response_placeholder.markdown(full_response)
                         st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": full_response})

            elif media_type == "image":
                with st.spinner("Генерация изображения..."):
                    url, error = generate_image(prompt)
                    if error:
                        st.error(error)
                        st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": error})
                    else:
                        st.image(url)
                        st.session_state.chat_history.append({"role": "assistant", "type": "image", "content": url, "prompt": prompt})

            elif media_type == "music":
                with st.spinner("Генерация музыки (это может занять некоторое время)..."):
                    path, error = generate_music(prompt)
                    if error:
                        st.error(error)
                        st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": error})
                    else:
                        st.audio(path)
                        st.session_state.chat_history.append({"role": "assistant", "type": "music", "content": path, "prompt": prompt})

            elif media_type == "video":
                with st.spinner("Генерация видео (это может занять несколько минут)..."):
                    path, error = generate_video(prompt)
                    if error:
                        st.error(error)
                        st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": error})
                    else:
                        st.video(path)
                        st.session_state.chat_history.append({"role": "assistant", "type": "video", "content": path, "prompt": prompt})
