import streamlit as st
from modules.text import generate_text
from modules.image import generate_image
from modules.music import generate_music, get_music_client
from modules.video import generate_video, get_video_client

st.set_page_config(page_title="Gemini Ultimate Bot", page_icon="🤖", layout="wide")

st.title("Gemini Ultimate Bot 🤖")
st.write("Генерация текста, изображений, музыки и видео в одном месте!")

# Sidebar configuration
st.sidebar.header("Настройки")
api_key = st.sidebar.text_input("Введите GOOGLE_API_KEY", type="password")
clear_chat_button = st.sidebar.button("Clear Chat History")

# Initialize session state for chat history and Gemini chat session
if "messages" not in st.session_state or clear_chat_button:
    st.session_state.messages = []
    st.session_state.chat_session = None

# Cache the gradio clients to avoid reinitializing on every interaction
@st.cache_resource
def load_music_client():
    return get_music_client()

@st.cache_resource
def load_video_client():
    return get_video_client()

music_client = load_music_client()
video_client = load_video_client()

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["type"] == "text":
            st.markdown(message["content"])
        elif message["type"] == "image":
            st.image(message["content"])
        elif message["type"] == "music":
            st.audio(message["content"])
        elif message["type"] == "video":
            st.video(message["content"])

# Chat input
if prompt := st.chat_input("Введите ваш запрос..."):
    # Determine the action based on keywords
    action = "text"
    lower_prompt = prompt.lower()

    if any(keyword in lower_prompt for keyword in ["нарисуй", "создай картинку", "сгенерируй изображение", "фото"]):
        action = "image"
    elif any(keyword in lower_prompt for keyword in ["создай музыку", "сгенерируй музыку", "песня", "мелодия"]):
        action = "music"
    elif any(keyword in lower_prompt for keyword in ["создай видео", "сгенерируй видео", "ролик"]):
        action = "video"

    st.session_state.messages.append({"role": "user", "type": "text", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        if action == "text":
            if not api_key:
                error_msg = "Пожалуйста, введите GOOGLE_API_KEY в настройках для генерации текста."
                st.markdown(error_msg)
                st.session_state.messages.append({"role": "assistant", "type": "text", "content": error_msg})
            else:
                with st.spinner("Генерация текста..."):
                    response_text, updated_session = generate_text(prompt, api_key, st.session_state.chat_session)
                    st.session_state.chat_session = updated_session
                    st.markdown(response_text)
                    st.session_state.messages.append({"role": "assistant", "type": "text", "content": response_text})

        elif action == "image":
            with st.spinner("Генерация изображения..."):
                image_url = generate_image(prompt)
                if image_url.startswith("http"):
                    st.image(image_url)
                    st.session_state.messages.append({"role": "assistant", "type": "image", "content": image_url})
                else:
                    st.error(image_url)
                    st.session_state.messages.append({"role": "assistant", "type": "text", "content": image_url})

        elif action == "music":
            with st.spinner("Генерация музыки (это может занять некоторое время)..."):
                music_result = generate_music(prompt, music_client)
                if isinstance(music_result, tuple):
                   music_result = music_result[0]

                if str(music_result).endswith('.wav') or str(music_result).endswith('.mp3'):
                    st.audio(music_result)
                    st.session_state.messages.append({"role": "assistant", "type": "music", "content": music_result})
                else:
                    st.error(f"Не удалось сгенерировать музыку: {music_result}")
                    st.session_state.messages.append({"role": "assistant", "type": "text", "content": f"Не удалось сгенерировать музыку: {music_result}"})

        elif action == "video":
            with st.spinner("Генерация видео (это может занять продолжительное время)..."):
                video_result = generate_video(prompt, video_client)

                # Check if it's a valid path
                if str(video_result).endswith('.mp4'):
                    st.video(video_result)
                    st.session_state.messages.append({"role": "assistant", "type": "video", "content": video_result})
                else:
                    st.error(f"Не удалось сгенерировать видео: {video_result}")
                    st.session_state.messages.append({"role": "assistant", "type": "text", "content": f"Не удалось сгенерировать видео: {video_result}"})
