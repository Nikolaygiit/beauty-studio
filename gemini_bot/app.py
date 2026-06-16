import streamlit as st
from modules.routing import get_route
from modules.image import generate_image
from modules.music import generate_music
from modules.video import generate_video
from modules.text import get_gemini_client, init_chat_session, generate_text_stream

st.set_page_config(page_title="Gemini Ultimate Bot", page_icon="✨", layout="wide")
st.title("✨ Gemini Ultimate Bot")
st.markdown("Генерация текста, изображений, музыки и видео!")

# Sidebar for config and reset
with st.sidebar:
    st.header("Настройки")
    api_key = st.text_input("Введите GOOGLE_API_KEY", type="password")
    if st.button("Очистить историю чата"):
        for key in ['chat_history', 'chat_session', 'gemini_client', 'current_api_key']:
            if key in st.session_state:
                del st.session_state[key]
        st.success("История очищена!")
        st.rerun()

# Initialization of State
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "current_api_key" not in st.session_state or st.session_state.current_api_key != api_key:
    if api_key:
        st.session_state.current_api_key = api_key
        client = get_gemini_client(api_key)
        if isinstance(client, str):
            st.error(f"Ошибка инициализации Gemini: {client}")
        else:
            st.session_state.gemini_client = client
            session = init_chat_session(client)
            if isinstance(session, str):
                st.error(f"Ошибка создания сессии: {session}")
            else:
                st.session_state.chat_session = session

# Display Chat History
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        if message["type"] == "text":
            st.markdown(message["content"])
        elif message["type"] == "image":
            st.image(message["content"])
            st.markdown(f"**URL:** {message['content']}")
        elif message["type"] == "music":
            st.audio(message["content"])
        elif message["type"] == "video":
            st.video(message["content"])

# User Input
if prompt := st.chat_input("Введите ваш запрос..."):
    if not api_key:
        st.error("Пожалуйста, введите GOOGLE_API_KEY в боковой панели.")
    else:
        st.session_state.chat_history.append({"role": "user", "type": "text", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        route = get_route(prompt)

        with st.chat_message("assistant"):
            if route == "image":
                with st.spinner("Создаю изображение..."):
                    img_url, err = generate_image(prompt)
                    if err:
                        st.error(err)
                    else:
                        st.image(img_url)
                        st.session_state.chat_history.append({"role": "assistant", "type": "image", "content": img_url})

            elif route == "music":
                with st.spinner("Создаю музыку (это может занять время)..."):
                    audio_path, err = generate_music(prompt)
                    if err:
                        st.error(err)
                    elif audio_path:
                        st.audio(audio_path)
                        st.session_state.chat_history.append({"role": "assistant", "type": "music", "content": audio_path})

            elif route == "video":
                with st.spinner("Создаю видео (это может занять несколько минут)..."):
                    video_path, err = generate_video(prompt)
                    if err:
                        st.error(err)
                    elif video_path:
                        st.video(video_path)
                        st.session_state.chat_history.append({"role": "assistant", "type": "video", "content": video_path})

            else:  # Text route
                if "chat_session" in st.session_state:
                    message_placeholder = st.empty()
                    full_response = ""
                    for chunk in generate_text_stream(st.session_state.chat_session, prompt):
                        full_response += chunk
                        message_placeholder.markdown(full_response + "▌")
                    message_placeholder.markdown(full_response)
                    st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": full_response})
                else:
                    st.error("Сессия чата не инициализирована. Проверьте API ключ.")
