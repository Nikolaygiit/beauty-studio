import streamlit as st
import re
from modules.image import generate_image
from modules.music import generate_music
from modules.video import generate_video
from modules.text import get_gemini_client, initialize_chat, send_message_stream

st.set_page_config(page_title="Gemini Ultimate Bot", page_icon="🤖")

st.title("Gemini Ultimate Bot")
st.write("Привет! Я могу генерировать текст, изображения, музыку и видео.")

# --- Sidebar ---
st.sidebar.title("Настройки")
api_key = st.sidebar.text_input("Введите GOOGLE_API_KEY", type="password")

if st.sidebar.button("Очистить историю чата"):
    st.session_state.chat_history = []
    st.session_state.chat_session = None
    st.session_state.gemini_client = None
    st.session_state.current_api_key = None
    st.rerun()

# --- State Management ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "chat_session" not in st.session_state:
    st.session_state.chat_session = None
if "gemini_client" not in st.session_state:
    st.session_state.gemini_client = None
if "current_api_key" not in st.session_state:
    st.session_state.current_api_key = None

# --- Re-initialize client if API key changes ---
if api_key and api_key != st.session_state.current_api_key:
    client, error = get_gemini_client(api_key)
    if error:
        st.error(error)
    else:
        chat, chat_error = initialize_chat(client)
        if chat_error:
            st.error(chat_error)
        else:
            st.session_state.gemini_client = client
            st.session_state.chat_session = chat
            st.session_state.current_api_key = api_key

# --- Helper function for morphology matching ---
def matches_keyword(prompt, keywords):
    prompt_lower = prompt.lower()
    return any(keyword in prompt_lower for keyword in keywords)

# --- Display chat history ---
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        if msg["type"] == "text":
            st.markdown(msg["content"])
        elif msg["type"] == "image":
            st.image(msg["content"])
        elif msg["type"] == "audio":
            st.audio(msg["content"])
        elif msg["type"] == "video":
            st.video(msg["content"])

# --- Chat Input ---
if prompt := st.chat_input("Введите ваш запрос..."):
    # Add user message to history
    st.session_state.chat_history.append({"role": "user", "type": "text", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # --- Routing ---
    with st.chat_message("assistant"):
        # Image routing
        if matches_keyword(prompt, ['нарисуй', 'фото', 'изображение']):
            st.write("Генерирую изображение...")
            url, error = generate_image(prompt)
            if error:
                st.error(error)
                st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": error})
            elif url:
                st.image(url)
                st.session_state.chat_history.append({"role": "assistant", "type": "image", "content": url})

        # Music routing
        elif matches_keyword(prompt, ['музык', 'песн', 'песен', 'трек']):
            st.write("Генерирую музыку... Это может занять некоторое время.")
            path, error = generate_music(prompt)
            if error:
                st.error(error)
                st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": error})
            elif path:
                st.audio(path)
                st.session_state.chat_history.append({"role": "assistant", "type": "audio", "content": path})

        # Video routing
        elif matches_keyword(prompt, ['видео', 'ролик']):
            st.write("Генерирую видео... Это может занять некоторое время.")
            path, error = generate_video(prompt)
            if error:
                st.error(error)
                st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": error})
            elif path:
                st.video(path)
                st.session_state.chat_history.append({"role": "assistant", "type": "video", "content": path})

        # Text routing (Gemini)
        else:
            if not st.session_state.chat_session:
                error_msg = "Пожалуйста, введите валидный GOOGLE_API_KEY в боковой панели."
                st.error(error_msg)
                st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": error_msg})
            else:
                response_stream, error = send_message_stream(st.session_state.chat_session, prompt)
                if error:
                    st.error(error)
                    st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": error})
                elif response_stream:
                    # Stream the response
                    placeholder = st.empty()
                    full_response = ""
                    try:
                        for chunk in response_stream:
                            if chunk.text:
                                full_response += chunk.text
                                placeholder.markdown(full_response + "▌")
                        placeholder.markdown(full_response)
                        st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": full_response})
                    except Exception as e:
                        st.error(f"Произошла ошибка при потоковой передаче текста: {e}")
                        if full_response:
                            st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": full_response})
