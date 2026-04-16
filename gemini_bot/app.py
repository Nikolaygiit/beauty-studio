import streamlit as st
import os
from modules.text import initialize_chat, generate_text
from modules.image import generate_image_url
from modules.music import get_music_client, generate_music
from modules.video import get_video_client, generate_video

# --- Layout and Configuration ---
st.set_page_config(
    page_title="Gemini Ultimate Bot",
    page_icon="✨",
    layout="wide",
)

st.title("✨ Gemini Ultimate Bot")
st.markdown("Универсальный бот: Текст, Картинки, Музыка и Видео!")

# --- Sidebar Configuration ---
with st.sidebar:
    st.header("Настройки")
    api_key_input = st.text_input("Введите ваш Google Gemini API Key:", type="password")

    if st.button("Очистить историю чата"):
        st.session_state.chat_history = []
        st.session_state.chat_session = None
        st.session_state.gemini_client = None
        st.session_state.current_api_key = None
        st.rerun()

# --- Initialize Session State ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "chat_session" not in st.session_state:
    st.session_state.chat_session = None
if "gemini_client" not in st.session_state:
    st.session_state.gemini_client = None
if "current_api_key" not in st.session_state:
    st.session_state.current_api_key = None

# --- Main Application Logic ---
api_key = api_key_input or os.environ.get("GOOGLE_API_KEY")

if not api_key:
    st.warning("Пожалуйста, введите Google Gemini API Key в боковой панели, чтобы начать.")
else:
    # Initialize or re-initialize chat if API key changes
    if st.session_state.current_api_key != api_key:
        client, chat_session = initialize_chat(api_key)
        if chat_session:
            st.session_state.gemini_client = client
            st.session_state.chat_session = chat_session
            st.session_state.current_api_key = api_key
            st.session_state.chat_history = [] # clear history on new key

    # Display chat history
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            if "image_url" in message:
                st.image(message["image_url"])
                st.markdown(message["content"])
            elif "audio_path" in message:
                st.audio(message["audio_path"])
                st.markdown(message["content"])
            elif "video_path" in message:
                st.video(message["video_path"])
                st.markdown(message["content"])
            else:
                st.markdown(message["content"])

    # Chat Input
    if prompt := st.chat_input("Введите ваш запрос..."):
        # Add user message to history and display
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        prompt_lower = prompt.lower()

        # --- Media Routing Logic ---
        with st.chat_message("assistant"):
            if any(word in prompt_lower for word in ['нарисуй', 'фото', 'изображение']):
                with st.spinner("Генерирую изображение..."):
                    img_url = generate_image_url(prompt)
                    st.image(img_url)
                    response_text = "Вот ваше изображение!"
                    st.markdown(response_text)
                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": response_text,
                        "image_url": img_url
                    })

            elif any(word in prompt_lower for word in ['музыка', 'песня', 'трек']):
                with st.spinner("Генерирую музыку (это может занять время)..."):
                    client = get_music_client()
                    result = generate_music(client, prompt)
                    if isinstance(result, str) and result.startswith("Error"):
                        st.error(result)
                        st.session_state.chat_history.append({"role": "assistant", "content": result})
                    else:
                        # Gradio client returns a tuple for audio (path, etc), we take the path
                        audio_path = result[0] if isinstance(result, tuple) else result
                        st.audio(audio_path)
                        response_text = "Вот ваша музыка!"
                        st.markdown(response_text)
                        st.session_state.chat_history.append({
                            "role": "assistant",
                            "content": response_text,
                            "audio_path": audio_path
                        })

            elif any(word in prompt_lower for word in ['видео', 'ролик']):
                with st.spinner("Генерирую видео (это может занять значительное время)..."):
                    client = get_video_client()
                    result = generate_video(client, prompt)
                    if isinstance(result, str) and result.startswith("Error"):
                        st.error(result)
                        st.session_state.chat_history.append({"role": "assistant", "content": result})
                    else:
                        video_path = result.get('video') if isinstance(result, dict) else result
                        st.video(video_path)
                        response_text = "Вот ваше видео!"
                        st.markdown(response_text)
                        st.session_state.chat_history.append({
                            "role": "assistant",
                            "content": response_text,
                            "video_path": video_path
                        })
            else:
                # Text Generation
                if st.session_state.chat_session:
                    with st.spinner("Думаю..."):
                        response_stream = generate_text(st.session_state.chat_session, prompt)
                        if response_stream:
                            response_placeholder = st.empty()
                            full_response = ""
                            for chunk in response_stream:
                                if chunk.text:
                                    full_response += chunk.text
                                    response_placeholder.markdown(full_response + "▌")
                            response_placeholder.markdown(full_response)
                            st.session_state.chat_history.append({"role": "assistant", "content": full_response})
                        else:
                             st.error("Не удалось получить ответ от Gemini.")
                else:
                    st.error("Чат не инициализирован. Проверьте API ключ.")
