import streamlit as st
from modules.text import init_gemini_client, init_chat_session, generate_text
from modules.image import generate_image
from modules.music import generate_music
from modules.video import generate_video

# --- UI Setup ---
st.set_page_config(page_title="Gemini Ultimate Bot", page_icon="🤖", layout="wide")
st.title("Gemini Ultimate Bot 🤖")
st.markdown("Создание изображений, музыки, текста и видео с помощью Gemini и других ИИ моделей.")

# --- Session State Initialization ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "gemini_client" not in st.session_state:
    st.session_state.gemini_client = None
if "chat_session" not in st.session_state:
    st.session_state.chat_session = None
if "current_api_key" not in st.session_state:
    st.session_state.current_api_key = ""

# --- Sidebar ---
with st.sidebar:
    st.header("Настройки")
    api_key = st.text_input("Введите ваш Google Gemini API Key:", type="password", value=st.session_state.current_api_key)

    # Handle API Key changes
    if api_key != st.session_state.current_api_key:
        st.session_state.current_api_key = api_key
        st.session_state.gemini_client = init_gemini_client(api_key)
        st.session_state.chat_session = init_chat_session(st.session_state.gemini_client)

    st.markdown("---")
    if st.button("Очистить историю чата"):
        st.session_state.chat_history = []
        st.session_state.chat_session = init_chat_session(st.session_state.gemini_client)
        st.rerun()

    st.markdown("---")
    st.markdown("### Подсказки по ключевым словам:")
    st.markdown("- **Фото/Изображение**: 'нарисуй', 'фото', 'изображение'")
    st.markdown("- **Музыка**: 'музыка', 'песня', 'трек'")
    st.markdown("- **Видео**: 'видео', 'ролик'")

# --- Display Chat History ---
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        if msg["type"] == "text":
            st.markdown(msg["content"])
        elif msg["type"] == "image":
            st.image(msg["content"])
        elif msg["type"] == "music":
            st.audio(msg["content"])
        elif msg["type"] == "video":
            st.video(msg["content"])
        elif msg["type"] == "error":
            st.error(msg["content"])

# --- Main Chat Logic ---
if prompt := st.chat_input("Введите ваш запрос..."):
    # Add user message to history
    st.session_state.chat_history.append({"role": "user", "type": "text", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    prompt_lower = prompt.lower()

    with st.chat_message("assistant"):
        # Image Generation
        if any(keyword in prompt_lower for keyword in ['нарисуй', 'фото', 'изображение']):
            with st.spinner("Генерация изображения..."):
                url, error = generate_image(prompt)
                if error:
                    st.error(error)
                    st.session_state.chat_history.append({"role": "assistant", "type": "error", "content": error})
                elif url:
                    st.image(url)
                    st.session_state.chat_history.append({"role": "assistant", "type": "image", "content": url})

        # Music Generation
        elif any(keyword in prompt_lower for keyword in ['музыка', 'песня', 'трек']):
            with st.spinner("Генерация музыки... (это может занять некоторое время)"):
                audio_path, error = generate_music(prompt)
                if error:
                    st.error(error)
                    st.session_state.chat_history.append({"role": "assistant", "type": "error", "content": error})
                elif audio_path:
                    st.audio(audio_path)
                    st.session_state.chat_history.append({"role": "assistant", "type": "music", "content": audio_path})

        # Video Generation
        elif any(keyword in prompt_lower for keyword in ['видео', 'ролик']):
            with st.spinner("Генерация видео... (это может занять некоторое время)"):
                video_path, error = generate_video(prompt)
                if error:
                    st.error(error)
                    st.session_state.chat_history.append({"role": "assistant", "type": "error", "content": error})
                elif video_path:
                    st.video(video_path)
                    st.session_state.chat_history.append({"role": "assistant", "type": "video", "content": video_path})

        # Text Generation (Default)
        else:
            if not st.session_state.current_api_key:
                st.error("Пожалуйста, введите ваш API ключ в боковой панели.")
            else:
                with st.spinner("Генерация текста..."):
                    response_stream, error = generate_text(prompt, st.session_state.chat_session)
                    if error:
                        st.error(error)
                        st.session_state.chat_history.append({"role": "assistant", "type": "error", "content": error})
                    elif response_stream:
                        placeholder = st.empty()
                        full_response = ""
                        try:
                            for chunk in response_stream:
                                if chunk.text:
                                    full_response += chunk.text
                                    placeholder.markdown(full_response + "▌")
                            placeholder.markdown(full_response)
                            st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": full_response})
                        except Exception as e:
                            error_msg = f"Error streaming text: {e}"
                            st.error(error_msg)
                            st.session_state.chat_history.append({"role": "assistant", "type": "error", "content": error_msg})
