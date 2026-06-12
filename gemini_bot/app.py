import streamlit as st

from modules.routing import get_route
from modules.text import create_client, create_chat_session, generate_text_stream
from modules.image import generate_image
from modules.music import generate_music
from modules.video import generate_video

# --- UI Setup ---
st.set_page_config(page_title="Gemini Ultimate Bot", page_icon="🤖")
st.title("Gemini Ultimate Bot 🤖")

# --- Sidebar / Settings ---
with st.sidebar:
    st.header("Настройки")
    api_key = st.text_input("Введите GOOGLE_API_KEY", type="password")

    if st.button("Очистить историю чата"):
        st.session_state.chat_history = []
        st.session_state.chat_session = None
        st.session_state.gemini_client = None
        st.session_state.current_api_key = None
        st.rerun()

# --- State Initialization ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "chat_session" not in st.session_state:
    st.session_state.chat_session = None
if "gemini_client" not in st.session_state:
    st.session_state.gemini_client = None
if "current_api_key" not in st.session_state:
    st.session_state.current_api_key = None

# Detect API Key changes to recreate client and session
if api_key and api_key != st.session_state.current_api_key:
    st.session_state.current_api_key = api_key
    try:
        st.session_state.gemini_client = create_client(api_key)
        st.session_state.chat_session = create_chat_session(st.session_state.gemini_client)
    except Exception as e:
        st.sidebar.error(f"Ошибка инициализации API: {str(e)}")
        st.session_state.chat_session = None

# --- Main App ---
if not st.session_state.current_api_key:
    st.warning("Пожалуйста, введите GOOGLE_API_KEY в боковой панели.")
    st.stop()

# --- Render Chat History ---
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        msg_type = message.get("type", "text")
        content = message["content"]

        if msg_type == "text":
            st.markdown(content)
        elif msg_type == "image":
            st.image(content)
        elif msg_type == "audio":
            st.audio(content)
        elif msg_type == "video":
            st.video(content)
        elif msg_type == "error":
            st.error(content)

# --- Handle User Input ---
if prompt := st.chat_input("Введите ваш запрос..."):
    # Append user prompt to history
    st.session_state.chat_history.append({"role": "user", "type": "text", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    # Route request
    route = get_route(prompt)

    with st.chat_message("assistant"):
        if route == "image":
            with st.spinner("Генерация изображения..."):
                url, err = generate_image(prompt)
                if err:
                    st.error(err)
                    st.session_state.chat_history.append({"role": "assistant", "type": "error", "content": err})
                else:
                    st.image(url)
                    st.session_state.chat_history.append({"role": "assistant", "type": "image", "content": url})

        elif route == "music":
            with st.spinner("Генерация музыки (это может занять некоторое время)..."):
                path, err = generate_music(prompt)
                if err:
                    st.error(err)
                    st.session_state.chat_history.append({"role": "assistant", "type": "error", "content": err})
                else:
                    st.audio(path)
                    st.session_state.chat_history.append({"role": "assistant", "type": "audio", "content": path})

        elif route == "video":
            with st.spinner("Генерация видео (это может занять несколько минут)..."):
                path, err = generate_video(prompt)
                if err:
                    st.error(err)
                    st.session_state.chat_history.append({"role": "assistant", "type": "error", "content": err})
                else:
                    st.video(path)
                    st.session_state.chat_history.append({"role": "assistant", "type": "video", "content": path})

        else: # route == "text"
            if st.session_state.chat_session is None:
                err_msg = "Сессия чата не инициализирована. Проверьте API ключ."
                st.error(err_msg)
                st.session_state.chat_history.append({"role": "assistant", "type": "error", "content": err_msg})
            else:
                message_placeholder = st.empty()
                full_response = ""

                # Streaming response
                for chunk in generate_text_stream(st.session_state.chat_session, prompt):
                    full_response += chunk
                    message_placeholder.markdown(full_response + "▌")

                message_placeholder.markdown(full_response)
                st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": full_response})
