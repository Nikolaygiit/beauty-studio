import streamlit as st
import os
import sys

# Set page config first
st.set_page_config(page_title="Gemini Ultimate Bot", page_icon="🤖", layout="wide")

# Add current directory to path so imports work
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

try:
    from core import GeminiHandler
    import media
    from PIL import Image
except ImportError as e:
    st.error(f"Error importing modules: {e}. Please make sure you are running this from the gemini_bot directory or installed requirements.")
    st.stop()

st.title("🤖 Gemini Ultimate Bot")
st.markdown("### Your All-in-One AI Assistant")

# Sidebar for Configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    api_key = st.text_input("Google API Key", type="password", help="Get it from https://aistudio.google.com/")
    hf_token = st.text_input("HuggingFace Token (Optional)", type="password", help="Required for some advanced models")

    if api_key:
        os.environ["GOOGLE_API_KEY"] = api_key
    if hf_token:
        os.environ["HF_TOKEN"] = hf_token

    st.divider()
    st.markdown("**Capabilities:**")
    st.markdown("- 💬 **Chat**: Gemini 1.5 Flash (Text & Vision)")
    st.markdown("- 🖼️ **Image**: Pollinations.ai (Flux/SD)")
    st.markdown("- 🎵 **Music**: Facebook MusicGen")
    st.markdown("- 🎥 **Video**: ModelScope Text-to-Video")

    st.info("Built with Streamlit & Gemini")

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["💬 Chat", "🖼️ Generate Image", "🎵 Generate Music", "🎥 Generate Video"])

# --- Chat Tab ---
with tab1:
    st.header("Chat with Vision")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # File uploader
    with st.expander("📷 Upload Image for Analysis"):
        uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png", "webp"], key="chat_image_upload")
        image_input = None
        if uploaded_file:
            image_input = Image.open(uploaded_file)
            st.image(image_input, caption="Uploaded Image", width=300)

    # Chat Input
    if prompt := st.chat_input("Ask Gemini something..."):
        if not api_key and not os.getenv("GOOGLE_API_KEY"):
             st.warning("Please enter your Google API Key in the sidebar.")
        else:
            # Display user message
            with st.chat_message("user"):
                st.markdown(prompt)
                if image_input:
                     st.image(image_input, width=300)

            # Add to history
            st.session_state.messages.append({"role": "user", "content": prompt})

            # Generate response
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                full_response = ""
                with st.spinner("Gemini is thinking..."):
                    try:
                        # Re-instantiate to pick up new key if changed
                        # But wait, GeminiHandler init uses env var or arg.
                        gemini = GeminiHandler(api_key=api_key or os.getenv("GOOGLE_API_KEY"))

                        # Call API
                        response_text = gemini.generate_content(prompt, image=image_input)

                        message_placeholder.markdown(response_text)
                        full_response = response_text
                    except Exception as e:
                        error_msg = f"Error: {str(e)}"
                        message_placeholder.error(error_msg)
                        full_response = error_msg

            # Add assistant response to history
            st.session_state.messages.append({"role": "assistant", "content": full_response})

# --- Image Tab ---
with tab2:
    st.header("Text-to-Image Generation")
    col1, col2 = st.columns([3, 1])
    with col1:
        img_prompt = st.text_input("Describe the image you want to create", placeholder="A cyberpunk street in Tokyo at night, neon lights, rainy")
    with col2:
        generate_btn = st.button("Generate 🖼️", use_container_width=True)

    if generate_btn:
        if not img_prompt:
             st.warning("Please enter a prompt.")
        else:
            with st.spinner("Dreaming up your image..."):
                image_bytes = media.generate_image(img_prompt)
                if image_bytes:
                    st.image(image_bytes, caption=img_prompt, use_container_width=True)
                else:
                    st.error("Failed to generate image.")

# --- Music Tab ---
with tab3:
    st.header("Text-to-Music Generation")
    st.info("This uses HuggingFace Spaces (MusicGen). It might take a minute.")

    col1, col2 = st.columns([3, 1])
    with col1:
        music_prompt = st.text_input("Describe the music", placeholder="Upbeat pop song with synthwave vibes")
    with col2:
        duration = st.slider("Duration (seconds)", 5, 30, 10)

    if st.button("Generate 🎵", use_container_width=True):
        if not music_prompt:
            st.warning("Please enter a prompt.")
        else:
            with st.spinner("Composing..."):
                audio_path = media.generate_music(music_prompt, duration)
                if audio_path:
                    st.audio(audio_path)
                    st.success("Music generated successfully!")
                else:
                    st.error("Failed to generate music. Service might be busy.")

# --- Video Tab ---
with tab4:
    st.header("Text-to-Video Generation")
    st.info("This uses HuggingFace Spaces (ModelScope). It is very resource intensive.")

    video_prompt = st.text_input("Describe the video", placeholder="A cat playing piano")

    if st.button("Generate 🎥", use_container_width=True):
        if not video_prompt:
             st.warning("Please enter a prompt.")
        else:
            with st.spinner("Filming..."):
                video_path = media.generate_video(video_prompt)
                if video_path:
                    st.video(video_path)
                    st.success("Video generated successfully!")
                else:
                    st.error("Failed to generate video. Service might be busy.")
