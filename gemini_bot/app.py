import streamlit as st
from modules.text import initialize_chat, generate_text_stream
from modules.image import generate_image_url
from modules.music import init_music_client, generate_music
from modules.video import init_video_client, generate_video

# Initialize resource-heavy clients and cache them
@st.cache_resource
def get_music_client():
    return init_music_client()

@st.cache_resource
def get_video_client():
    return init_video_client()

st.title("Gemini Ultimate Bot")

# Sidebar for config and actions
with st.sidebar:
    st.header("Настройки")
    api_key = st.text_input("Введите GOOGLE_API_KEY", type="password")

    if st.button("Clear Chat History"):
        st.session_state.chat_session = None
        st.session_state.messages = []
        st.rerun()

# Initialize session state for messages and chat session
if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_session" not in st.session_state:
    st.session_state.chat_session = None

# Show error if API key is not provided yet
if not api_key:
    st.warning("Пожалуйста, введите ваш GOOGLE_API_KEY в боковом меню.")
    st.stop()

# Initialize chat session if it's not initialized or if it was cleared
if st.session_state.chat_session is None:
    st.session_state.chat_session = initialize_chat(api_key)
    if isinstance(st.session_state.chat_session, str):
        st.error(st.session_state.chat_session)
        st.session_state.chat_session = None
        st.stop()

# Display chat messages from history
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
    # Display user message
    st.session_state.messages.append({"role": "user", "type": "text", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Route based on keywords
    prompt_lower = prompt.lower()

    if any(word in prompt_lower for word in ['нарисуй', 'фото', 'изображение']):
        # Image Generation
        with st.chat_message("assistant"):
            st.markdown(f"Генерирую изображение по запросу: *{prompt}*...")
            image_url = generate_image_url(prompt)
            st.image(image_url)
        st.session_state.messages.append({"role": "assistant", "type": "image", "content": image_url})

    elif any(word in prompt_lower for word in ['музыка', 'песня', 'трек']):
        # Music Generation
        with st.chat_message("assistant"):
            with st.spinner(f"Создаю музыку по запросу: *{prompt}*..."):
                music_client = get_music_client()
                if isinstance(music_client, str):
                    st.error(music_client)
                else:
                    audio_result = generate_music(prompt, music_client)
                    if isinstance(audio_result, str) and audio_result.startswith("Error"):
                         st.error(audio_result)
                    else:
                        st.audio(audio_result)
                        st.session_state.messages.append({"role": "assistant", "type": "music", "content": audio_result})

    elif any(word in prompt_lower for word in ['видео', 'ролик']):
        # Video Generation
        with st.chat_message("assistant"):
             with st.spinner(f"Создаю видео по запросу: *{prompt}*..."):
                 video_client = get_video_client()
                 if isinstance(video_client, str):
                     st.error(video_client)
                 else:
                     video_result = generate_video(prompt, video_client)
                     if isinstance(video_result, str) and video_result.startswith("Error"):
                         st.error(video_result)
                     else:
                         st.video(video_result)
                         st.session_state.messages.append({"role": "assistant", "type": "video", "content": video_result})

    else:
        # Text Generation (Gemini)
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            for chunk in generate_text_stream(st.session_state.chat_session, prompt):
                full_response += chunk
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "type": "text", "content": full_response})
