import streamlit as st
from modules.routing import get_route
from modules.text import get_gemini_client, initialize_chat, generate_text_stream
from modules.image import generate_image
from modules.music import generate_music
from modules.video import generate_video

# Streamlit Page Config
st.set_page_config(
    page_title="Gemini Ultimate Bot",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Gemini Ultimate Bot")
st.markdown("Умный ассистент с генерацией текста, изображений, музыки и видео.")

# --- Sidebar ---
st.sidebar.title("Настройки")
api_key = st.sidebar.text_input("Введите Google Gemini API Key", type="password")

if st.sidebar.button("Очистить историю чата"):
    st.session_state.chat_history = []
    st.session_state.gemini_client = None
    st.session_state.chat_session = None
    st.rerun()

# --- Session State Initialization ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "current_api_key" not in st.session_state:
    st.session_state.current_api_key = ""

# Handle API Key changes to re-init client
if api_key != st.session_state.current_api_key:
    st.session_state.current_api_key = api_key
    st.session_state.gemini_client = None
    st.session_state.chat_session = None

if api_key and st.session_state.get("gemini_client") is None:
    client, error = get_gemini_client(api_key)
    if error:
        st.error(error)
    else:
        st.session_state.gemini_client = client
        st.session_state.chat_session = initialize_chat(client)

# --- Render Chat History ---
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message.get("type") == "image" and message.get("media_path"):
            st.image(message["media_path"])
        elif message.get("type") == "music" and message.get("media_path"):
            st.audio(message["media_path"])
        elif message.get("type") == "video" and message.get("media_path"):
            st.video(message["media_path"])

# --- Chat Input & Processing ---
if prompt := st.chat_input("Напишите сообщение (напр. 'нарисуй кота', 'сочини музыку', 'сделай видео')"):
    if not api_key:
        st.error("Пожалуйста, введите API ключ в боковой панели.")
        st.stop()

    if not st.session_state.chat_session:
        st.error("Чат не инициализирован. Проверьте API ключ.")
        st.stop()

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Route generation based on prompt
    route = get_route(prompt)

    with st.chat_message("assistant"):
        if route == "image":
            with st.spinner("Генерирую изображение..."):
                st.markdown(f"*Генерирую изображение по запросу: {prompt}*")
                image_url, error = generate_image(prompt)
                if error:
                    st.error(error)
                    st.session_state.chat_history.append({"role": "user", "content": prompt})
                    st.session_state.chat_history.append({"role": "assistant", "content": f"Ошибка: {error}", "type": "text"})
                else:
                    st.image(image_url)
                    st.session_state.chat_history.append({"role": "user", "content": prompt})
                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": f"Вот ваше изображение по запросу: {prompt}",
                        "type": "image",
                        "media_path": image_url
                    })

        elif route == "music":
            with st.spinner("Генерирую музыку..."):
                st.markdown(f"*Генерирую музыку по запросу: {prompt}*")
                audio_path, error = generate_music(prompt)
                if error:
                    st.error(error)
                    st.session_state.chat_history.append({"role": "user", "content": prompt})
                    st.session_state.chat_history.append({"role": "assistant", "content": f"Ошибка: {error}", "type": "text"})
                else:
                    st.audio(audio_path)
                    st.session_state.chat_history.append({"role": "user", "content": prompt})
                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": f"Вот ваша музыка по запросу: {prompt}",
                        "type": "music",
                        "media_path": audio_path
                    })

        elif route == "video":
            with st.spinner("Генерирую видео..."):
                st.markdown(f"*Генерирую видео по запросу: {prompt}*")
                video_path, error = generate_video(prompt)
                if error:
                    st.error(error)
                    st.session_state.chat_history.append({"role": "user", "content": prompt})
                    st.session_state.chat_history.append({"role": "assistant", "content": f"Ошибка: {error}", "type": "text"})
                else:
                    st.video(video_path)
                    st.session_state.chat_history.append({"role": "user", "content": prompt})
                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": f"Вот ваше видео по запросу: {prompt}",
                        "type": "video",
                        "media_path": video_path
                    })

        else: # text route
            response_placeholder = st.empty()
            full_response = ""
            for chunk_text in generate_text_stream(st.session_state.chat_session, prompt):
                full_response += chunk_text
                response_placeholder.markdown(full_response + "▌")

            response_placeholder.markdown(full_response)

            st.session_state.chat_history.append({"role": "user", "content": prompt})
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": full_response,
                "type": "text"
            })
