import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
from PIL import Image
import requests
from io import BytesIO
from gradio_client import Client

# Load environment variables
load_dotenv()

# Page Config
st.set_page_config(
    page_title="Gemini Ultimate Bot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Sidebar for Configuration
with st.sidebar:
    st.title("⚙️ Settings")

    # API Keys
    google_api_key = st.text_input("Google API Key", value=os.getenv("GOOGLE_API_KEY", ""), type="password")
    hf_token = st.text_input("Hugging Face Token (Optional)", value=os.getenv("HF_TOKEN", ""), type="password", help="Required for some Spaces if they are gated or if you want to skip queues.")

    st.markdown("---")
    st.markdown("### About")
    st.markdown("This bot uses **Gemini 1.5 Flash** for text/vision, **Pollinations.ai** for images, and **Hugging Face Spaces** for music and video.")
    st.info("Note: Music and Video generation rely on public Hugging Face Spaces which may be busy or require a token.")

# Main Interface
st.title("🤖 Gemini Ultimate Bot")
st.markdown("All-in-one AI Assistant for Text, Images, Music, and Video.")

# Tabs
tab_chat, tab_image, tab_music, tab_video = st.tabs(["💬 Chat", "🖼️ Image", "🎵 Music", "🎥 Video"])

# --- Chat Tab ---
with tab_chat:
    st.header("Chat with Gemini")

    if not google_api_key:
        st.warning("Please enter your Google API Key in the sidebar to use the chat.")
    else:
        # Configure Gemini
        genai.configure(api_key=google_api_key)

        # Initialize Chat Session
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []

        # Display Chat History
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                if "image" in message:
                    st.image(message["image"])

        # Chat Input
        prompt = st.chat_input("Ask something or describe an image...")
        uploaded_file = st.file_uploader("Upload an image (optional)", type=["jpg", "jpeg", "png"], key="chat_image_upload")

        if prompt:
            # User Message
            user_msg = {"role": "user", "content": prompt}

            # Use a separate container to display the new message immediately
            with st.chat_message("user"):
                st.markdown(prompt)
                if uploaded_file:
                    image = Image.open(uploaded_file)
                    st.image(image)
                    user_msg["image"] = image

            # Add to history
            st.session_state.chat_history.append(user_msg)

            # Generate Response
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    try:
                        model = genai.GenerativeModel('gemini-1.5-flash')

                        if uploaded_file:
                             # For single turn vision chat, history management is tricky with the API as it expects text/parts.
                             # Simple approach: Just send the current prompt and image.
                             response = model.generate_content([prompt, user_msg["image"]])
                             bot_reply = response.text
                        else:
                            # Re-construct history for context
                            history_for_model = []
                            for msg in st.session_state.chat_history[:-1]: # Exclude current prompt (already handled)
                                role = "user" if msg["role"] == "user" else "model"
                                parts = [msg["content"]]
                                if "image" in msg:
                                    parts.append(msg["image"])
                                history_for_model.append({"role": role, "parts": parts})

                            chat = model.start_chat(history=history_for_model)
                            response = chat.send_message(prompt)
                            bot_reply = response.text

                        st.markdown(bot_reply)
                        st.session_state.chat_history.append({"role": "assistant", "content": bot_reply})

                    except Exception as e:
                        error_msg = f"Error: {str(e)}"
                        st.error(error_msg)
                        st.session_state.chat_history.append({"role": "assistant", "content": error_msg})

# --- Image Tab ---
with tab_image:
    st.header("Generate Images")
    st.markdown("Powered by **Pollinations.ai**")

    img_prompt = st.text_area("Enter prompt for image generation", "A futuristic city with flying cars, cyberpunk style")

    if st.button("Generate Image"):
        if not img_prompt:
            st.error("Please enter a prompt.")
        else:
            with st.spinner("Generating image..."):
                try:
                    # Clean prompt for URL
                    safe_prompt = requests.utils.quote(img_prompt)
                    url = f"https://image.pollinations.ai/prompt/{safe_prompt}"

                    # Fetch image to ensure it loads
                    response = requests.get(url)
                    if response.status_code == 200:
                        image = Image.open(BytesIO(response.content))
                        st.image(image, caption=img_prompt, use_column_width=True)

                        # Download button
                        buf = BytesIO()
                        image.save(buf, format="PNG")
                        st.download_button("Download Image", data=buf.getvalue(), file_name="generated_image.png", mime="image/png")
                    else:
                        st.error(f"Failed to generate image. Status code: {response.status_code}")
                except Exception as e:
                    st.error(f"Error: {str(e)}")

# --- Music Tab ---
with tab_music:
    st.header("Generate Music")
    st.markdown("Powered by **MusicGen** (via Hugging Face Spaces)")

    music_prompt = st.text_input("Describe the music", "Lo-fi hip hop beat, relaxing")
    duration = st.slider("Duration (seconds)", 5, 30, 10)

    if st.button("Generate Music"):
        with st.spinner("Generating music... (This may take a while)"):
            try:
                client_args = {}
                if hf_token:
                    client_args['hf_token'] = hf_token

                # Try connecting
                client = Client("facebook/MusicGen", **client_args)
                result = client.predict(
                    music_prompt,	# str  in 'Describe your music' Textbox component
                    None,	# str (filepath or URL to file) in 'File' Audio component
                    duration,	# float  in 'Duration' Slider component
                    api_name="/predict"
                )

                # Handle result
                if isinstance(result, tuple):
                    # (sample_rate, filepath) or (sample_rate, data)
                    st.audio(result[1], sample_rate=result[0])
                elif isinstance(result, str):
                    st.audio(result)
                else:
                    st.write("Result:", result)

            except Exception as e:
                st.error(f"Error: {str(e)}. Try adding a Hugging Face Token in the settings or check if the space is busy.")

# --- Video Tab ---
with tab_video:
    st.header("Generate Video")
    st.markdown("Powered by **ModelScope Text-to-Video** (via Hugging Face Spaces)")

    video_prompt = st.text_input("Describe the video", "A panda eating bamboo in a forest")

    if st.button("Generate Video"):
         with st.spinner("Generating video... (This may take a while and requires a powerful space)"):
            try:
                client_args = {}
                if hf_token:
                    client_args['hf_token'] = hf_token

                client = Client("damo-vilab/modelscope-damo-text-to-video-synthesis", **client_args)
                result = client.predict(
                    video_prompt,	# str  in 'Prompt' Textbox component
                    -1,	# float  in 'Seed' Number component
                    16,	# float  in 'Number of frames' Number component
                    25,	# float  in 'Number of inference steps' Number component
                    api_name="/predict"
                )

                if isinstance(result, str):
                    st.video(result)
                else:
                     st.write("Result:", result)

            except Exception as e:
                st.error(f"Error: {str(e)}. This space might be busy or private. Try adding a Hugging Face Token.")
