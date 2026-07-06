import streamlit as st
import traceback

from modules.routing import get_route
from modules.text import get_gemini_client, get_chat_session
from modules.image import generate_image
from modules.music import generate_music
from modules.video import generate_video

# Initialize session states
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "chat_session" not in st.session_state:
    st.session_state.chat_session = None
if "gemini_client" not in st.session_state:
    st.session_state.gemini_client = None
if "current_api_key" not in st.session_state:
    st.session_state.current_api_key = ""

st.set_page_config(page_title="Gemini Ultimate Bot", page_icon="✨", layout="centered")

st.title("✨ Gemini Ultimate Bot")

# Sidebar for API Key and options
with st.sidebar:
    st.header("Настройки")
    api_key = st.text_input("Введите GOOGLE_API_KEY", type="password", value=st.session_state.current_api_key)

    if st.button("Очистить историю чата"):
        st.session_state.chat_history = []
        st.session_state.chat_session = None
        st.session_state.gemini_client = None
        st.success("История очищена!")
        st.rerun()

# Handle API Key change
if api_key != st.session_state.current_api_key:
    st.session_state.current_api_key = api_key
    if api_key:
        client, error = get_gemini_client(api_key)
        if error:
            st.sidebar.error(error)
            st.session_state.gemini_client = None
            st.session_state.chat_session = None
        else:
            st.session_state.gemini_client = client
            st.session_state.chat_session = get_chat_session(client)
            st.sidebar.success("Успешно подключено!")
    else:
        st.session_state.gemini_client = None
        st.session_state.chat_session = None

if not st.session_state.current_api_key:
    st.warning("Пожалуйста, введите GOOGLE_API_KEY в боковом меню для начала работы.")
    st.stop()

# Display chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message.get("type") == "image" and message.get("media_path"):
            st.image(message["media_path"])
        elif message.get("type") == "music" and message.get("media_path"):
            st.audio(message["media_path"])
        elif message.get("type") == "video" and message.get("media_path"):
            st.video(message["media_path"])

# Chat input
if prompt := st.chat_input("Введите сообщение (например: нарисуй кота, музыка для сна, видео с природой)"):
    # Append user message
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Route request
    route = get_route(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()

        try:
            if route == "image":
                message_placeholder.markdown("Генерирую изображение...")
                media_path, error = generate_image(prompt)

                if error:
                    st.error(error)
                    st.session_state.chat_history.append({"role": "assistant", "content": error, "type": "error"})
                elif media_path:
                    st.image(media_path)
                    st.session_state.chat_history.append({"role": "assistant", "content": "Вот ваше изображение!", "type": "image", "media_path": media_path})

            elif route == "music":
                message_placeholder.markdown("Генерирую музыку... (это может занять время)")
                media_path, error = generate_music(prompt)

                if error:
                    st.error(error)
                    st.session_state.chat_history.append({"role": "assistant", "content": error, "type": "error"})
                elif media_path:
                    st.audio(media_path)
                    st.session_state.chat_history.append({"role": "assistant", "content": "Вот ваша музыка!", "type": "music", "media_path": media_path})

            elif route == "video":
                message_placeholder.markdown("Генерирую видео... (это может занять продолжительное время)")
                media_path, error = generate_video(prompt)

                if error:
                    st.error(error)
                    st.session_state.chat_history.append({"role": "assistant", "content": error, "type": "error"})
                elif media_path:
                    st.video(media_path)
                    st.session_state.chat_history.append({"role": "assistant", "content": "Вот ваше видео!", "type": "video", "media_path": media_path})

            elif route == "text":
                if st.session_state.chat_session:
                    full_response = ""
                    try:
                        response_stream = st.session_state.chat_session.send_message_stream(prompt)
                        for chunk in response_stream:
                            if chunk.text:
                                full_response += chunk.text
                                message_placeholder.markdown(full_response + "▌")
                        message_placeholder.markdown(full_response)
                        st.session_state.chat_history.append({"role": "assistant", "content": full_response, "type": "text"})
                    except Exception as e:
                        error_msg = f"Ошибка генерации текста: {e}"
                        st.error(error_msg)
                        st.session_state.chat_history.append({"role": "assistant", "content": error_msg, "type": "error"})
                else:
                     st.error("Сессия чата не инициализирована.")

        except Exception as e:
             error_msg = f"Внутренняя ошибка: {traceback.format_exc()}"
             st.error(error_msg)
             st.session_state.chat_history.append({"role": "assistant", "content": error_msg, "type": "error"})
