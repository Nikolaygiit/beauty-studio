import streamlit as st
from modules.routing import get_route
from modules.text import create_client, create_chat_session
from modules.image import generate_image
from modules.music import generate_music
from modules.video import generate_video

def main():
    st.set_page_config(page_title="Gemini Ultimate Bot", page_icon="✨", layout="wide")
    st.title("Gemini Ultimate Bot ✨")

    # Sidebar
    st.sidebar.title("Настройки")
    api_key = st.sidebar.text_input("Введите GOOGLE_API_KEY", type="password")

    # Initialize session state for history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Check if API key changed
    if "current_api_key" not in st.session_state or st.session_state.current_api_key != api_key:
        st.session_state.current_api_key = api_key
        # Reset chat session if API key changes
        if "chat_session" in st.session_state:
            del st.session_state.chat_session
        if "gemini_client" in st.session_state:
            del st.session_state.gemini_client

    # Initialize or retrieve Gemini chat session
    if api_key:
        if "gemini_client" not in st.session_state or "chat_session" not in st.session_state:
             try:
                 client = create_client(api_key)
                 st.session_state.gemini_client = client
                 st.session_state.chat_session = create_chat_session(client, history=None)
             except Exception as e:
                 st.sidebar.error(f"Ошибка инициализации Gemini: {e}")
    else:
        st.sidebar.warning("Пожалуйста, введите GOOGLE_API_KEY для текстовых ответов.")

    # Clear history button
    if st.sidebar.button("Очистить историю чата"):
        st.session_state.chat_history = []
        if "chat_session" in st.session_state:
             del st.session_state.chat_session
        if "gemini_client" in st.session_state:
             del st.session_state.gemini_client
        st.rerun()

    # Display chat history
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            if message["type"] == "text":
                st.markdown(message["content"])
            elif message["type"] == "image":
                st.image(message["content"])
            elif message["type"] == "audio":
                st.audio(message["content"])
            elif message["type"] == "video":
                st.video(message["content"])

    # Input area
    prompt = st.chat_input("Введите ваш запрос...")

    if prompt:
        # Display user prompt
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.chat_history.append({"role": "user", "type": "text", "content": prompt})

        # Route the request
        route = get_route(prompt)

        with st.chat_message("assistant"):
            if route == "image":
                with st.spinner("Генерация изображения..."):
                    url, err = generate_image(prompt)
                    if err:
                        st.error(err)
                        st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": f"Ошибка: {err}"})
                    elif url:
                        st.image(url)
                        st.session_state.chat_history.append({"role": "assistant", "type": "image", "content": url})

            elif route == "music":
                with st.spinner("Генерация музыки..."):
                    audio_path, err = generate_music(prompt)
                    if err:
                        st.error(err)
                        st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": f"Ошибка: {err}"})
                    elif audio_path:
                        st.audio(audio_path)
                        st.session_state.chat_history.append({"role": "assistant", "type": "audio", "content": audio_path})

            elif route == "video":
                with st.spinner("Генерация видео..."):
                    video_path, err = generate_video(prompt)
                    if err:
                        st.error(err)
                        st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": f"Ошибка: {err}"})
                    elif video_path:
                        st.video(video_path)
                        st.session_state.chat_history.append({"role": "assistant", "type": "video", "content": video_path})

            else: # text route
                if "chat_session" not in st.session_state:
                     st.error("Пожалуйста, введите GOOGLE_API_KEY в боковой панели.")
                     st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": "Ошибка: GOOGLE_API_KEY не установлен."})
                else:
                     with st.spinner("Думаю..."):
                         try:
                             response = st.session_state.chat_session.send_message_stream(prompt)
                             # Create a placeholder to display the streamed response
                             response_placeholder = st.empty()
                             full_response = ""

                             for chunk in response:
                                 if chunk.text:
                                     full_response += chunk.text
                                     response_placeholder.markdown(full_response + "▌")

                             response_placeholder.markdown(full_response)
                             st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": full_response})
                         except Exception as e:
                             error_msg = f"Ошибка генерации текста: {str(e)}"
                             st.error(error_msg)
                             st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": error_msg})

if __name__ == "__main__":
    main()
