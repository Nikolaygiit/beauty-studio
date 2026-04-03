import streamlit as st
from modules import text, image, music, video

st.set_page_config(page_title="Gemini Ultimate Bot", page_icon="🤖")

st.title("Gemini Ultimate Bot")
st.markdown("Генерация текста, изображений, музыки и видео!")

# --- Sidebar ---
st.sidebar.title("Настройки")
api_key = st.sidebar.text_input("Введите GOOGLE_API_KEY", type="password")

if st.sidebar.button("Очистить историю чата"):
    st.session_state.chat_history = []
    if "chat_session" in st.session_state:
        del st.session_state.chat_session
    st.rerun()

# --- Caching Resource Heavy Clients ---
@st.cache_resource
def load_music_client():
    return music.get_music_client()

@st.cache_resource
def load_video_client():
    return video.get_video_client()

# --- Session State Initialization ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "chat_session" not in st.session_state and api_key:
    try:
        st.session_state.chat_session = text.init_chat_session(api_key)
    except Exception as e:
        st.error(f"Ошибка инициализации Gemini: {e}")

# --- Display Chat History ---
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
        elif message["type"] == "error":
             st.error(message["content"])

# --- Chat Input & Routing ---
prompt = st.chat_input("Напишите сообщение...")

if prompt:
    if not api_key:
        st.warning("Пожалуйста, введите GOOGLE_API_KEY в боковой панели.")
    else:
        # 1. Add user message to UI and history
        st.chat_message("user").markdown(prompt)
        st.session_state.chat_history.append({"role": "user", "type": "text", "content": prompt})

        # 2. Routing logic
        lower_prompt = prompt.lower()

        # IMAGE ROUTING
        if any(keyword in lower_prompt for keyword in ["нарисуй", "фото", "изображение"]):
            with st.chat_message("assistant"):
                st.markdown("Генерирую изображение...")
                image_url = image.generate_image_url(prompt)
                st.image(image_url)
                st.session_state.chat_history.append({"role": "assistant", "type": "image", "content": image_url})

        # MUSIC ROUTING
        elif any(keyword in lower_prompt for keyword in ["музыка", "песня", "трек"]):
            with st.chat_message("assistant"):
                st.markdown("Генерирую музыку (это может занять некоторое время)...")
                music_client = load_music_client()
                if isinstance(music_client, str): # Error initializing
                     st.error(music_client)
                     st.session_state.chat_history.append({"role": "assistant", "type": "error", "content": music_client})
                else:
                    audio_path = music.generate_music(music_client, prompt)
                    if isinstance(audio_path, str) and audio_path.startswith("Error"):
                        st.error(audio_path)
                        st.session_state.chat_history.append({"role": "assistant", "type": "error", "content": audio_path})
                    else:
                        st.audio(audio_path)
                        st.session_state.chat_history.append({"role": "assistant", "type": "music", "content": audio_path})

        # VIDEO ROUTING
        elif any(keyword in lower_prompt for keyword in ["видео", "ролик"]):
            with st.chat_message("assistant"):
                st.markdown("Генерирую видео (это может занять значительное время)...")
                video_client = load_video_client()
                if isinstance(video_client, str): # Error initializing
                     st.error(video_client)
                     st.session_state.chat_history.append({"role": "assistant", "type": "error", "content": video_client})
                else:
                    video_path = video.generate_video(video_client, prompt)
                    if isinstance(video_path, str) and video_path.startswith("Error"):
                        st.error(video_path)
                        st.session_state.chat_history.append({"role": "assistant", "type": "error", "content": video_path})
                    else:
                        st.video(video_path)
                        st.session_state.chat_history.append({"role": "assistant", "type": "video", "content": video_path})

        # TEXT ROUTING (Fallback)
        else:
            with st.chat_message("assistant"):
                if "chat_session" in st.session_state:
                    response_placeholder = st.empty()
                    full_response = ""
                    # We pass the prompt to the generator
                    for chunk in text.generate_text_stream(st.session_state.chat_session, prompt):
                        full_response += chunk
                        response_placeholder.markdown(full_response + "▌")
                    response_placeholder.markdown(full_response)
                    st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": full_response})
                else:
                    st.error("Сессия чата не инициализирована.")
