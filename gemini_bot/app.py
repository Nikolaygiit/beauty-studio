import streamlit as st

# Custom modules
from modules import text, image, music, video, routing

st.set_page_config(page_title="Gemini Ultimate Bot", layout="wide")
st.title("Gemini Ultimate Bot")

# Sidebar
st.sidebar.header("Настройки")
api_key_input = st.sidebar.text_input("Введите GOOGLE_API_KEY", type="password")

if st.sidebar.button("Очистить историю чата"):
    st.session_state.chat_history = []
    if 'chat_session' in st.session_state:
        del st.session_state['chat_session']
    if 'gemini_client' in st.session_state:
        del st.session_state['gemini_client']
    if 'current_api_key' in st.session_state:
        st.session_state.current_api_key = None
    st.rerun()

# Initialize state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

if 'current_api_key' not in st.session_state:
    st.session_state.current_api_key = None

# Update client and chat session if API key changes or is newly provided
if api_key_input and api_key_input != st.session_state.current_api_key:
    try:
        client = text.get_text_client(api_key_input)
        chat_session = text.start_chat_session(client)
        st.session_state.gemini_client = client
        st.session_state.chat_session = chat_session
        st.session_state.current_api_key = api_key_input
        st.sidebar.success("API ключ успешно применен!")
    except Exception as e:
        st.sidebar.error(f"Ошибка при инициализации API: {e}")
elif not api_key_input:
    st.info("Пожалуйста, введите ваш GOOGLE_API_KEY в боковой панели.")
    st.stop()

# Display chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        if message["type"] == "text":
            st.markdown(message["content"])
        elif message["type"] == "image":
            st.image(message["content"], caption="Сгенерированное изображение")
        elif message["type"] == "music":
            st.audio(message["content"], format='audio/wav')
        elif message["type"] == "video":
            st.video(message["content"])
        elif message["type"] == "error":
            st.error(message["content"])

# User prompt
prompt = st.chat_input("Введите ваш запрос...")

if prompt:
    # Display user prompt
    st.chat_message("user").markdown(prompt)
    st.session_state.chat_history.append({"role": "user", "type": "text", "content": prompt})

    route = routing.get_route(prompt)

    with st.chat_message("assistant"):
        if route == "text":
            with st.spinner("Генерация текста..."):
                response_container = st.empty()
                full_response = ""
                for chunk in text.stream_text_response(st.session_state.chat_session, prompt):
                    full_response += chunk
                    response_container.markdown(full_response + "▌")
                response_container.markdown(full_response)
                st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": full_response})

        elif route == "image":
            with st.spinner("Генерация изображения..."):
                img_url, error = image.generate_image(prompt)
                if error:
                    st.error(error)
                    st.session_state.chat_history.append({"role": "assistant", "type": "error", "content": error})
                else:
                    st.image(img_url, caption="Сгенерированное изображение")
                    st.session_state.chat_history.append({"role": "assistant", "type": "image", "content": img_url})

        elif route == "music":
            with st.spinner("Генерация музыки... Это может занять некоторое время."):
                audio_path, error = music.generate_music(prompt)
                if error:
                    st.error(error)
                    st.session_state.chat_history.append({"role": "assistant", "type": "error", "content": error})
                else:
                    st.audio(audio_path, format='audio/wav')
                    st.session_state.chat_history.append({"role": "assistant", "type": "music", "content": audio_path})

        elif route == "video":
            with st.spinner("Генерация видео... Это может занять некоторое время."):
                video_path, error = video.generate_video(prompt)
                if error:
                    st.error(error)
                    st.session_state.chat_history.append({"role": "assistant", "type": "error", "content": error})
                else:
                    st.video(video_path)
                    st.session_state.chat_history.append({"role": "assistant", "type": "video", "content": video_path})
