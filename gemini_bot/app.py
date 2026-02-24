import streamlit as st
import os
import sys
import time
from PIL import Image
import io

# Add current directory to path so imports work
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from modules import text, image, music, video

# Page Config
st.set_page_config(
    page_title="Gemini Ultimate Bot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .stChatMessage {
        border-radius: 10px;
        padding: 10px;
        margin-bottom: 10px;
    }
    .stButton button {
        width: 100%;
        border-radius: 20px;
    }
    /* Hide the deploy button */
    .stDeployButton {
        display: none;
    }
</style>
""", unsafe_allow_html=True)

# Session State Initialization
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "chat_session" not in st.session_state:
    st.session_state.chat_session = None

# Sidebar
with st.sidebar:
    st.title("🤖 Gemini Ultimate")

    api_key = st.text_input("Google API Key", type="password", help="Get your key at https://aistudio.google.com/")

    st.markdown("### Navigation")
    mode = st.radio("Select Mode", ["Chat 💬", "Image Generation 🖼️", "Music Generation 🎵", "Video Generation 🎥"])

    if mode == "Chat 💬":
        if st.button("Clear Chat History", type="secondary"):
            st.session_state.chat_history = []
            st.session_state.chat_session = text.create_chat_session()
            st.rerun()

    st.markdown("---")
    st.markdown("### About")
    st.info("This bot uses Gemini 1.5 Flash for text/vision, Pollinations.ai for images, and Hugging Face Spaces for Music/Video.")
    st.markdown("Created by Jules")

# Main Application Logic

# Chat Mode
if mode == "Chat 💬":
    st.header("Chat with Gemini 💬")

    if not api_key:
        st.warning("Please enter your Google API Key in the sidebar to start chatting.")
        st.markdown("[Get your API key here](https://aistudio.google.com/)")
        st.stop()

    # Configure API if changed
    if "api_key_configured" not in st.session_state or st.session_state.api_key_configured != api_key:
        if text.configure_api(api_key):
            st.session_state.api_key_configured = api_key
            st.session_state.chat_session = text.create_chat_session() # Reset session on key change
            st.session_state.chat_history = []
            st.success("Connected to Gemini!")
            time.sleep(1)
            st.rerun()

    if st.session_state.chat_session is None:
        st.session_state.chat_session = text.create_chat_session()

    # Display Chat History
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            if "image" in message and message["image"]:
                st.image(message["image"], caption="Uploaded Image", width=300)
            st.markdown(message["content"])

    # Chat Input
    # File uploader outside chat_input
    with st.expander("Upload Image (Optional)", expanded=False):
        uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"], key="chat_image_upload")

    prompt = st.chat_input("Ask something...")

    if prompt:
        image_input = None
        if uploaded_file:
            image_input = Image.open(uploaded_file)

        # Display User Message
        with st.chat_message("user"):
            if image_input:
                st.image(image_input, caption="Uploaded Image", width=300)
            st.markdown(prompt)

        # Add to history
        st.session_state.chat_history.append({"role": "user", "content": prompt, "image": image_input})

        # Generate Response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = text.get_gemini_response(
                    st.session_state.chat_session,
                    prompt,
                    image=image_input
                )

                full_response = ""
                if isinstance(response, str): # Error message
                    st.error(response)
                    full_response = response
                else:
                    try:
                        full_response = response.text
                        st.markdown(full_response)
                    except ValueError:
                        st.error("Blocked by safety filters or empty response.")
                        full_response = "Error: Blocked by safety filters."

        # Add to history
        st.session_state.chat_history.append({"role": "assistant", "content": full_response})

# Image Mode
elif mode == "Image Generation 🖼️":
    st.header("Generate Images 🖼️")

    col1, col2 = st.columns([1, 2])

    with col1:
        img_prompt = st.text_area("Describe the image", "A futuristic cyberpunk city with neon lights, realistic, 8k", height=150)
        width = st.slider("Width", 256, 2048, 1024, step=64)
        height = st.slider("Height", 256, 2048, 1024, step=64)
        model = st.selectbox("Model", ["flux", "turbo", "stable-diffusion"])
        generate_btn = st.button("Generate Image", type="primary")

    with col2:
        if generate_btn:
            with st.spinner("Generating image..."):
                generated_img = image.generate_image(img_prompt, width, height, model)

                if generated_img:
                    st.image(generated_img, caption=img_prompt, use_container_width=True)

                    # Download Button
                    buf = io.BytesIO()
                    generated_img.save(buf, format="PNG")
                    byte_im = buf.getvalue()

                    st.download_button(
                        label="Download Image",
                        data=byte_im,
                        file_name="generated_image.png",
                        mime="image/png"
                    )
                else:
                    st.error("Failed to generate image. Please try again.")

# Music Mode
elif mode == "Music Generation 🎵":
    st.header("Generate Music 🎵")
    st.info("Note: Music generation can take a minute or two depending on the server load.")

    music_prompt = st.text_area("Describe the music", "Lo-fi hip hop beat with rain sounds", height=100)
    generate_music_btn = st.button("Generate Music", type="primary")

    if generate_music_btn:
        with st.spinner("Composing... (this might take a while)"):
            audio_path = music.generate_music(music_prompt)

            if audio_path:
                st.audio(audio_path)

                with open(audio_path, "rb") as f:
                    audio_bytes = f.read()

                st.download_button(
                    label="Download Music",
                    data=audio_bytes,
                    file_name="generated_music.mp3", # Usually mp3 or wav
                    mime="audio/mpeg"
                )
            else:
                st.error("Failed to generate music. The space might be busy.")

# Video Mode
elif mode == "Video Generation 🎥":
    st.header("Generate Video 🎥")
    st.info("Note: Video generation is computationally expensive and might take several minutes.")

    video_prompt = st.text_area("Describe the video", "A panda eating bamboo in a forest, high quality", height=100)
    generate_video_btn = st.button("Generate Video", type="primary")

    if generate_video_btn:
        with st.spinner("Rendering... (please wait)"):
            video_path = video.generate_video(video_prompt)

            if video_path:
                st.video(video_path)

                with open(video_path, "rb") as f:
                    video_bytes = f.read()

                st.download_button(
                    label="Download Video",
                    data=video_bytes,
                    file_name="generated_video.mp4",
                    mime="video/mp4"
                )
            else:
                st.error("Failed to generate video. The space might be busy.")
