import streamlit as st
import os
import sys

# Ensure modules can be imported
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from modules import text, image, music, video

st.set_page_config(page_title="Gemini Ultimate Bot", page_icon="🤖", layout="wide")

st.title("🤖 Gemini Ultimate Bot")
st.caption("All-in-one AI Assistant: Text, Image, Music, Video")

# Sidebar
with st.sidebar:
    st.header("Configuration")
    api_key = st.text_input("Google API Key", type="password", help="Get your API key from Google AI Studio")
    if api_key:
        os.environ["GOOGLE_API_KEY"] = api_key
        text.configure_api(api_key)
        st.success("API Key set!")

    st.markdown("---")
    st.markdown("### Capabilities")
    st.markdown("- **Text**: Gemini 1.5 Flash")
    st.markdown("- **Image**: Pollinations.ai")
    st.markdown("- **Music**: MusicGen")
    st.markdown("- **Video**: ModelScope")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "image_url" in message:
            st.image(message["image_url"])
        if "audio_path" in message:
            st.audio(message["audio_path"])
        if "video_path" in message:
            st.video(message["video_path"])

# Chat input
if prompt := st.chat_input("What can I do for you today?"):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Determine intent
    intent = "text"
    clean_prompt = prompt.lower()

    # Simple keyword detection
    if any(keyword in clean_prompt for keyword in ["draw", "generate image", "create image", "photo of", "picture of"]):
        intent = "image"
    elif any(keyword in clean_prompt for keyword in ["generate music", "make music", "compose music", "song about", "melody"]):
        intent = "music"
    elif any(keyword in clean_prompt for keyword in ["generate video", "create video", "movie of", "clip of"]):
        intent = "video"

    # Generate response
    with st.chat_message("assistant"):
        if intent == "text":
            if not api_key:
                st.warning("Please set your Google API Key in the sidebar to use text chat.")
                st.markdown("You can still use Image, Music, and Video generation without an API Key if configured.")
                # Fallback to just warning but maybe allow other mods if they don't need key?
                # Pollinations doesn't need key. Gradio spaces might not need key (free tier).
                # But typically text is the default fallback.
            else:
                try:
                    stream = text.generate_response(prompt, history=st.session_state.messages)
                    response = st.write_stream(stream)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                except Exception as e:
                    st.error(f"An error occurred: {e}")

        elif intent == "image":
            with st.spinner("Generating image..."):
                try:
                    image_url = image.generate_image(prompt)
                    st.image(image_url)
                    st.markdown(f"**Image generated for:** {prompt}")
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": f"Here is the image for: {prompt}",
                        "image_url": image_url
                    })
                except Exception as e:
                    st.error(f"Failed to generate image: {e}")

        elif intent == "music":
            with st.spinner("Generating music... (this might take a minute)"):
                try:
                    music_path = music.generate_music(prompt)
                    if "Error" in str(music_path):
                        st.error(music_path)
                    else:
                        st.audio(music_path)
                        st.markdown(f"**Music generated for:** {prompt}")
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": f"Here is the music for: {prompt}",
                            "audio_path": music_path
                        })
                except Exception as e:
                    st.error(f"Failed to generate music: {e}")

        elif intent == "video":
            with st.spinner("Generating video... (this might take a few minutes)"):
                try:
                    video_path = video.generate_video(prompt)
                    if "Error" in str(video_path):
                        st.error(video_path)
                    else:
                        st.video(video_path)
                        st.markdown(f"**Video generated for:** {prompt}")
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": f"Here is the video for: {prompt}",
                            "video_path": video_path
                        })
                except Exception as e:
                    st.error(f"Failed to generate video: {e}")
