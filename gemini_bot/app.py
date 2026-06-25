import streamlit as st
from modules.routing import route_prompt
from modules.text import get_gemini_client, get_chat_session
from modules.image import generate_image
from modules.music import generate_music
from modules.video import generate_video

st.set_page_config(page_title="Gemini Ultimate Bot", page_icon="🤖")

def clear_chat():
    st.session_state.chat_history = []
    st.session_state.chat_session = None
    st.session_state.gemini_client = None

# Sidebar
with st.sidebar:
    st.title("⚙️ Настройки")
    api_key = st.text_input("Введите GOOGLE_API_KEY", type="password")
    if st.button("Очистить историю чата"):
        clear_chat()
        st.success("История очищена!")

# Initialize state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "current_api_key" not in st.session_state:
    st.session_state.current_api_key = ""
if "chat_session" not in st.session_state:
    st.session_state.chat_session = None
if "gemini_client" not in st.session_state:
    st.session_state.gemini_client = None

# Check API key change
if api_key != st.session_state.current_api_key:
    st.session_state.current_api_key = api_key
    st.session_state.gemini_client = None
    st.session_state.chat_session = None

st.title("🤖 Gemini Ultimate Bot")
st.markdown("Привет! Я могу генерировать текст, изображения, музыку и видео. Просто попроси меня об этом!")

# Display history
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        media_type = msg.get("type")
        media_path = msg.get("media_path")

        if media_path:
            if media_type == "image":
                st.image(media_path)
            elif media_type == "music":
                st.audio(media_path)
            elif media_type == "video":
                st.video(media_path)

# Chat input
if prompt := st.chat_input("Введите ваш запрос..."):
    if not api_key:
        st.error("Пожалуйста, введите GOOGLE_API_KEY в боковой панели.")
        st.stop()

    # Append user message
    st.session_state.chat_history.append({"role": "user", "content": prompt, "type": "text"})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Route and process
    route = route_prompt(prompt)

    with st.chat_message("assistant"):
        if route == "text":
            # Initialize client if needed
            if st.session_state.gemini_client is None:
                client, err = get_gemini_client(api_key)
                if err:
                    st.error(err)
                    st.stop()
                st.session_state.gemini_client = client
                st.session_state.chat_session = get_chat_session(client)

            try:
                response_placeholder = st.empty()
                full_response = ""
                # Stream response
                response_stream = st.session_state.chat_session.send_message_stream(prompt)
                for chunk in response_stream:
                    if chunk.text:
                        full_response += chunk.text
                        response_placeholder.markdown(full_response + "▌")
                response_placeholder.markdown(full_response)

                st.session_state.chat_history.append({"role": "assistant", "content": full_response, "type": "text"})
            except Exception as e:
                st.error(f"Ошибка Gemini API: {str(e)}")

        elif route == "image":
            with st.spinner("Генерация изображения..."):
                url, err = generate_image(prompt)
                if err:
                    st.error(err)
                elif url:
                    st.markdown(f"Вот ваше изображение:")
                    st.image(url)
                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": "Вот ваше изображение:",
                        "type": "image",
                        "media_path": url
                    })

        elif route == "music":
            with st.spinner("Генерация музыки... (это может занять время)"):
                path, err = generate_music(prompt)
                if err:
                    st.error(err)
                elif path:
                    st.markdown("Вот ваша музыка:")
                    st.audio(path)
                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": "Вот ваша музыка:",
                        "type": "music",
                        "media_path": path
                    })

        elif route == "video":
            with st.spinner("Генерация видео... (это может занять время)"):
                path, err = generate_video(prompt)
                if err:
                    st.error(err)
                elif path:
                    st.markdown("Вот ваше видео:")
                    st.video(path)
                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": "Вот ваше видео:",
                        "type": "video",
                        "media_path": path
                    })
