import streamlit as st
from modules.text import init_client, init_chat, generate_text_stream
from modules.image import generate_image
from modules.music import generate_music
from modules.video import generate_video

# --- Configure Streamlit Page ---
st.set_page_config(
    page_title="Gemini Ultimate Bot",
    page_icon="✨",
    layout="wide"
)

# --- Initialize Session State ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "chat_session" not in st.session_state:
    st.session_state.chat_session = None
if "gemini_client" not in st.session_state:
    st.session_state.gemini_client = None
if "current_api_key" not in st.session_state:
    st.session_state.current_api_key = ""

# --- Helper Functions ---
def reset_session():
    st.session_state.chat_history = []
    st.session_state.chat_session = None
    st.session_state.gemini_client = None
    st.session_state.current_api_key = ""

@st.cache_resource
def cached_generate_music(prompt):
    return generate_music(prompt)

@st.cache_resource
def cached_generate_video(prompt):
    return generate_video(prompt)

# --- Sidebar UI ---
with st.sidebar:
    st.title("✨ Настройки бота")
    st.markdown("Введите ваш API-ключ от Google (Gemini) для работы.")

    api_key = st.text_input("Google API Key", type="password", key="api_key_input")

    # Initialize client if API key changes
    if api_key and api_key != st.session_state.current_api_key:
        with st.spinner("Инициализация..."):
            client, error = init_client(api_key)
            if error:
                st.error(f"Ошибка инициализации API: {error}")
            else:
                chat, chat_error = init_chat(client)
                if chat_error:
                    st.error(f"Ошибка создания сессии: {chat_error}")
                else:
                    st.session_state.gemini_client = client
                    st.session_state.chat_session = chat
                    st.session_state.current_api_key = api_key
                    st.success("API ключ успешно применен!")

    st.markdown("---")
    st.markdown("### Инструкция по генерации")
    st.markdown("""
    Бот автоматически определяет, что вы хотите сгенерировать по ключевым словам:
    * **Изображение**: используйте слова *нарисуй*, *фото*, *изображение*
    * **Музыка**: используйте слова *музыка*, *песня*, *трек*
    * **Видео**: используйте слова *видео*, *ролик*
    * **Текст**: просто напишите любой другой запрос.
    """)
    st.markdown("---")

    if st.button("🗑️ Очистить историю", on_click=reset_session):
        st.success("История очищена. Введите API-ключ заново.")

# --- Main Chat UI ---
st.title("✨ Gemini Ultimate Bot")
st.markdown("Генерация текста, изображений, музыки и видео!")

# Display Chat History
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
        elif message["type"] == "error":
            st.error(message["content"])

# User Input Handling
prompt = st.chat_input("Напишите ваш запрос...")

if prompt:
    # 1. Add user message to UI
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.chat_history.append({"role": "user", "type": "text", "content": prompt})

    # Check what kind of media to generate based on keywords
    prompt_lower = prompt.lower()

    if any(keyword in prompt_lower for keyword in ["нарисуй", "фото", "изображение"]):
        # Generate Image
        with st.chat_message("assistant"):
            with st.spinner("Рисую изображение..."):
                url, error = generate_image(prompt)
                if error:
                    st.error(error)
                    st.session_state.chat_history.append({"role": "assistant", "type": "error", "content": error})
                else:
                    st.image(url)
                    st.session_state.chat_history.append({"role": "assistant", "type": "image", "content": url})

    elif any(keyword in prompt_lower for keyword in ["музыка", "песня", "трек"]):
        # Generate Music
        with st.chat_message("assistant"):
            with st.spinner("Генерирую музыку (может занять время)..."):
                audio_path, error = cached_generate_music(prompt)
                if error:
                    st.error(error)
                    st.session_state.chat_history.append({"role": "assistant", "type": "error", "content": error})
                else:
                    st.audio(audio_path)
                    st.session_state.chat_history.append({"role": "assistant", "type": "audio", "content": audio_path})

    elif any(keyword in prompt_lower for keyword in ["видео", "ролик"]):
        # Generate Video
        with st.chat_message("assistant"):
            with st.spinner("Создаю видео (очень ресурсоемко, подождите)..."):
                video_path, error = cached_generate_video(prompt)
                if error:
                    st.error(error)
                    st.session_state.chat_history.append({"role": "assistant", "type": "error", "content": error})
                else:
                    st.video(video_path)
                    st.session_state.chat_history.append({"role": "assistant", "type": "video", "content": video_path})

    else:
        # Generate Text (requires API key)
        if not st.session_state.chat_session:
            st.error("Пожалуйста, введите Google API Key в меню слева для генерации текста.")
        else:
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                full_response = ""
                with st.spinner("Думаю..."):
                    stream = generate_text_stream(st.session_state.chat_session, prompt)
                    for chunk in stream:
                        full_response += chunk
                        message_placeholder.markdown(full_response + "▌")
                    message_placeholder.markdown(full_response)

                if full_response.startswith("Ошибка:"):
                    st.session_state.chat_history.append({"role": "assistant", "type": "error", "content": full_response})
                else:
                    st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": full_response})
