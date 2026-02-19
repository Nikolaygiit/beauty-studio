import streamlit as st
import google.generativeai as genai
import os
import requests
from PIL import Image
from io import BytesIO
from dotenv import load_dotenv
from gradio_client import Client

# Load environment variables
load_dotenv()

# Configure Gemini
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)

# App Title
st.set_page_config(page_title="Gemini Ultimate Bot", page_icon="🤖", layout="wide")
st.title("🤖 Gemini Ultimate Bot")

# Sidebar for configuration
with st.sidebar:
    st.header("Settings")
    api_key_input = st.text_input("Google API Key", type="password", value=GOOGLE_API_KEY if GOOGLE_API_KEY else "")
    if api_key_input:
        genai.configure(api_key=api_key_input)

    st.markdown("---")
    st.markdown("### About")
    st.markdown("This bot uses:")
    st.markdown("- **Gemini 1.5 Flash** for Text")
    st.markdown("- **Pollinations.ai** for Images")
    st.markdown("- **MusicGen** for Music")
    st.markdown("- **ModelScope** for Video")

# Tabs for different functionalities
tab1, tab2, tab3, tab4 = st.tabs(["📝 Text Generation", "🎨 Image Generation", "🎵 Music Generation", "🎥 Video Generation"])

# Text Generation
with tab1:
    st.header("Text Generation with Gemini 1.5 Flash")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask me anything..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            try:
                # Prepare history for Gemini
                gemini_history = []
                for msg in st.session_state.messages[:-1]: # Exclude the last new message which we will send
                    role = "user" if msg["role"] == "user" else "model"
                    gemini_history.append({"role": role, "parts": [msg["content"]]})

                model = genai.GenerativeModel('gemini-1.5-flash')
                chat = model.start_chat(history=gemini_history)
                response = chat.send_message(prompt)

                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Error generating text: {e}")

# Image Generation
with tab2:
    st.header("Image Generation with Pollinations.ai")

    image_prompt = st.text_input("Enter a prompt for the image:", "A futuristic cityscape at sunset")

    if st.button("Generate Image"):
        if image_prompt:
            with st.spinner("Generating image..."):
                try:
                    # Pollinations.ai API
                    url = f"https://image.pollinations.ai/prompt/{image_prompt}"
                    response = requests.get(url)

                    if response.status_code == 200:
                        image = Image.open(BytesIO(response.content))
                        st.image(image, caption=image_prompt, use_column_width=True)

                        # Download button
                        buf = BytesIO()
                        image.save(buf, format="PNG")
                        byte_im = buf.getvalue()
                        st.download_button(
                            label="Download Image",
                            data=byte_im,
                            file_name="generated_image.png",
                            mime="image/png",
                        )
                    else:
                        st.error(f"Error generating image: {response.status_code}")
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.warning("Please enter a prompt.")

# Music Generation
with tab3:
    st.header("Music Generation with MusicGen")
    music_prompt = st.text_input("Enter a prompt for music:", "Lo-fi hip hop beat")

    if st.button("Generate Music"):
        if music_prompt:
            with st.spinner("Generating music... (this may take a minute)"):
                try:
                    # Attempt to connect to MusicGen space
                    client = Client("facebook/MusicGen")
                    # Note: API signature might change. This is a best-effort guess based on standard MusicGen spaces.
                    # Usually it returns a path to the generated audio file.
                    result = client.predict(
                        music_prompt,
                        None, # Optional audio file input
                        fn_index=0
                    )
                    # Result inspection (handling different return formats)
                    if isinstance(result, tuple):
                         # Often returns (video_path, audio_path) or similar
                         audio_path = result[1] if len(result) > 1 else result[0]
                    else:
                        audio_path = result

                    st.audio(audio_path)
                    st.success("Music generated successfully!")

                except Exception as e:
                    st.error(f"Error generating music: {e}")
                    st.warning("Note: This feature relies on the 'facebook/MusicGen' Hugging Face Space. If you see a queue error or timeout, the space is likely busy. Try again later or use a private space.")
        else:
            st.warning("Please enter a prompt.")

# Video Generation
with tab4:
    st.header("Video Generation with ModelScope")
    video_prompt = st.text_input("Enter a prompt for video:", "A panda eating bamboo")

    if st.button("Generate Video"):
        if video_prompt:
            with st.spinner("Generating video... (this may take a few minutes)"):
                try:
                    # Attempt to connect to ModelScope space
                    client = Client("damo-vilab/modelscope-damo-text-to-video-synthesis")
                    result = client.predict(
                        video_prompt,
                        fn_index=0
                    )
                    st.video(result)
                    st.success("Video generated successfully!")

                except Exception as e:
                    st.error(f"Error generating video: {e}")
                    st.warning("Note: This feature relies on the 'damo-vilab/modelscope-damo-text-to-video-synthesis' Hugging Face Space. If you see a queue error or timeout, the space is likely busy. Try again later or use a private space.")
        else:
            st.warning("Please enter a prompt.")
