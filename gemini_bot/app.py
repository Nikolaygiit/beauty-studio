import streamlit as st
import os
from modules.text import GeminiText
from modules.image import ImageGenerator
from modules.music import MusicGenerator
from modules.video import VideoGenerator

# Page Config
st.set_page_config(page_title="Gemini Ultimate Bot", layout="wide")

# Title
st.title("🤖 Gemini Ultimate Bot")

# Sidebar
with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("Google API Key", type="password")

    st.markdown("---")
    st.header("Mode")
    mode = st.radio("Select Generation Mode", ["Text/Chat", "Image", "Music", "Video"])

    st.markdown("---")
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        if 'gemini_chat' in st.session_state and st.session_state.gemini_chat:
            st.session_state.gemini_chat.chat = st.session_state.gemini_chat.model.start_chat(history=[])
        st.rerun()

# Initialize Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

if "gemini_chat" not in st.session_state:
    st.session_state.gemini_chat = None

# Initialize Modules
@st.cache_resource
def get_image_generator():
    return ImageGenerator()

@st.cache_resource
def get_music_generator():
    return MusicGenerator()

@st.cache_resource
def get_video_generator():
    return VideoGenerator()

image_gen = get_image_generator()
music_gen = get_music_generator()
video_gen = get_video_generator()

# Initialize Gemini Chat
if api_key:
    if st.session_state.gemini_chat is None or st.session_state.gemini_chat.api_key != api_key:
        st.session_state.gemini_chat = GeminiText(api_key)

# Chat Interface
# Display history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["type"] == "text":
            st.markdown(message["content"])
        elif message["type"] == "image":
            st.image(message["content"])
        elif message["type"] == "audio":
            st.audio(message["content"])
        elif message["type"] == "video":
            st.video(message["content"])

# User Input
if prompt := st.chat_input("What would you like to generate?"):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "type": "text", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Handle Request based on Mode
    if mode == "Text/Chat":
        if not api_key:
            st.error("Please enter your Google API Key in the sidebar.")
        else:
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                full_response = ""
                try:
                    response = st.session_state.gemini_chat.send_message(prompt)
                    # Check if response is a string (error) or a generation object
                    if isinstance(response, str):
                         message_placeholder.markdown(response)
                         full_response = response
                    else:
                        # Assuming response is a generation object with chunks
                        # Verify if response is iterable for streaming
                        if hasattr(response, '__iter__'):
                            for chunk in response:
                                try:
                                    if chunk.text:
                                        full_response += chunk.text
                                        message_placeholder.markdown(full_response + "▌")
                                except ValueError:
                                    # Handle cases where safety filters block the response
                                    continue
                            message_placeholder.markdown(full_response)
                        else:
                            # Not streaming or single response
                            full_response = response.text
                            message_placeholder.markdown(full_response)

                    st.session_state.messages.append({"role": "assistant", "type": "text", "content": full_response})
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")

    elif mode == "Image":
        with st.chat_message("assistant"):
            st.markdown("Generating image...")
            try:
                image_url = image_gen.generate_image(prompt)
                st.image(image_url)
                st.session_state.messages.append({"role": "assistant", "type": "image", "content": image_url})
            except Exception as e:
                st.error(f"Error generating image: {e}")

    elif mode == "Music":
        with st.chat_message("assistant"):
            st.markdown("Generating music... (this may take a while)")
            try:
                result = music_gen.generate_music(prompt)

                # Check for error
                if isinstance(result, tuple) and result[0] is None:
                     st.error(result[1])
                else:
                    # Gradio predict usually returns path for file output
                    audio_path = result
                    if isinstance(result, tuple):
                        # Some spaces return (sample_rate, data) or (path, metadata)
                        # We need to be robust.
                        # musicgen-streaming often returns a filepath.
                        # Let's assume filepath is the first element if tuple.
                         audio_path = result[0] if isinstance(result[0], str) else result

                    st.audio(audio_path)
                    st.session_state.messages.append({"role": "assistant", "type": "audio", "content": audio_path})
            except Exception as e:
                st.error(f"Error generating music: {e}")

    elif mode == "Video":
        with st.chat_message("assistant"):
            st.markdown("Generating video... (this may take a while)")
            try:
                result = video_gen.generate_video(prompt)
                if isinstance(result, tuple) and result[0] is None:
                     st.error(result[1])
                else:
                    video_path = result
                    if isinstance(result, tuple):
                         video_path = result[0] if isinstance(result[0], str) else result

                    st.video(video_path)
                    st.session_state.messages.append({"role": "assistant", "type": "video", "content": video_path})
            except Exception as e:
                st.error(f"Error generating video: {e}")
