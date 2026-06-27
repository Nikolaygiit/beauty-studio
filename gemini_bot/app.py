import streamlit as st
from google.genai import types

from modules.text import get_gemini_client
from modules.image import generate_image
from modules.music import generate_music
from modules.video import generate_video
from modules.routing import get_route

st.set_page_config(page_title="Gemini Ultimate Bot", page_icon="✨", layout="wide")

st.title("✨ Gemini Ultimate Bot")
st.markdown("Генерация изображений, музыки, текста и видео с помощью ИИ!")

# Sidebar for configuration
with st.sidebar:
    st.header("Настройки")
    api_key = st.text_input("Введите GOOGLE_API_KEY", type="password")

    if st.button("Очистить историю чата", key="clear_chat"):
        st.session_state.chat_history = []
        st.session_state.chat_session = None
        st.session_state.gemini_client = None
        # current_api_key might remain the same, but we reset the session

# Initialize session state variables
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "chat_session" not in st.session_state:
    st.session_state.chat_session = None
if "gemini_client" not in st.session_state:
    st.session_state.gemini_client = None
if "current_api_key" not in st.session_state:
    st.session_state.current_api_key = None

# Re-initialize Gemini client if API key changes or if it's missing
if api_key and (api_key != st.session_state.current_api_key or st.session_state.chat_session is None):
    st.session_state.current_api_key = api_key
    client, error = get_gemini_client(api_key)

    if error:
        st.sidebar.error(error)
        st.session_state.gemini_client = None
        st.session_state.chat_session = None
    else:
        st.session_state.gemini_client = client
        config = types.GenerateContentConfig(
            system_instruction="Ты — дружелюбный и полезный ассистент. Всегда отвечай на русском языке.",
        )
        st.session_state.chat_session = client.chats.create(model="gemini-2.0-flash", config=config)
        st.sidebar.success("Gemini API успешно подключен!")

# Display chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        if "text" in message:
            st.markdown(message["text"])

        # Display media if present
        msg_type = message.get("type", "text")
        media_path = message.get("media_path")

        if media_path:
            if msg_type == "image":
                st.image(media_path)
            elif msg_type == "music":
                st.audio(media_path)
            elif msg_type == "video":
                st.video(media_path)

# Handle user input
if prompt := st.chat_input("Напишите сообщение..."):
    # Add user message to history
    st.session_state.chat_history.append({"role": "user", "text": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Determine route
    route = get_route(prompt)

    with st.chat_message("assistant"):
        if route == "image":
            with st.spinner("Генерация изображения..."):
                media_path, error = generate_image(prompt)
                if error:
                    st.error(error)
                    st.session_state.chat_history.append({"role": "assistant", "text": error, "type": "text"})
                else:
                    st.image(media_path)
                    st.session_state.chat_history.append({"role": "assistant", "type": "image", "media_path": media_path, "text": f"Вот ваше изображение по запросу: {prompt}"})

        elif route == "music":
            with st.spinner("Генерация музыки... Это может занять некоторое время."):
                media_path, error = generate_music(prompt)
                if error:
                    st.error(error)
                    st.session_state.chat_history.append({"role": "assistant", "text": error, "type": "text"})
                else:
                    st.audio(media_path)
                    st.session_state.chat_history.append({"role": "assistant", "type": "music", "media_path": media_path, "text": f"Вот ваша музыка по запросу: {prompt}"})

        elif route == "video":
            with st.spinner("Генерация видео... Это может занять несколько минут."):
                media_path, error = generate_video(prompt)
                if error:
                    st.error(error)
                    st.session_state.chat_history.append({"role": "assistant", "text": error, "type": "text"})
                else:
                    st.video(media_path)
                    st.session_state.chat_history.append({"role": "assistant", "type": "video", "media_path": media_path, "text": f"Вот ваше видео по запросу: {prompt}"})

        elif route == "text":
            if not st.session_state.chat_session:
                st.error("Пожалуйста, введите корректный GOOGLE_API_KEY в настройках.")
            else:
                try:
                    response_placeholder = st.empty()
                    full_response = ""

                    # Streaming response
                    response_stream = st.session_state.chat_session.send_message_stream(prompt)
                    for chunk in response_stream:
                        if chunk.text:
                            full_response += chunk.text
                            response_placeholder.markdown(full_response + "▌")

                    response_placeholder.markdown(full_response)
                    st.session_state.chat_history.append({"role": "assistant", "text": full_response, "type": "text"})

                except Exception as e:
                    st.error(f"Ошибка при общении с Gemini: {str(e)}")
                    st.session_state.chat_history.append({"role": "assistant", "text": f"Ошибка: {str(e)}", "type": "text"})
