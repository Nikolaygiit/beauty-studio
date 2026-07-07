import streamlit as st
from modules.routing import get_route
from modules.text import get_gemini_client, create_chat_session
from modules.image import generate_image
from modules.music import generate_music
from modules.video import generate_video

# Streamlit App Configuration
st.set_page_config(page_title="Gemini Ultimate Bot", page_icon="🤖", layout="wide")
st.title("🤖 Gemini Ultimate Bot")

# Sidebar for configuration
with st.sidebar:
    st.header("Настройки")
    api_key = st.text_input("Введите GOOGLE_API_KEY", type="password")

    if st.button("Очистить историю чата", key="clear_chat"):
        st.session_state.chat_history = []
        st.session_state.chat_session = None
        st.session_state.gemini_client = None
        st.session_state.current_api_key = None
        st.rerun()

# Initialize Session State
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "chat_session" not in st.session_state:
    st.session_state.chat_session = None
if "gemini_client" not in st.session_state:
    st.session_state.gemini_client = None
if "current_api_key" not in st.session_state:
    st.session_state.current_api_key = None

# Handle API Key change
if api_key and api_key != st.session_state.current_api_key:
    client, error = get_gemini_client(api_key)
    if error:
        st.sidebar.error(error)
    else:
        chat_session, error = create_chat_session(client)
        if error:
            st.sidebar.error(error)
        else:
            st.session_state.gemini_client = client
            st.session_state.chat_session = chat_session
            st.session_state.current_api_key = api_key
            st.sidebar.success("API Ключ успешно подключен!")

# Render chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        if message["type"] == "text":
            st.markdown(message["content"])
        elif message["type"] == "image":
            st.markdown(message["content"])
            if message.get("media_path"):
                st.image(message["media_path"])
        elif message["type"] == "music":
            st.markdown(message["content"])
            if message.get("media_path"):
                st.audio(message["media_path"])
        elif message["type"] == "video":
            st.markdown(message["content"])
            if message.get("media_path"):
                st.video(message["media_path"])

# Chat input
if prompt := st.chat_input("Введите ваш запрос..."):
    # Add user message to state and display
    st.session_state.chat_history.append({"role": "user", "type": "text", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Determine intent
    route = get_route(prompt)

    # Handle based on route
    with st.chat_message("assistant"):
        if route == "text":
            if not st.session_state.chat_session:
                st.error("Пожалуйста, введите валидный API ключ в боковом меню.")
            else:
                message_placeholder = st.empty()
                full_response = ""
                try:
                    # Use streaming
                    response = st.session_state.chat_session.send_message_stream(prompt)
                    for chunk in response:
                        if chunk.text:
                            full_response += chunk.text
                            message_placeholder.markdown(full_response + "▌")
                    message_placeholder.markdown(full_response)
                    st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": full_response})
                except Exception as e:
                    st.error(f"Ошибка при обращении к Gemini API: {str(e)}")

        elif route == "image":
            st.markdown(f"Генерирую изображение по запросу: {prompt}...")
            url, error = generate_image(prompt)
            if error:
                st.error(error)
                st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": error})
            else:
                st.image(url)
                st.session_state.chat_history.append({"role": "assistant", "type": "image", "content": "Вот ваше изображение:", "media_path": url})

        elif route == "music":
            st.markdown(f"Генерирую музыку по запросу: {prompt}...")
            with st.spinner("Создаем шедевр (это может занять время)..."):
                media_path, error = generate_music(prompt)
            if error:
                st.error(error)
                st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": error})
            else:
                st.audio(media_path)
                st.session_state.chat_history.append({"role": "assistant", "type": "music", "content": "Вот ваша музыка:", "media_path": media_path})

        elif route == "video":
            st.markdown(f"Генерирую видео по запросу: {prompt}...")
            with st.spinner("Создаем видеоряд (пожалуйста, подождите)..."):
                media_path, error = generate_video(prompt)
            if error:
                st.error(error)
                st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": error})
            else:
                st.video(media_path)
                st.session_state.chat_history.append({"role": "assistant", "type": "video", "content": "Вот ваше видео:", "media_path": media_path})
