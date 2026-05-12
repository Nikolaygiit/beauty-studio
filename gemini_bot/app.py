import streamlit as st
from modules.text import get_gemini_client, create_chat_session, generate_text_stream
from modules.image import generate_image
from modules.music import generate_music
from modules.video import generate_video

# Streamlit page configuration
st.set_page_config(page_title="Gemini Ultimate Bot", page_icon="🤖", layout="wide")

st.title("🤖 Gemini Ultimate Bot")
st.markdown("Бот, который может генерировать текст, изображения, музыку и видео!")

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "chat_session" not in st.session_state:
    st.session_state.chat_session = None
if "gemini_client" not in st.session_state:
    st.session_state.gemini_client = None
if "current_api_key" not in st.session_state:
    st.session_state.current_api_key = ""

# Sidebar settings
with st.sidebar:
    st.header("Настройки")
    api_key = st.text_input("Введите ваш Google API Key", type="password")

    if api_key != st.session_state.current_api_key:
        st.session_state.current_api_key = api_key
        if api_key:
            client, error = get_gemini_client(api_key)
            if client:
                st.session_state.gemini_client = client
                chat_session, chat_error = create_chat_session(client)
                if chat_session:
                    st.session_state.chat_session = chat_session
                    st.success("API ключ успешно применен!")
                else:
                    st.error(chat_error)
            else:
                st.error(error)

    if st.button("Очистить историю чата"):
        st.session_state.chat_history = []
        if st.session_state.gemini_client:
            chat_session, chat_error = create_chat_session(st.session_state.gemini_client)
            if chat_session:
                 st.session_state.chat_session = chat_session
        st.rerun()

# Display chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        if message["type"] == "text":
            st.markdown(message["content"])
        elif message["type"] == "image":
            st.image(message["content"], caption=message["caption"])
        elif message["type"] == "music":
            st.audio(message["content"])
        elif message["type"] == "video":
            st.video(message["content"])

# Caching media generators
@st.cache_resource(show_spinner=False)
def generate_music_cached(prompt):
    return generate_music(prompt)

@st.cache_resource(show_spinner=False)
def generate_video_cached(prompt):
    return generate_video(prompt)

# User input
if prompt := st.chat_input("Напишите ваш запрос..."):
    if not st.session_state.current_api_key:
         st.warning("Пожалуйста, введите Google API Key в настройках.")
         st.stop()

    st.session_state.chat_history.append({"role": "user", "type": "text", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    prompt_lower = prompt.lower()

    with st.chat_message("assistant"):
        if any(keyword in prompt_lower for keyword in ['нарисуй', 'фото', 'изображение']):
            with st.spinner("Генерация изображения..."):
                image_url, error = generate_image(prompt)
                if image_url:
                    st.image(image_url, caption=prompt)
                    st.session_state.chat_history.append({"role": "assistant", "type": "image", "content": image_url, "caption": prompt})
                else:
                    st.error(error)

        elif any(keyword in prompt_lower for keyword in ['музыка', 'песня', 'трек']):
            with st.spinner("Генерация музыки... Это может занять некоторое время."):
                audio_path, error = generate_music_cached(prompt)
                if audio_path:
                    st.audio(audio_path)
                    st.session_state.chat_history.append({"role": "assistant", "type": "music", "content": audio_path})
                else:
                    st.error(error)

        elif any(keyword in prompt_lower for keyword in ['видео', 'ролик']):
            with st.spinner("Генерация видео... Это может занять некоторое время."):
                 video_path, error = generate_video_cached(prompt)
                 if video_path:
                     st.video(video_path)
                     st.session_state.chat_history.append({"role": "assistant", "type": "video", "content": video_path})
                 else:
                     st.error(error)
        else:
            if not st.session_state.chat_session:
                 st.error("Сессия чата не инициализирована. Проверьте API ключ.")
            else:
                 response_container = st.empty()
                 full_response = ""
                 try:
                     response_stream, error = generate_text_stream(st.session_state.chat_session, prompt)
                     if response_stream:
                         for chunk in response_stream:
                             if chunk.text:
                                 full_response += chunk.text
                                 response_container.markdown(full_response + "▌")
                         response_container.markdown(full_response)
                         st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": full_response})
                     else:
                         st.error(error)
                 except Exception as e:
                     st.error(f"Произошла ошибка при получении ответа от Gemini: {e}")
