import streamlit as st
import google.generativeai as genai
from gradio_client import Client
import os

from modules.text import get_gemini_response
from modules.image import generate_image
from modules.music import generate_music
from modules.video import generate_video

# --- Configure Streamlit Page ---
st.set_page_config(
    page_title="Gemini Ultimate Bot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("Gemini Ultimate Bot 🤖")
st.markdown("Your all-in-one bot for Text, Image, Music, and Video generation.")

# --- Initialization / Caching ---
@st.cache_resource
def load_music_client():
    return Client("sanchit-gandhi/musicgen-streaming")

@st.cache_resource
def load_video_client():
    return Client("damo-vilab/modelscope-text-to-video-synthesis")

# --- Sidebar ---
with st.sidebar:
    st.header("Configuration")
    api_key = st.text_input("Enter your GOOGLE_API_KEY", type="password")

    if api_key:
        genai.configure(api_key=api_key)

    st.divider()

    st.header("Controls")
    generation_mode = st.radio("Select Mode", ["Text", "Image", "Music", "Video"])

    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.session_state.chat_session = None
        st.success("Chat history cleared.")

# --- Session State for Text Chat ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat_session" not in st.session_state:
    st.session_state.chat_session = None

# --- Main Logic ---
if generation_mode == "Text":
    st.subheader("Text Generation with Gemini 1.5 Flash")

    if not api_key:
        st.warning("Please enter your GOOGLE_API_KEY in the sidebar to use text generation.")
    else:
        # Display chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Accept user input
        if prompt := st.chat_input("What is up?"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                full_response = ""

                with st.spinner("Thinking..."):
                    response, new_chat_session = get_gemini_response(prompt, st.session_state.chat_session)

                    if isinstance(response, str) and response.startswith("An error occurred:"):
                         st.error(response)
                    else:
                        st.session_state.chat_session = new_chat_session
                        for chunk in response:
                            if chunk.text:
                                full_response += chunk.text
                                message_placeholder.markdown(full_response + "▌")
                        message_placeholder.markdown(full_response)
                        st.session_state.messages.append({"role": "assistant", "content": full_response})

elif generation_mode == "Image":
    st.subheader("Image Generation with Pollinations.ai")
    prompt = st.text_input("Enter a prompt for the image:")
    if st.button("Generate Image"):
        if prompt:
            with st.spinner("Generating image..."):
                image_bytes = generate_image(prompt)
                if isinstance(image_bytes, str) and image_bytes.startswith("An error occurred:"):
                    st.error(image_bytes)
                else:
                    st.image(image_bytes, caption=prompt)
        else:
            st.warning("Please enter a prompt.")

elif generation_mode == "Music":
    st.subheader("Music Generation with MusicGen")
    prompt = st.text_input("Enter a description of the music you want to generate:")
    if st.button("Generate Music"):
        if prompt:
            with st.spinner("Generating music (this might take a while)..."):
                music_client = load_music_client()
                audio_path = generate_music(music_client, prompt)

                if isinstance(audio_path, str) and audio_path.startswith("An error occurred:"):
                    st.error(audio_path)
                elif audio_path:
                    st.audio(audio_path)
                else:
                    st.error("Failed to generate music.")
        else:
            st.warning("Please enter a description.")

elif generation_mode == "Video":
    st.subheader("Video Generation with ModelScope")
    prompt = st.text_input("Enter a description of the video you want to generate:")
    if st.button("Generate Video"):
        if prompt:
             with st.spinner("Generating video (this might take a while)..."):
                video_client = load_video_client()
                video_path = generate_video(video_client, prompt)

                if isinstance(video_path, str) and video_path.startswith("An error occurred:"):
                    st.error(video_path)
                elif video_path:
                    st.video(video_path)
                else:
                    st.error("Failed to generate video.")
        else:
            st.warning("Please enter a description.")
