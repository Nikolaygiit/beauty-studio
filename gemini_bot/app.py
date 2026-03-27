import streamlit as st
from modules.text import get_chat_session, generate_text_stream
from modules.image import generate_image_url
from modules.music import get_music_generator, generate_music
from modules.video import get_video_generator, generate_video

# Cached initializers
@st.cache_resource
def init_music_gen():
    return get_music_generator()

@st.cache_resource
def init_video_gen():
    return get_video_generator()

st.title("Gemini Ultimate Bot")

with st.sidebar:
    api_key = st.text_input("Enter GOOGLE_API_KEY", type="password")
    if st.button("Clear Chat History"):
        if "chat_session" in st.session_state:
            del st.session_state["chat_session"]
        st.rerun()

if not api_key:
    st.warning("Please enter your GOOGLE_API_KEY in the sidebar to continue.")
    st.stop()

if "chat_session" not in st.session_state:
    st.session_state["chat_session"] = get_chat_session(api_key)

if "messages" not in st.session_state:
    st.session_state["messages"] = []

for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        if "image_url" in msg:
            st.image(msg["image_url"])
        if "audio_path" in msg:
            st.audio(msg["audio_path"])
        if "video_path" in msg:
            st.video(msg["video_path"])

prompt = st.chat_input("Enter your message")

if prompt:
    st.session_state["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    prompt_lower = prompt.lower()
    msg_data = {"role": "assistant"}

    with st.chat_message("assistant"):
        if any(kw in prompt_lower for kw in ["нарисуй", "фото", "изображение"]):
            with st.spinner("Generating image..."):
                url = generate_image_url(prompt)
                st.image(url)
                msg_data["content"] = "Вот ваше изображение:"
                msg_data["image_url"] = url
                st.write(msg_data["content"])

        elif any(kw in prompt_lower for kw in ["музыка", "песня", "трек"]):
            with st.spinner("Generating music..."):
                client = init_music_gen()
                result = generate_music(client, prompt)
                if isinstance(result, str) and (result.startswith("Error") or result.startswith("Video")):
                    st.error(result)
                    msg_data["content"] = result
                else:
                    st.audio(result)
                    msg_data["content"] = "Вот ваша музыка:"
                    msg_data["audio_path"] = result
                    st.write(msg_data["content"])

        elif any(kw in prompt_lower for kw in ["видео", "ролик"]):
            with st.spinner("Generating video..."):
                client = init_video_gen()
                result = generate_video(client, prompt)
                if isinstance(result, str) and (result.startswith("Error") or result.startswith("Video")):
                    st.error(result)
                    msg_data["content"] = result
                else:
                    st.video(result)
                    msg_data["content"] = "Вот ваше видео:"
                    msg_data["video_path"] = result
                    st.write(msg_data["content"])

        else:
            with st.spinner("Thinking..."):
                response_container = st.empty()
                full_text = ""
                for chunk in generate_text_stream(st.session_state["chat_session"], prompt):
                    full_text += chunk
                    response_container.write(full_text)
                msg_data["content"] = full_text

    st.session_state["messages"].append(msg_data)
