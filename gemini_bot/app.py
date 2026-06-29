import streamlit as st
import os

# Import modules
from modules.routing import route_prompt
from modules.text import get_gemini_client
from modules.image import generate_image
from modules.music import generate_music
from modules.video import generate_video

# Streamlit App Configuration
st.set_page_config(page_title="Gemini Ultimate Bot", page_icon="🤖", layout="centered")

# Sidebar settings
st.sidebar.title("Настройки")
api_key = st.sidebar.text_input("Введите GOOGLE_API_KEY", type="password")

if st.sidebar.button("Очистить историю чата"):
    # Clear Chat History by resetting session state keys
    for key in ['chat_history', 'chat_session', 'gemini_client', 'current_api_key']:
        if key in st.session_state:
            del st.session_state[key]
    st.rerun()

st.title("🤖 Gemini Ultimate Bot")
st.markdown("Генерация текста, изображений, музыки и видео!")

# Initialize session state variables if they don't exist
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'current_api_key' not in st.session_state:
    st.session_state.current_api_key = ""

# Handle Gemini Client re-initialization if API key changes
if api_key and (api_key != st.session_state.current_api_key or 'chat_session' not in st.session_state):
    chat, error = get_gemini_client(api_key)
    if not chat:
        st.error(error)
    else:
        st.session_state.chat_session = chat
        # Core client can also be saved if needed, but chat_session is primarily used for generating content
        st.session_state.current_api_key = api_key
        st.success("API ключ успешно применен!")

# Display Chat History
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

        # Multimodal rendering
        msg_type = message.get("type", "text")
        media_path = message.get("media_path")

        if msg_type == "image" and media_path:
            st.image(media_path)
        elif msg_type == "music" and media_path:
            st.audio(media_path)
        elif msg_type == "video" and media_path:
            st.video(media_path)

# Handle user input
prompt = st.chat_input("Введите ваш запрос...")

if prompt:
    # Append user prompt to chat history and display
    st.session_state.chat_history.append({"role": "user", "content": prompt, "type": "text"})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Route intent based on Russian keywords
    intent = route_prompt(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        media_result = None
        msg_type = "text"

        try:
            if intent == "text":
                if 'chat_session' not in st.session_state:
                    st.error("Пожалуйста, введите GOOGLE_API_KEY в настройках.")
                else:
                    # Stream text response from Gemini
                    chat = st.session_state.chat_session
                    response_stream = chat.send_message_stream(prompt)
                    for chunk in response_stream:
                        if chunk.text:
                            full_response += chunk.text
                            message_placeholder.markdown(full_response + "▌")
                    message_placeholder.markdown(full_response)

            elif intent == "image":
                message_placeholder.markdown("Рисую изображение, подождите...")
                url, error = generate_image(prompt)
                if not url:
                    st.error(error)
                else:
                    full_response = f"Вот ваше изображение по запросу: {prompt}"
                    message_placeholder.markdown(full_response)
                    st.image(url)
                    media_result = url
                    msg_type = "image"

            elif intent == "music":
                message_placeholder.markdown("Генерирую музыку, это может занять минуту...")
                path, error = generate_music(prompt)
                if not path:
                    st.error(error)
                else:
                    full_response = f"Вот ваша музыка по запросу: {prompt}"
                    message_placeholder.markdown(full_response)
                    st.audio(path)
                    media_result = path
                    msg_type = "music"

            elif intent == "video":
                message_placeholder.markdown("Генерирую видео, это может занять пару минут...")
                path, error = generate_video(prompt)
                if not path:
                    st.error(error)
                else:
                    full_response = f"Вот ваше видео по запросу: {prompt}"
                    message_placeholder.markdown(full_response)
                    st.video(path)
                    media_result = path
                    msg_type = "video"

            # Save assistant response to history
            if full_response or media_result:
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": full_response,
                    "type": msg_type,
                    "media_path": media_result
                })

        except Exception as e:
            st.error(f"Произошла ошибка: {str(e)}")
