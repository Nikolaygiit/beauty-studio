import streamlit as st
import modules.text as text
import modules.image as image
import modules.music as music
import modules.video as video

st.set_page_config(page_title="Gemini Ultimate Bot", layout="wide")

# Initialize clients (cached to avoid re-init)
@st.cache_resource
def load_music_client():
    return music.get_music_client()

@st.cache_resource
def load_video_client():
    return video.get_video_client()

music_client = load_music_client()
video_client = load_video_client()

# Session State Initialization
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "chat_session" not in st.session_state:
    st.session_state.chat_session = None
if "gemini_client" not in st.session_state:
    st.session_state.gemini_client = None
if "current_api_key" not in st.session_state:
    st.session_state.current_api_key = ""

with st.sidebar:
    st.title("⚙️ Настройки")
    api_key = st.text_input("Google API Key", type="password", value=st.session_state.current_api_key)

    if st.button("Очистить историю чата"):
        st.session_state.chat_history = []
        st.session_state.chat_session = None
        st.session_state.gemini_client = None
        st.session_state.current_api_key = ""
        st.rerun()

    if api_key and api_key != st.session_state.current_api_key:
        st.session_state.current_api_key = api_key
        st.session_state.gemini_client, st.session_state.chat_session = text.initialize_chat(api_key)

st.title("🤖 Gemini Ultimate Bot")
st.write("Генерация текста, изображений, музыки и видео!")

if not st.session_state.current_api_key:
    st.info("Пожалуйста, введите ваш Google API Key в боковой панели.")
    st.stop()

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

if prompt := st.chat_input("Введите ваш запрос..."):
    # Append user message
    st.session_state.chat_history.append({"role": "user", "type": "text", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        prompt_lower = prompt.lower()

        # Image Generation Routing
        if any(keyword in prompt_lower for keyword in ["нарисуй", "фото", "изображение"]):
            with st.spinner("Создаю изображение..."):
                url, err = image.generate_image(prompt)
                if err:
                    st.error(err)
                    st.session_state.chat_history.append({"role": "assistant", "type": "error", "content": err})
                else:
                    st.image(url)
                    st.session_state.chat_history.append({"role": "assistant", "type": "image", "content": url})

        # Music Generation Routing
        elif any(keyword in prompt_lower for keyword in ["музыка", "песня", "трек"]):
            with st.spinner("Создаю музыку..."):
                audio_path, err = music.generate_music(prompt, music_client)
                if err:
                    st.error(err)
                    st.session_state.chat_history.append({"role": "assistant", "type": "error", "content": err})
                else:
                    st.audio(audio_path)
                    st.session_state.chat_history.append({"role": "assistant", "type": "audio", "content": audio_path})

        # Video Generation Routing
        elif any(keyword in prompt_lower for keyword in ["видео", "ролик"]):
            with st.spinner("Создаю видео... (это может занять время)"):
                video_path, err = video.generate_video(prompt, video_client)
                if err:
                    st.error(err)
                    st.session_state.chat_history.append({"role": "assistant", "type": "error", "content": err})
                else:
                    st.video(video_path)
                    st.session_state.chat_history.append({"role": "assistant", "type": "video", "content": video_path})

        # Default: Text Generation Routing
        else:
            with st.spinner("Думаю..."):
                response_stream = text.generate_text_stream(prompt, st.session_state.chat_session)
                response_container = st.empty()
                full_response = ""

                if isinstance(response_stream, list) and response_stream[0].startswith("Text generation error"):
                    st.error(response_stream[0])
                    st.session_state.chat_history.append({"role": "assistant", "type": "error", "content": response_stream[0]})
                else:
                    for chunk in response_stream:
                        if hasattr(chunk, 'text'):
                            full_response += chunk.text
                        elif isinstance(chunk, str):
                            full_response += chunk
                        response_container.markdown(full_response + "▌")
                    response_container.markdown(full_response)
                    st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": full_response})
