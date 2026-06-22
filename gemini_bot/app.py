import streamlit as st
from modules import routing, text, image, music, video

st.set_page_config(page_title="Gemini Ultimate Bot", layout="wide")

st.title("Gemini Ultimate Bot")
st.markdown("Генерация текста, изображений, музыки и видео!")

# Sidebar configuration
st.sidebar.title("Настройки")
api_key = st.sidebar.text_input("Введите GOOGLE_API_KEY", type="password")

def clear_chat():
    st.session_state.chat_history = []
    st.session_state.chat_session = None
    st.session_state.gemini_client = None

if st.sidebar.button("Clear Chat History"):
    clear_chat()
    st.sidebar.success("История чата очищена")

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "chat_session" not in st.session_state:
    st.session_state.chat_session = None
if "gemini_client" not in st.session_state:
    st.session_state.gemini_client = None
if "current_api_key" not in st.session_state:
    st.session_state.current_api_key = ""

# Handle API Key changes
if api_key != st.session_state.current_api_key:
    st.session_state.current_api_key = api_key
    clear_chat()

if st.session_state.current_api_key and st.session_state.gemini_client is None:
    st.session_state.gemini_client, error = text.get_gemini_client(st.session_state.current_api_key)
    if st.session_state.gemini_client:
        st.session_state.chat_session = text.create_chat_session(st.session_state.gemini_client)
    else:
        st.error(f"Ошибка инициализации Gemini: {error}")

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
if prompt := st.chat_input("Введите ваш запрос..."):
    # Append user message
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Route the prompt
    route = routing.route_prompt(prompt)

    with st.chat_message("assistant"):
        if route == "image":
            with st.spinner("Генерация изображения..."):
                url, error = image.generate_image(prompt)
                if error:
                    st.error(error)
                    st.session_state.chat_history.append({"role": "assistant", "content": error})
                else:
                    st.image(url)
                    msg = f"Вот ваше изображение: {url}"
                    st.session_state.chat_history.append({"role": "assistant", "content": msg, "type": "image", "media_path": url})

        elif route == "music":
            with st.spinner("Генерация музыки (это может занять время)..."):
                path, error = music.generate_music(prompt)
                if error:
                    st.error(error)
                    st.session_state.chat_history.append({"role": "assistant", "content": error})
                else:
                    st.audio(path)
                    msg = "Музыка сгенерирована."
                    st.session_state.chat_history.append({"role": "assistant", "content": msg, "type": "music", "media_path": path})

        elif route == "video":
            with st.spinner("Генерация видео (это может занять время)..."):
                path, error = video.generate_video(prompt)
                if error:
                    st.error(error)
                    st.session_state.chat_history.append({"role": "assistant", "content": error})
                else:
                    st.video(path)
                    msg = "Видео сгенерировано."
                    st.session_state.chat_history.append({"role": "assistant", "content": msg, "type": "video", "media_path": path})

        else: # Text route
            if not st.session_state.chat_session:
                msg = "Пожалуйста, введите валидный GOOGLE_API_KEY в настройках для текстового чата."
                st.error(msg)
                st.session_state.chat_history.append({"role": "assistant", "content": msg})
            else:
                try:
                    response_placeholder = st.empty()
                    full_response = ""
                    # Stream response
                    response_stream = st.session_state.chat_session.send_message_stream(prompt)
                    for chunk in response_stream:
                        if chunk.text:
                            full_response += chunk.text
                            response_placeholder.markdown(full_response + "▌")
                    response_placeholder.markdown(full_response)
                    st.session_state.chat_history.append({"role": "assistant", "content": full_response})
                except Exception as e:
                    error_msg = f"Ошибка генерации текста: {str(e)}"
                    st.error(error_msg)
                    st.session_state.chat_history.append({"role": "assistant", "content": error_msg})
