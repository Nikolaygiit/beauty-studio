import streamlit as st
from modules.routing import determine_route
from modules.text import get_client, create_chat_session, generate_text_stream
from modules.image import generate_image
from modules.music import generate_music
from modules.video import generate_video

# --- Session State Initialization ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "gemini_client" not in st.session_state:
    st.session_state.gemini_client = None
if "chat_session" not in st.session_state:
    st.session_state.chat_session = None
if "current_api_key" not in st.session_state:
    st.session_state.current_api_key = ""

# --- UI Setup ---
st.set_page_config(page_title="Gemini Ultimate Bot", page_icon="✨", layout="wide")
st.title("✨ Gemini Ultimate Bot")
st.markdown("Генерация текста, изображений, музыки и видео на базе ИИ.")

# --- Sidebar ---
with st.sidebar:
    st.header("Настройки")
    api_key = st.text_input("Google API Key", type="password")

    if api_key != st.session_state.current_api_key:
        st.session_state.current_api_key = api_key
        st.session_state.gemini_client = get_client(api_key)
        if st.session_state.gemini_client:
             st.session_state.chat_session = create_chat_session(st.session_state.gemini_client)
        else:
             st.session_state.chat_session = None

    if st.button("Очистить историю"):
        st.session_state.chat_history = []
        if st.session_state.gemini_client:
            st.session_state.chat_session = create_chat_session(st.session_state.gemini_client)

# --- Main Chat Area ---
# Display chat history
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

# Handle user input
prompt = st.chat_input("Введите ваш запрос...")

if prompt:
    if not api_key:
         st.error("Пожалуйста, введите Google API Key в боковой панели.")
    elif not st.session_state.chat_session:
         st.error("Ошибка инициализации Gemini API. Проверьте ключ.")
    else:
        # Display user prompt
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.chat_history.append({"role": "user", "type": "text", "content": prompt})

        # Determine route
        route = determine_route(prompt)

        with st.chat_message("assistant"):
            if route == "text":
                response_placeholder = st.empty()
                full_response = ""
                for chunk_text in generate_text_stream(st.session_state.gemini_client, st.session_state.chat_session, prompt):
                    if chunk_text:
                        full_response += chunk_text
                        response_placeholder.markdown(full_response + "▌")
                response_placeholder.markdown(full_response)
                st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": full_response})

            elif route == "image":
                with st.spinner("Рисую изображение..."):
                    url, error = generate_image(prompt)
                    if error:
                        st.error(error)
                        st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": error})
                    else:
                        st.image(url)
                        st.session_state.chat_history.append({"role": "assistant", "type": "image", "content": url})

            elif route == "music":
                 with st.spinner("Создаю музыку..."):
                    audio_path, error = generate_music(prompt)
                    if error:
                        st.error(error)
                        st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": error})
                    else:
                        st.audio(audio_path)
                        st.session_state.chat_history.append({"role": "assistant", "type": "audio", "content": audio_path})

            elif route == "video":
                 with st.spinner("Генерирую видео..."):
                    video_path, error = generate_video(prompt)
                    if error:
                        st.error(error)
                        st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": error})
                    else:
                        st.video(video_path)
                        st.session_state.chat_history.append({"role": "assistant", "type": "video", "content": video_path})
