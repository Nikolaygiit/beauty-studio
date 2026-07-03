import streamlit as st

# Setup page config
st.set_page_config(page_title="Gemini Ultimate Bot", page_icon="🤖", layout="wide")

from modules.routing import get_route, ROUTE_IMAGE, ROUTE_MUSIC, ROUTE_VIDEO, ROUTE_TEXT
from modules.text import get_gemini_client, get_chat_config
from modules.image import generate_image
from modules.music import generate_music
from modules.video import generate_video

def init_session_state():
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "chat_session" not in st.session_state:
        st.session_state.chat_session = None
    if "gemini_client" not in st.session_state:
        st.session_state.gemini_client = None
    if "current_api_key" not in st.session_state:
        st.session_state.current_api_key = ""

def clear_chat_history():
    st.session_state.chat_history = []
    st.session_state.chat_session = None
    # Re-init chat session if we have a client
    if st.session_state.gemini_client:
        st.session_state.chat_session = st.session_state.gemini_client.chats.create(
            model="gemini-2.0-flash",
            config=get_chat_config()
        )

def main():
    st.title("🤖 Gemini Ultimate Bot")
    st.markdown("Генерация текста, изображений, музыки и видео на базе Gemini и ИИ моделей.")

    init_session_state()

    # Sidebar
    with st.sidebar:
        st.header("Настройки")
        api_key = st.text_input("Google API Key", type="password", help="Введите ваш Gemini API ключ")

        # If API key changed, re-init client
        if api_key != st.session_state.current_api_key:
            st.session_state.current_api_key = api_key
            if api_key:
                client, err = get_gemini_client(api_key)
                if err:
                    st.error(err)
                    st.session_state.gemini_client = None
                    st.session_state.chat_session = None
                else:
                    st.session_state.gemini_client = client
                    st.session_state.chat_session = client.chats.create(
                        model="gemini-2.0-flash",
                        config=get_chat_config()
                    )
                    st.success("API ключ успешно применен!")

        if st.button("Очистить историю чата"):
            clear_chat_history()
            st.rerun()

    # Display chat history
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            if msg["type"] == "text":
                st.markdown(msg["content"])
            elif msg["type"] == "image":
                st.markdown(msg["content"]) # Text prompt
                if msg.get("media_path"):
                    st.image(msg["media_path"])
                elif msg.get("error"):
                    st.error(msg["error"])
            elif msg["type"] == "music":
                st.markdown(msg["content"])
                if msg.get("media_path"):
                    st.audio(msg["media_path"])
                elif msg.get("error"):
                    st.error(msg["error"])
            elif msg["type"] == "video":
                st.markdown(msg["content"])
                if msg.get("media_path"):
                    st.video(msg["media_path"])
                elif msg.get("error"):
                    st.error(msg["error"])

    # Chat input
    if prompt := st.chat_input("Введите ваш запрос..."):
        # Append user message
        st.session_state.chat_history.append({"role": "user", "type": "text", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        route = get_route(prompt)

        with st.chat_message("assistant"):
            if route == ROUTE_IMAGE:
                st.markdown(f"Генерирую изображение по запросу: {prompt}")
                with st.spinner("Создание изображения..."):
                    img_url, err = generate_image(prompt)
                    if err:
                        st.error(err)
                        st.session_state.chat_history.append({"role": "assistant", "type": "image", "content": f"Генерирую изображение по запросу: {prompt}", "error": err})
                    else:
                        st.image(img_url)
                        st.session_state.chat_history.append({"role": "assistant", "type": "image", "content": f"Генерирую изображение по запросу: {prompt}", "media_path": img_url})

            elif route == ROUTE_MUSIC:
                st.markdown(f"Генерирую музыку по запросу: {prompt}")
                with st.spinner("Создание музыки..."):
                    music_path, err = generate_music(prompt)
                    if err:
                        st.error(err)
                        st.session_state.chat_history.append({"role": "assistant", "type": "music", "content": f"Генерирую музыку по запросу: {prompt}", "error": err})
                    else:
                        st.audio(music_path)
                        st.session_state.chat_history.append({"role": "assistant", "type": "music", "content": f"Генерирую музыку по запросу: {prompt}", "media_path": music_path})

            elif route == ROUTE_VIDEO:
                st.markdown(f"Генерирую видео по запросу: {prompt}")
                with st.spinner("Создание видео..."):
                    video_path, err = generate_video(prompt)
                    if err:
                        st.error(err)
                        st.session_state.chat_history.append({"role": "assistant", "type": "video", "content": f"Генерирую видео по запросу: {prompt}", "error": err})
                    else:
                        st.video(video_path)
                        st.session_state.chat_history.append({"role": "assistant", "type": "video", "content": f"Генерирую видео по запросу: {prompt}", "media_path": video_path})

            elif route == ROUTE_TEXT:
                if not st.session_state.gemini_client or not st.session_state.chat_session:
                    st.error("Пожалуйста, введите валидный Google API Key в боковой панели.")
                    st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": "Пожалуйста, введите валидный Google API Key в боковой панели."})
                else:
                    try:
                        response = st.session_state.chat_session.send_message_stream(prompt)
                        full_response = ""
                        placeholder = st.empty()
                        for chunk in response:
                            if chunk.text:
                                full_response += chunk.text
                                placeholder.markdown(full_response + "▌")
                        placeholder.markdown(full_response)
                        st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": full_response})
                    except Exception as e:
                        err_msg = f"Ошибка Gemini API: {str(e)}"
                        st.error(err_msg)
                        st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": err_msg})

if __name__ == "__main__":
    main()
