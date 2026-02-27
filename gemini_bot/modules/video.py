import streamlit as st
from gradio_client import Client

@st.cache_resource
def get_video_client():
    return Client("damo-vilab/modelscope-text-to-video-synthesis")

def handle_video_generation():
    st.header("Video Generation")
    prompt = st.text_input("Enter a prompt for the video:", "A panda eating bamboo")

    if st.button("Generate Video"):
        if prompt:
            try:
                with st.spinner("Generating video... (this takes several minutes)"):
                    client = get_video_client()
                    result = client.predict(
                        prompt,	# str  in 'Input Text' Textbox component
                        -1,	# float  in 'Seed' Number component
                        16,	# float  in 'Number of frames' Number component
                        25,	# float  in 'Number of inference steps' Number component
                        fn_index=0
                    )
                    # result is typically the path to the video file.
                    if result:
                        st.video(result)

            except Exception as e:
                st.error(f"Error generating video: {e}")
        else:
            st.warning("Please enter a prompt.")
