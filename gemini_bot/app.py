import streamlit as st
import os

# Import modules
from modules.text import handle_chat_session, configure_genai
from modules.image import handle_image_generation
from modules.music import handle_music_generation
from modules.video import handle_video_generation

# Page Configuration
st.set_page_config(
    page_title="Gemini Ultimate Bot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

def main():
    st.title("🤖 Gemini Ultimate Bot")
    st.markdown("""
    Welcome to the ultimate AI assistant powered by Gemini and other state-of-the-art models.
    Generate text, images, music, and videos all in one place!
    """)

    # Sidebar
    st.sidebar.title("Configuration")

    # API Key Input
    api_key = st.sidebar.text_input("Enter Google API Key", type="password")
    if api_key:
        os.environ["GOOGLE_API_KEY"] = api_key
        configure_genai(api_key)
    else:
        st.sidebar.warning("Please enter your Google API Key to use text generation features.")

    # Navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Chat & Text", "Image Generation", "Music Generation", "Video Generation"])

    # Clear Chat History Button (Global)
    if st.sidebar.button("Clear Chat History"):
        if "messages" in st.session_state:
            st.session_state.messages = []
        st.sidebar.success("Chat history cleared!")

    # Page Routing
    if page == "Chat & Text":
        if api_key:
            handle_chat_session()
        else:
            st.info("Please enter your Google API Key in the sidebar to start chatting.")

    elif page == "Image Generation":
        handle_image_generation()

    elif page == "Music Generation":
        handle_music_generation()

    elif page == "Video Generation":
        handle_video_generation()

    # Footer
    st.sidebar.markdown("---")
    st.sidebar.markdown("Made with ❤️ by Jules")

if __name__ == "__main__":
    main()
