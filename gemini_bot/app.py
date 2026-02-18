import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
import urllib.parse
from gradio_client import Client

# Load environment variables
load_dotenv()

# App configuration
st.set_page_config(page_title="Gemini Ultimate Bot", page_icon="🤖", layout="wide")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar for API Keys
with st.sidebar:
    st.title("⚙️ Settings")

    # Google API Key
    google_api_key = st.text_input("Google API Key", value=os.getenv("GOOGLE_API_KEY", ""), type="password")
    if not google_api_key:
        st.warning("Please enter your Google API Key to use the bot.")

    # Hugging Face Token (Optional)
    hf_token = st.text_input("Hugging Face Token (Optional)", value=os.getenv("HF_TOKEN", ""), type="password", help="Required for some private spaces or higher rate limits.")

    st.markdown("---")
    st.markdown("### About")
    st.markdown("This bot uses **Gemini 1.5 Flash** for text and chat, **Pollinations.ai** for images, and **Hugging Face Spaces** for music and video generation.")

# Main Interface with Tabs
tab_chat, tab_image, tab_music, tab_video = st.tabs(["💬 Chat", "🎨 Image", "🎵 Music", "🎥 Video"])

# --- CHAT TAB ---
with tab_chat:
    st.header("Chat with Gemini")

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("What is up?"):
        if not google_api_key:
            st.error("Please provide a Google API Key in the sidebar.")
        else:
            # Add user message to state
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            # Generate response
            try:
                genai.configure(api_key=google_api_key)
                model = genai.GenerativeModel("gemini-1.5-flash")

                # Prepare history for Gemini
                history = []
                for msg in st.session_state.messages:
                    role = "user" if msg["role"] == "user" else "model"
                    history.append({"role": role, "parts": [msg["content"]]})

                chat = model.start_chat(history=history[:-1]) # exclude last message which is the prompt
                response = chat.send_message(prompt)

                response_text = response.text

                # Add assistant message to state
                st.session_state.messages.append({"role": "assistant", "content": response_text})
                with st.chat_message("assistant"):
                    st.markdown(response_text)

            except Exception as e:
                st.error(f"An error occurred: {e}")
                st.session_state.messages.append({"role": "assistant", "content": f"An error occurred: {e}"})

# --- IMAGE TAB ---
with tab_image:
    st.header("Generate Images")

    image_prompt = st.text_input("Enter a prompt for the image:", "A futuristic city on Mars")

    if st.button("Generate Image"):
        if not image_prompt:
            st.warning("Please enter a prompt.")
        else:
            with st.spinner("Generating image..."):
                try:
                    encoded_prompt = urllib.parse.quote(image_prompt)
                    image_url = f"https://pollinations.ai/p/{encoded_prompt}"
                    st.image(image_url, caption=image_prompt, use_container_width=True)
                    st.success("Image generated successfully!")
                except Exception as e:
                    st.error(f"Failed to generate image: {e}")

# --- MUSIC TAB ---
with tab_music:
    st.header("Generate Music")
    music_prompt = st.text_input("Enter a prompt for the music:", "A Lo-Fi beat for studying")

    if st.button("Generate Music"):
        if not music_prompt:
            st.warning("Please enter a prompt.")
        else:
            with st.spinner("Generating music... (This may take a minute)"):
                try:
                    client = Client("facebook/MusicGen", hf_token=hf_token if hf_token else None)
                    result = client.predict(
                        music_prompt,	# str  in 'Describe your music' Textbox component
                        None,	# str (filepath or URL to file) in 'File' Audio component
                        api_name="/predict"
                    )
                    st.audio(result)
                    st.success("Music generated successfully!")
                except Exception as e:
                    st.error(f"Failed to generate music: {e}")
                    st.info("Tip: Try providing a Hugging Face Token in the sidebar if the space is gated.")

# --- VIDEO TAB ---
with tab_video:
    st.header("Generate Video")
    video_prompt = st.text_input("Enter a prompt for the video:", "A cute panda eating bamboo")

    if st.button("Generate Video"):
        if not video_prompt:
            st.warning("Please enter a prompt.")
        else:
            with st.spinner("Generating video... (This may take a minute)"):
                try:
                    client = Client("ali-vilab/modelscope-damo-text-to-video-synthesis", hf_token=hf_token if hf_token else None)
                    result = client.predict(
                        video_prompt,
                        api_name="/predict"
                    )
                    st.video(result)
                    st.success("Video generated successfully!")
                except Exception as e:
                    st.error(f"Failed to generate video: {e}")
                    st.info("Tip: Try providing a Hugging Face Token in the sidebar.")
