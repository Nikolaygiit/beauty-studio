import streamlit as st
import os
from dotenv import load_dotenv
from PIL import Image
import io

# Import our modules
# Note: When running with `streamlit run app.py`, the import path needs to be relative or absolute based on where it's run.
# If running from inside `gemini_bot`, imports should be `modules.text`.
try:
    from modules.text import GeminiHandler
    from modules.image import generate_image
    from modules.media import generate_music, generate_video
except ImportError:
    # Fallback if running from root
    from gemini_bot.modules.text import GeminiHandler
    from gemini_bot.modules.image import generate_image
    from gemini_bot.modules.media import generate_music, generate_video

# Load environment variables
load_dotenv()

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
    .stApp header {
        background-color: transparent;
    }
    .stButton>button {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.title("🤖 Gemini Ultimate")

    # API Key Handling
    if not os.getenv("GOOGLE_API_KEY"):
        api_key = st.text_input("Enter Google API Key", type="password")
        if api_key:
            os.environ["GOOGLE_API_KEY"] = api_key
            st.success("API Key set! Please reload to initialize.")

    mode = st.radio("Select Mode", ["Chat", "Image Generator", "Music Generator", "Video Generator"])

    st.markdown("---")
    st.markdown("### Settings")
    model_name = st.selectbox("Model", ["gemini-1.5-flash", "gemini-1.5-pro"], index=0)

    # Reset Chat Button
    if mode == "Chat":
        if st.button("New Chat"):
            if "handler" in st.session_state:
                st.session_state.chat_session = st.session_state.handler.start_chat()
            st.session_state.messages = []
            st.rerun()

    st.markdown("---")
    st.caption("Powered by Google Gemini, Pollinations.ai & HuggingFace")

# --- CHAT MODE ---
if mode == "Chat":
    st.header("💬 Chat with Gemini")

    # Image Upload for Vision
    with st.expander("🖼️ Upload Image for Analysis"):
        uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg", "webp"])
        image_content = None
        if uploaded_file:
            image_content = Image.open(uploaded_file)
            st.image(image_content, caption="Uploaded Image", width=300)

    # Initialize Chat Session
    if "handler" not in st.session_state or st.session_state.handler.model_name != model_name:
        try:
            st.session_state.handler = GeminiHandler(model_name=model_name)
            # If we switch models, we might want to keep history or reset.
            # Resetting is safer for now as history objects are tied to model instances usually.
            st.session_state.chat_session = st.session_state.handler.start_chat()
            st.session_state.messages = []
        except Exception as e:
            st.error(f"Please set a valid GOOGLE_API_KEY in the sidebar.")
            st.stop()

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display Chat History
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            if "image" in message and message["image"]:
                st.image(message["image"], width=300)
            st.markdown(message["content"])

    # Chat Input
    if prompt := st.chat_input("What is on your mind?"):
        # Prepare content for display
        display_content = prompt

        # Add user message to history
        msg_entry = {"role": "user", "content": prompt}
        if image_content:
            msg_entry["image"] = image_content
            # Convert image to compatible format for Gemini if needed,
            # but GeminiHandler expects PIL Image which we have.

        st.session_state.messages.append(msg_entry)

        with st.chat_message("user"):
            if image_content:
                st.image(image_content, width=300)
            st.markdown(prompt)

        # Generate Response
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""

            with st.spinner("Thinking..."):
                try:
                    # Prepare input for Gemini
                    if image_content:
                        input_content = [prompt, image_content]
                    else:
                        input_content = prompt

                    response = st.session_state.handler.send_message(input_content, stream=True)

                    # Stream response
                    for chunk in response:
                        if chunk.text:
                            full_response += chunk.text
                            message_placeholder.markdown(full_response + "▌")
                    message_placeholder.markdown(full_response)

                    st.session_state.messages.append({"role": "assistant", "content": full_response})

                except Exception as e:
                    st.error(f"Error: {str(e)}")

# --- IMAGE MODE ---
elif mode == "Image Generator":
    st.header("🎨 Image Generator")
    st.caption("Powered by Pollinations.ai")

    col1, col2 = st.columns([1, 2])

    with col1:
        img_prompt = st.text_area("Describe the image", height=150, placeholder="A futuristic city with flying cars, cyberpunk style...")
        width = st.slider("Width", 256, 2048, 1024, step=64)
        height = st.slider("Height", 256, 2048, 1024, step=64)
        seed = st.number_input("Seed (Optional)", value=0, help="Set to 0 for random")
        model_type = st.selectbox("Style Model", ["flux", "turbo"], index=0)
        generate_btn = st.button("Generate Image", type="primary")

    with col2:
        if generate_btn and img_prompt:
            with st.spinner("Generating image..."):
                # Use random seed if 0
                actual_seed = seed if seed != 0 else None
                img_data = generate_image(img_prompt, width=width, height=height, seed=actual_seed, model=model_type)

                if img_data:
                    st.image(img_data, caption=img_prompt, use_column_width=True)
                    # Download button
                    st.download_button(
                        label="Download Image",
                        data=img_data,
                        file_name="generated_image.jpg",
                        mime="image/jpeg"
                    )
                else:
                    st.error("Failed to generate image. Please try again.")

# --- MUSIC MODE ---
elif mode == "Music Generator":
    st.header("🎵 Music Generator")
    st.caption("Powered by Facebook MusicGen via Hugging Face")

    music_prompt = st.text_input("Describe the music style/mood", placeholder="Lo-fi hip hop beat, chill, relaxing")
    duration = st.slider("Duration (seconds)", 5, 30, 10)

    if st.button("Generate Music", type="primary"):
        if music_prompt:
            with st.spinner("Composing music... (This may take a minute)"):
                audio_path = generate_music(music_prompt, duration)
                if audio_path:
                    # Gradio client returns a tuple sometimes? Let's handle it.
                    if isinstance(audio_path, tuple):
                        audio_path = audio_path[1] # usually path is second element if first is sr

                    # Sometimes it returns a directory or list.
                    # Let's rely on st.audio trying to play it.
                    try:
                        st.audio(audio_path)
                        st.success("Music generated!")

                        # Read file for download
                        with open(audio_path, "rb") as f:
                             audio_bytes = f.read()
                        st.download_button(
                             label="Download Audio",
                             data=audio_bytes,
                             file_name="generated_music.mp4", # MusicGen often outputs mp4 or wav
                             mime="audio/mp4"
                        )
                    except Exception as e:
                        st.error(f"Could not load audio file: {e}")
                        st.write(f"Debug path: {audio_path}")
                else:
                    st.error("Failed to generate music. Service might be busy.")

# --- VIDEO MODE ---
elif mode == "Video Generator":
    st.header("🎥 Video Generator")
    st.caption("Powered by ModelScope via Hugging Face")

    video_prompt = st.text_input("Describe the video scene", placeholder="A panda eating bamboo in a forest")

    if st.button("Generate Video", type="primary"):
        if video_prompt:
            with st.spinner("Rendering video... (This takes time, usually 1-2 mins)"):
                video_path = generate_video(video_prompt)
                if video_path:
                     # Check if path is valid
                    try:
                        st.video(video_path)
                        st.success("Video generated!")

                        with open(video_path, "rb") as f:
                             video_bytes = f.read()
                        st.download_button(
                             label="Download Video",
                             data=video_bytes,
                             file_name="generated_video.mp4",
                             mime="video/mp4"
                        )
                    except Exception as e:
                        st.error(f"Could not load video file: {e}")
                        st.write(f"Debug path: {video_path}")
                else:
                    st.error("Failed to generate video. Service might be busy.")
