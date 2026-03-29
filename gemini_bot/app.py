import streamlit as st
from google import genai
from modules.text import generate_text
from modules.image import generate_image
from modules.music import generate_music
from modules.video import generate_video

# Streamlit App Configuration
st.set_page_config(page_title="Gemini Ultimate Bot", page_icon="🤖", layout="wide")

st.title("Gemini Ultimate Bot")
st.write("Генерация текста, изображений, музыки и видео")

# Sidebar
with st.sidebar:
    st.header("Настройки")
    api_key = st.text_input("Введите ваш Google API Key", type="password")
    if st.button("Очистить историю чата"):
        st.session_state.chat_session = None
        st.session_state.messages = []
        st.rerun()

# Initialize session state for messages and chat session
if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_session" not in st.session_state:
    st.session_state.chat_session = None

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if "content" in message:
            st.markdown(message["content"])
        if "image" in message:
            st.image(message["image"])
        if "audio" in message:
            st.audio(message["audio"])
        if "video" in message:
            st.video(message["video"])

# Chat input
if prompt := st.chat_input("Введите ваш запрос..."):
    # Append user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    prompt_lower = prompt.lower()

    with st.chat_message("assistant"):
        # Image routing
        if any(keyword in prompt_lower for keyword in ["нарисуй", "фото", "изображение"]):
            with st.spinner("Генерация изображения..."):
                image_url = generate_image(prompt)
                st.image(image_url)
                st.session_state.messages.append({"role": "assistant", "image": image_url})

        # Music routing
        elif any(keyword in prompt_lower for keyword in ["музыка", "песня", "трек"]):
            with st.spinner("Генерация музыки..."):
                audio_path = generate_music(prompt)
                if audio_path:
                    st.audio(audio_path)
                    st.session_state.messages.append({"role": "assistant", "audio": audio_path})
                else:
                    error_msg = "Не удалось сгенерировать музыку."
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})

        # Video routing
        elif any(keyword in prompt_lower for keyword in ["видео", "ролик"]):
            with st.spinner("Генерация видео..."):
                video_result = generate_video(prompt)
                if isinstance(video_result, str) and (video_result.startswith("Ошибка:") or video_result == "Генерация видео недоступна."):
                    st.error(video_result)
                    st.session_state.messages.append({"role": "assistant", "content": video_result})
                elif video_result:
                    st.video(video_result)
                    st.session_state.messages.append({"role": "assistant", "video": video_result})
                else:
                    error_msg = "Не удалось сгенерировать видео."
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})

        # Text routing (default)
        else:
            if not api_key:
                st.warning("Пожалуйста, введите ваш Google API Key в боковой панели.")
            else:
                with st.spinner("Генерация текста..."):
                    # Initialize Gemini client if not exists or if chat_session is empty
                    if not st.session_state.chat_session:
                        try:
                            client = genai.Client(api_key=api_key)
                            # Create a chat session with the model
                            st.session_state.chat_session = client.chats.create(model="gemini-2.0-flash")
                        except Exception as e:
                            st.error(f"Ошибка инициализации Gemini: {e}")
                            st.stop()

                    response_text = generate_text(prompt, st.session_state.chat_session)
                    st.markdown(response_text)
                    st.session_state.messages.append({"role": "assistant", "content": response_text})
