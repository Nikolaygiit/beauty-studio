import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set page config
st.set_page_config(
    page_title="Gemini Ultimate Bot",
    page_icon="🤖",
    layout="wide"
)

# Sidebar for configuration
with st.sidebar:
    st.title("Configuration")

    # API Keys
    google_api_key = st.text_input("Google API Key", type="password", value=os.getenv("GOOGLE_API_KEY", ""))
    hf_token = st.text_input("Hugging Face Token (Optional)", type="password", value=os.getenv("HF_TOKEN", ""), help="Required for some Music/Video generation models if gated.")

    if not google_api_key:
        st.warning("Please enter your Google API Key to use the bot.")
        st.info("Get your API key from https://aistudio.google.com/")
        st.stop()

# Import modules
from modules.text import TextGenerator
from modules.image import ImageGenerator
from modules.music import MusicGenerator
from modules.video import VideoGenerator

# Initialize generators
if "text_generator" not in st.session_state or st.session_state.get("google_api_key_last") != google_api_key:
    if google_api_key:
        try:
            st.session_state.text_generator = TextGenerator(api_key=google_api_key)
            st.session_state.google_api_key_last = google_api_key
            # Clear chat history on re-initialization to avoid context mismatch
            st.session_state.messages = []
        except Exception as e:
             st.error(f"Failed to initialize Text Generator: {e}")

if "image_generator" not in st.session_state:
    st.session_state.image_generator = ImageGenerator()

if "music_generator" not in st.session_state or st.session_state.get("hf_token_last") != hf_token:
    st.session_state.music_generator = MusicGenerator(hf_token=hf_token if hf_token else None)
    st.session_state.hf_token_last = hf_token

if "video_generator" not in st.session_state or st.session_state.get("hf_token_last_video") != hf_token:
    st.session_state.video_generator = VideoGenerator(hf_token=hf_token if hf_token else None)
    st.session_state.hf_token_last_video = hf_token

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Main Interface
st.title("🤖 Gemini Ultimate Bot")
st.markdown("Your all-in-one AI assistant for Text, Image, Music, and Video generation.")

tab1, tab2, tab3, tab4 = st.tabs(["💬 Chat", "🖼️ Image", "🎵 Music", "🎥 Video"])

with tab1:
    st.header("Chat with Gemini")

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("What is on your mind?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate response
        with st.chat_message("assistant"):
            try:
                response = st.session_state.text_generator.send_message(prompt)
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                st.error(f"Error: {e}")

with tab2:
    st.header("Generate Images")
    image_prompt = st.text_area("Describe the image you want to generate:", height=100)
    col1, col2 = st.columns(2)
    with col1:
        width = st.slider("Width", 256, 1024, 1024, step=64)
    with col2:
        height = st.slider("Height", 256, 1024, 1024, step=64)

    if st.button("Generate Image"):
        if image_prompt:
            with st.spinner("Generating image..."):
                try:
                    image = st.session_state.image_generator.generate(image_prompt, width, height)
                    if image:
                        st.image(image, caption=image_prompt)
                    else:
                        st.error("Failed to generate image.")
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.warning("Please enter a prompt.")

with tab3:
    st.header("Generate Music")
    st.info("Powered by MusicGen Streaming (Hugging Face Space)")
    music_prompt = st.text_area("Describe the music you want to generate:", height=100, key="music_prompt")
    duration = st.slider("Duration (seconds)", 5, 30, 15)

    if st.button("Generate Music"):
        if music_prompt:
            with st.spinner("Generating music..."):
                try:
                    result = st.session_state.music_generator.generate(music_prompt, duration)
                    if isinstance(result, str) and result.startswith("Error"):
                        st.error(result)
                    else:
                        st.audio(result)
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.warning("Please enter a prompt.")

with tab4:
    st.header("Generate Video")
    st.info("Powered by ModelScope Text-to-Video (Hugging Face Space)")
    video_prompt = st.text_area("Describe the video you want to generate:", height=100, key="video_prompt")

    if st.button("Generate Video"):
        if video_prompt:
            with st.spinner("Generating video..."):
                try:
                    result = st.session_state.video_generator.generate(video_prompt)
                    if isinstance(result, str) and result.startswith("Error"):
                        st.error(result)
                    else:
                        st.video(result)
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.warning("Please enter a prompt.")
