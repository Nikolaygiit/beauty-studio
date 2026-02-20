import streamlit as st
import os
from dotenv import load_dotenv
from modules import text, image, music, video

# Load environment variables
load_dotenv()

st.set_page_config(page_title="Gemini Ultimate Bot", layout="wide")

# Sidebar
st.sidebar.title("Gemini Ultimate Bot")
mode = st.sidebar.radio("Select Mode", ["Text Chat", "Image Generation", "Music Generation", "Video Generation"])

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    st.sidebar.warning("Please set GOOGLE_API_KEY in .env file.")
    api_key = st.sidebar.text_input("Or enter Google API Key here", type="password")

hf_token = os.getenv("HF_TOKEN")
if not hf_token:
    st.sidebar.info("HF_TOKEN not found in .env. Using public access (may be rate limited).")
    hf_token = st.sidebar.text_input("Or enter Hugging Face Token (optional)", type="password")
    if hf_token == "":
        hf_token = None

if mode == "Text Chat":
    st.header("Chat with Gemini")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # User input
    if prompt := st.chat_input("What is up?"):
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)

        # Prepare history for Gemini (exclude current prompt, it's passed as argument)
        gemini_history = []
        for m in st.session_state.messages:
            role = "user" if m["role"] == "user" else "model"
            gemini_history.append({"role": role, "parts": [m["content"]]})

        # Generate response
        with st.spinner("Gemini is thinking..."):
            response_text, _ = text.generate_text(prompt, api_key, gemini_history)

        # Display assistant response
        with st.chat_message("assistant"):
            st.markdown(response_text)

        # Update session state
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.messages.append({"role": "assistant", "content": response_text})

elif mode == "Image Generation":
    st.header("Generate Images (Pollinations.ai)")
    prompt = st.text_input("Enter image description", placeholder="A futuristic city with flying cars")

    if st.button("Generate Image"):
        if not prompt:
            st.warning("Please enter a prompt.")
        else:
            with st.spinner("Generating image..."):
                img = image.generate_image(prompt)
                if img:
                    st.image(img, caption=prompt, use_column_width=True)
                else:
                    st.error("Failed to generate image. Try again.")

elif mode == "Music Generation":
    st.header("Generate Music (MusicGen)")
    prompt = st.text_input("Enter music description", placeholder="Lo-fi hip hop beat")
    duration = st.slider("Duration (seconds)", 5, 30, 10)

    if st.button("Generate Music"):
        if not prompt:
            st.warning("Please enter a prompt.")
        else:
            with st.spinner("Generating music (this may take a minute)..."):
                # Pass hf_token explicitly if user provided it in sidebar
                audio_path = music.generate_music(prompt, duration, hf_token)
                if audio_path:
                    st.audio(audio_path)
                    st.success(f"Generated: {audio_path}")
                else:
                    st.error("Failed to generate music. Hugging Face Space might be busy.")

elif mode == "Video Generation":
    st.header("Generate Video (Text-to-Video)")
    prompt = st.text_input("Enter video description", placeholder="A panda eating bamboo")

    if st.button("Generate Video"):
        if not prompt:
            st.warning("Please enter a prompt.")
        else:
            with st.spinner("Generating video (this may take a few minutes)..."):
                # Pass hf_token explicitly if user provided it in sidebar
                video_path = video.generate_video(prompt, hf_token)
                if video_path:
                    st.video(video_path)
                    st.success(f"Generated: {video_path}")
                else:
                    st.error("Failed to generate video. Hugging Face Space might be busy.")
