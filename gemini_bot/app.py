import streamlit as st
from modules.image import generate_image
from modules.music import generate_music
from modules.video import generate_video
from modules.text import init_client, generate_text_stream

st.set_page_config(page_title="Gemini Ultimate Bot", page_icon="🤖")

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "chat_session" not in st.session_state:
    st.session_state.chat_session = None
if "gemini_client" not in st.session_state:
    st.session_state.gemini_client = None
if "current_api_key" not in st.session_state:
    st.session_state.current_api_key = ""

# Sidebar
st.sidebar.title("Настройки")
api_key = st.sidebar.text_input("Введите GOOGLE_API_KEY", type="password")

if st.sidebar.button("Clear Chat History"):
    st.session_state.chat_history = []
    st.session_state.chat_session = None
    st.session_state.gemini_client = None
    st.session_state.current_api_key = ""
    st.rerun()

# Update client if API key changes
if api_key != st.session_state.current_api_key:
    st.session_state.current_api_key = api_key
    if api_key:
        client = init_client(api_key)
        if client:
            st.session_state.gemini_client = client
            st.session_state.chat_session = client.chats.create(model="gemini-2.0-flash")
        else:
            st.session_state.gemini_client = None
            st.session_state.chat_session = None
            st.sidebar.error("Ошибка при инициализации клиента Gemini.")

st.title("🤖 Gemini Ultimate Bot")
st.write("Привет! Я могу генерировать текст, изображения, музыку и видео. Что бы вы хотели создать?")

# Display chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        if message["type"] == "text":
            st.markdown(message["content"])
        elif message["type"] == "image":
            st.image(message["content"])
        elif message["type"] == "music":
            st.audio(message["content"])
        elif message["type"] == "video":
            st.video(message["content"])

# User input
if prompt := st.chat_input("Введите ваш запрос..."):
    # Add user message to chat history
    st.session_state.chat_history.append({"role": "user", "type": "text", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    prompt_lower = prompt.lower()

    with st.chat_message("assistant"):
        # Image routing
        if 'нарисуй' in prompt_lower or 'фото' in prompt_lower or 'изображение' in prompt_lower:
            with st.spinner("Генерация изображения..."):
                url, error = generate_image(prompt)
                if error:
                    st.error(f"Ошибка при генерации изображения: {error}")
                    st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": f"Ошибка: {error}"})
                else:
                    st.image(url)
                    st.session_state.chat_history.append({"role": "assistant", "type": "image", "content": url})

        # Music routing
        elif 'музыка' in prompt_lower or 'песня' in prompt_lower or 'трек' in prompt_lower:
            with st.spinner("Генерация музыки..."):
                audio_path, error = generate_music(prompt)
                if error:
                    st.error(f"Ошибка при генерации музыки: {error}")
                    st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": f"Ошибка: {error}"})
                else:
                    # musicgen result is sometimes a tuple/list, the actual path is typically the first element if so,
                    # but gradio_client usually returns a string path for files
                    if isinstance(audio_path, tuple) or isinstance(audio_path, list):
                        audio_path = audio_path[0]
                    st.audio(audio_path)
                    st.session_state.chat_history.append({"role": "assistant", "type": "music", "content": audio_path})

        # Video routing
        elif 'видео' in prompt_lower or 'ролик' in prompt_lower:
            with st.spinner("Генерация видео..."):
                video_path, error = generate_video(prompt)
                if error:
                    st.error(f"Ошибка при генерации видео: {error}")
                    st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": f"Ошибка: {error}"})
                else:
                    if isinstance(video_path, dict) and 'video' in video_path:
                        video_path = video_path['video']
                    elif isinstance(video_path, tuple) or isinstance(video_path, list):
                        video_path = video_path[0]
                    st.video(video_path)
                    st.session_state.chat_history.append({"role": "assistant", "type": "video", "content": video_path})

        # Text routing (default)
        else:
            if not st.session_state.gemini_client or not st.session_state.chat_session:
                msg = "Пожалуйста, введите валидный GOOGLE_API_KEY в боковой панели для генерации текста."
                st.warning(msg)
                st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": msg})
            else:
                response_container = st.empty()
                full_response = ""
                for chunk in generate_text_stream(st.session_state.gemini_client, st.session_state.chat_session, prompt):
                    full_response += chunk
                    response_container.markdown(full_response + "▌")
                response_container.markdown(full_response)
                st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": full_response})
