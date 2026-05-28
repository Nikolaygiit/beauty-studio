import streamlit as st
from modules.text import init_gemini_client, start_chat_session, generate_text_stream
from modules.image import generate_image
from modules.music import generate_music
from modules.video import generate_video
from modules.routing import get_routing

st.set_page_config(page_title="Gemini Ultimate Bot", page_icon="🤖")

# Initialize session state variables if they don't exist
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "chat_session" not in st.session_state:
    st.session_state.chat_session = None
if "gemini_client" not in st.session_state:
    st.session_state.gemini_client = None
if "current_api_key" not in st.session_state:
    st.session_state.current_api_key = ""

st.title("🤖 Gemini Ultimate Bot")

# Sidebar for configuration and clear chat functionality
with st.sidebar:
    st.header("Настройки")
    api_key_input = st.text_input("Введите GOOGLE_API_KEY", type="password", value=st.session_state.current_api_key)

    if st.button("Очистить историю чата"):
        st.session_state.chat_history = []
        st.session_state.chat_session = None
        st.session_state.gemini_client = None
        # We don't clear current_api_key so the user doesn't have to re-enter it constantly
        st.rerun()

# Update client if API key changes
if api_key_input and api_key_input != st.session_state.current_api_key:
    st.session_state.current_api_key = api_key_input
    client, error = init_gemini_client(api_key_input)
    if error:
        st.sidebar.error(error)
        st.session_state.gemini_client = None
        st.session_state.chat_session = None
    else:
        st.session_state.gemini_client = client
        st.session_state.chat_session, err = start_chat_session(client)
        if err:
            st.sidebar.error(err)
            st.session_state.chat_session = None

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
        elif message["type"] == "error":
            st.error(message["content"])

# Handle user input
prompt = st.chat_input("Введите ваш запрос...")

if prompt:
    # Add user message to history and display it
    st.session_state.chat_history.append({"role": "user", "type": "text", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    route = get_routing(prompt)
    with st.chat_message("assistant"):
        # Image routing
        if route == "image":
            with st.spinner("Генерация изображения..."):
                media_url, error = generate_image(prompt)
                if error:
                    st.error(error)
                    st.session_state.chat_history.append({"role": "assistant", "type": "error", "content": error})
                else:
                    st.image(media_url)
                    st.session_state.chat_history.append({"role": "assistant", "type": "image", "content": media_url})

        # Music routing
        elif route == "music":
            with st.spinner("Генерация музыки..."):
                media_path, error = generate_music(prompt)
                if error:
                    st.error(error)
                    st.session_state.chat_history.append({"role": "assistant", "type": "error", "content": error})
                else:
                    st.audio(media_path)
                    st.session_state.chat_history.append({"role": "assistant", "type": "audio", "content": media_path})

        # Video routing
        elif route == "video":
            with st.spinner("Генерация видео..."):
                media_path, error = generate_video(prompt)
                if error:
                    st.error(error)
                    st.session_state.chat_history.append({"role": "assistant", "type": "error", "content": error})
                else:
                    st.video(media_path)
                    st.session_state.chat_history.append({"role": "assistant", "type": "video", "content": media_path})

        # Text routing (default)
        else:
            if not st.session_state.chat_session:
                 error_msg = "Пожалуйста, введите валидный GOOGLE_API_KEY в настройках."
                 st.error(error_msg)
                 st.session_state.chat_history.append({"role": "assistant", "type": "error", "content": error_msg})
            else:
                 with st.spinner("Генерация ответа..."):
                     response_container = st.empty()
                     full_response = ""
                     # generate_text_stream yields strings
                     for chunk in generate_text_stream(st.session_state.chat_session, prompt):
                         full_response += chunk
                         response_container.markdown(full_response + "▌")
                     response_container.markdown(full_response)
                     st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": full_response})
