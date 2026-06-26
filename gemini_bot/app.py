import streamlit as st
from modules.routing import get_route
from modules.text import get_gemini_client, start_chat_session
from modules.image import generate_image
from modules.music import get_music_client, generate_music
from modules.video import get_video_client, generate_video

st.set_page_config(page_title="Gemini Ultimate Bot", layout="wide")
st.title("Gemini Ultimate Bot 🤖✨")

# Sidebar
with st.sidebar:
    st.header("Настройки")
    api_key = st.text_input("Введите GOOGLE_API_KEY", type="password")

    if st.button("Очистить историю чата"):
        st.session_state.chat_history = []
        st.session_state.chat_session = None
        st.session_state.gemini_client = None
        st.session_state.current_api_key = None
        st.rerun()

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "chat_session" not in st.session_state:
    st.session_state.chat_session = None
if "gemini_client" not in st.session_state:
    st.session_state.gemini_client = None
if "current_api_key" not in st.session_state:
    st.session_state.current_api_key = None

# Reinitialize Gemini if API key changed
if api_key and api_key != st.session_state.current_api_key:
    client, error = get_gemini_client(api_key)
    if error:
        st.error(error)
    else:
        st.session_state.gemini_client = client
        st.session_state.current_api_key = api_key
        chat, chat_error = start_chat_session(client)
        if chat_error:
            st.error(chat_error)
        else:
            st.session_state.chat_session = chat

# Render chat history
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        if msg["type"] == "text":
            st.markdown(msg["content"])
        elif msg["type"] == "image":
            st.markdown(f"**Запрос:** {msg['content']}")
            st.image(msg["media_path"])
        elif msg["type"] == "music":
            st.markdown(f"**Запрос:** {msg['content']}")
            st.audio(msg["media_path"])
        elif msg["type"] == "video":
            st.markdown(f"**Запрос:** {msg['content']}")
            st.video(msg["media_path"])

# Chat input
if prompt := st.chat_input("Введите сообщение (напр. 'нарисуй кота', 'песня про лето', 'видео океана')"):

    # Check if we have API key for text (though image/music/video might not need it, we enforce it globally for simplicity)
    if not st.session_state.gemini_client:
        st.error("Пожалуйста, введите API ключ в боковой панели.")
        st.stop()

    st.session_state.chat_history.append({"role": "user", "type": "text", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    route = get_route(prompt)

    with st.chat_message("assistant"):
        if route == "image":
            with st.spinner("Генерация изображения..."):
                url, error = generate_image(prompt)
                if error:
                    st.error(error)
                else:
                    st.image(url)
                    st.session_state.chat_history.append({"role": "assistant", "type": "image", "content": prompt, "media_path": url})

        elif route == "music":
            with st.spinner("Инициализация клиента музыки..."):
                client, error = get_music_client()
            if error:
                st.error(error)
            else:
                with st.spinner("Генерация музыки (это может занять некоторое время)..."):
                    path, gen_error = generate_music(prompt, client)
                    if gen_error:
                        st.error(gen_error)
                    else:
                        st.audio(path)
                        st.session_state.chat_history.append({"role": "assistant", "type": "music", "content": prompt, "media_path": path})

        elif route == "video":
            with st.spinner("Инициализация клиента видео..."):
                client, error = get_video_client()
            if error:
                st.error(error)
            else:
                with st.spinner("Генерация видео (это может занять длительное время)..."):
                    path, gen_error = generate_video(prompt, client)
                    if gen_error:
                        st.error(gen_error)
                    else:
                        st.video(path)
                        st.session_state.chat_history.append({"role": "assistant", "type": "video", "content": prompt, "media_path": path})

        else: # text
            if not st.session_state.chat_session:
                st.error("Сессия чата не инициализирована.")
                st.stop()

            try:
                response_stream = st.session_state.chat_session.send_message_stream(prompt)

                # Stream the text output
                message_placeholder = st.empty()
                full_response = ""

                for chunk in response_stream:
                    if chunk.text:
                        full_response += chunk.text
                        message_placeholder.markdown(full_response + "▌")

                message_placeholder.markdown(full_response)
                st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": full_response})
            except Exception as e:
                st.error(f"Ошибка при обращении к Gemini: {str(e)}")
