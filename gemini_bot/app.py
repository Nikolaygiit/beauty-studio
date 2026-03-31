import streamlit as st
from modules import text, image, music, video

st.set_page_config(page_title="Gemini Ultimate Bot", page_icon="🤖")

st.title("Gemini Ultimate Bot")

# Sidebar
st.sidebar.title("Настройки")
api_key = st.sidebar.text_input("Введите GOOGLE_API_KEY", type="password")

if st.sidebar.button("Clear Chat History"):
    if "chat_session" in st.session_state:
        del st.session_state["chat_session"]
    if "messages" in st.session_state:
        del st.session_state["messages"]
    st.rerun()

# Initialize session state for messages and chat session
if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_session" not in st.session_state and api_key:
    st.session_state.chat_session = text.get_chat_session(api_key)

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["type"] == "text":
            st.markdown(message["content"])
        elif message["type"] == "image":
            st.image(message["content"])
        elif message["type"] == "audio":
            st.audio(message["content"])
        elif message["type"] == "video":
            st.video(message["content"])

# Chat input
if prompt := st.chat_input("Введите сообщение (например, 'нарисуй кота' или 'напиши стих')"):
    if not api_key:
        st.error("Пожалуйста, введите GOOGLE_API_KEY в боковом меню.")
        st.stop()

    if "chat_session" not in st.session_state:
        st.session_state.chat_session = text.get_chat_session(api_key)

    # Append user message to history
    st.session_state.messages.append({"role": "user", "type": "text", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    prompt_lower = prompt.lower()

    # Image Generation
    if "нарисуй" in prompt_lower or "фото" in prompt_lower or "изображение" in prompt_lower:
        with st.chat_message("assistant"):
            st.markdown(f"Генерирую изображение по запросу: *{prompt}*...")
            image_url = image.generate_image_url(prompt)
            st.image(image_url)
            st.session_state.messages.append({"role": "assistant", "type": "image", "content": image_url})

    # Music Generation
    elif "музыка" in prompt_lower or "песня" in prompt_lower or "трек" in prompt_lower:
        with st.chat_message("assistant"):
            st.markdown(f"Генерирую музыку по запросу: *{prompt}*... (Это может занять некоторое время)")
            client = music.get_music_client()
            audio_path, error = music.generate_music(client, prompt)

            if error:
                st.error(error)
                st.session_state.messages.append({"role": "assistant", "type": "text", "content": error})
            else:
                st.audio(audio_path)
                st.session_state.messages.append({"role": "assistant", "type": "audio", "content": audio_path})

    # Video Generation
    elif "видео" in prompt_lower or "ролик" in prompt_lower:
        with st.chat_message("assistant"):
            st.markdown(f"Генерирую видео по запросу: *{prompt}*... (Это может занять длительное время)")
            client = video.get_video_client()
            video_path, error = video.generate_video(client, prompt)

            if error:
                st.error(error)
                st.session_state.messages.append({"role": "assistant", "type": "text", "content": error})
            else:
                st.video(video_path)
                st.session_state.messages.append({"role": "assistant", "type": "video", "content": video_path})

    # Text Generation (Fallback)
    else:
        with st.chat_message("assistant"):
            response_placeholder = st.empty()
            full_response = ""
            for chunk in text.stream_text_response(st.session_state.chat_session, prompt):
                full_response += chunk
                response_placeholder.markdown(full_response + "▌")
            response_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "type": "text", "content": full_response})
