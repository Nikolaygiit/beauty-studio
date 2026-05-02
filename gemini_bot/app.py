import streamlit as st
from modules.text import init_client, init_chat_session, stream_text_response
from modules.image import generate_image
from modules.music import generate_music
from modules.video import generate_video

# --- Page Configuration ---
st.set_page_config(
    page_title="Gemini Ultimate Bot",
    page_icon="🤖",
    layout="wide"
)

# --- Initialization & State Management ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "chat_session" not in st.session_state:
    st.session_state.chat_session = None
if "gemini_client" not in st.session_state:
    st.session_state.gemini_client = None
if "current_api_key" not in st.session_state:
    st.session_state.current_api_key = ""

def clear_chat():
    """Resets the chat history and session states."""
    st.session_state.chat_history = []
    st.session_state.chat_session = None
    st.session_state.gemini_client = None
    st.session_state.current_api_key = ""

# --- Sidebar UI ---
with st.sidebar:
    st.title("⚙️ Настройки")
    api_key = st.text_input("Введите ваш Google Gemini API Key:", type="password")

    st.markdown("---")
    st.markdown("### Доступные функции:")
    st.markdown("- 💬 **Текст:** Обычный диалог с Gemini")
    st.markdown("- 🖼️ **Изображения:** Напишите 'нарисуй', 'фото' или 'изображение' и описание")
    st.markdown("- 🎵 **Музыка:** Напишите 'музыка', 'песня' или 'трек' и описание")
    st.markdown("- 🎥 **Видео:** Напишите 'видео' или 'ролик' и описание")

    st.markdown("---")
    st.button("Очистить историю чата", on_click=clear_chat)

# --- Main Logic ---
st.title("🤖 Gemini Ultimate Bot")
st.markdown("Универсальный бот: текст, изображения, музыка и видео!")

# Validate and Initialize API Key
if api_key:
    if api_key != st.session_state.current_api_key:
        try:
            client = init_client(api_key)
            # Make sure to initialize the chat session here and store it in state
            st.session_state.gemini_client = client
            st.session_state.chat_session = init_chat_session(client)
            st.session_state.current_api_key = api_key
            st.sidebar.success("API Key успешно установлен!")
        except Exception as e:
            st.error(f"Ошибка при инициализации API: {str(e)}")
            st.stop()
else:
    st.info("Пожалуйста, введите ваш Google Gemini API Key в боковой панели, чтобы начать.")
    st.stop()

# Display chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        if message["type"] == "text":
            st.markdown(message["content"])
        elif message["type"] == "image":
            st.image(message["content"])
        elif message["type"] == "audio":
            st.audio(message["content"])
        elif message["type"] == "video":
            st.video(message["content"])

# User Input
if prompt := st.chat_input("Введите ваш запрос..."):
    # Append user prompt to history
    st.session_state.chat_history.append({"role": "user", "type": "text", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    prompt_lower = prompt.lower()

    with st.chat_message("assistant"):
        # Route to Image Generator
        if any(keyword in prompt_lower for keyword in ["нарисуй", "фото", "изображение"]):
            with st.spinner("Создаю изображение..."):
                image_url, error = generate_image(prompt)
                if error:
                    st.error(error)
                    st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": error})
                elif image_url:
                    st.image(image_url)
                    st.session_state.chat_history.append({"role": "assistant", "type": "image", "content": image_url})

        # Route to Music Generator
        elif any(keyword in prompt_lower for keyword in ["музыка", "песня", "трек"]):
            with st.spinner("Создаю музыку (это может занять около 30 секунд)..."):
                audio_path, error = generate_music(prompt)
                if error:
                    st.error(error)
                    st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": error})
                elif audio_path:
                    st.audio(audio_path)
                    st.session_state.chat_history.append({"role": "assistant", "type": "audio", "content": audio_path})

        # Route to Video Generator
        elif any(keyword in prompt_lower for keyword in ["видео", "ролик"]):
            with st.spinner("Создаю видео (это может занять время)..."):
                video_path, error = generate_video(prompt)
                if error:
                    st.error(error)
                    st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": error})
                elif video_path:
                    st.video(video_path)
                    st.session_state.chat_history.append({"role": "assistant", "type": "video", "content": video_path})

        # Route to Text (Gemini Model)
        else:
            if st.session_state.chat_session:
                with st.spinner("Думаю..."):
                    # Use st.write_stream to output the generator from stream_text_response
                    response_text = st.write_stream(stream_text_response(st.session_state.chat_session, prompt))
                    # Storing the joined streamed text
                    st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": response_text})
            else:
                 error_msg = "Чат-сессия не инициализирована. Пожалуйста, проверьте ваш API ключ."
                 st.error(error_msg)
                 st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": error_msg})
