import streamlit as st
from modules.text import get_gemini_client
from modules.image import generate_image
from modules.music import generate_music
from modules.video import generate_video
from modules.routing import get_route

st.set_page_config(page_title="Gemini Ultimate Bot", page_icon="✨", layout="centered")

st.title("✨ Gemini Ultimate Bot")

# --- Session State Initialization ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "chat_session" not in st.session_state:
    st.session_state.chat_session = None
if "gemini_client" not in st.session_state:
    st.session_state.gemini_client = None
if "current_api_key" not in st.session_state:
    st.session_state.current_api_key = ""

# --- Sidebar UI ---
with st.sidebar:
    st.header("Настройки")
    api_key_input = st.text_input("Введите GOOGLE_API_KEY", type="password", value=st.session_state.current_api_key)

    if st.button("Очистить историю чата", key="clear_chat"):
        st.session_state.chat_history = []
        st.session_state.chat_session = None
        st.session_state.gemini_client = None
        st.session_state.current_api_key = ""
        st.rerun()

# --- API Key Change Handling ---
if api_key_input and api_key_input != st.session_state.current_api_key:
    st.session_state.current_api_key = api_key_input
    # Reinitialize client with new key
    client, chat = get_gemini_client(api_key_input)
    if client:
        st.session_state.gemini_client = client
        st.session_state.chat_session = chat
        # Optional: could clear history on key change or keep it. Let's keep it for now.
    else:
        st.sidebar.error(chat) # This contains error message if client is None

# --- Main UI ---
if not st.session_state.current_api_key:
    st.warning("Пожалуйста, введите ваш Google API Key в боковой панели, чтобы начать.")
elif not st.session_state.gemini_client:
    # Try initializing if key is there but client isn't (e.g. after refresh)
    client, chat = get_gemini_client(st.session_state.current_api_key)
    if client:
        st.session_state.gemini_client = client
        st.session_state.chat_session = chat
    else:
        st.error(chat)

# Render Chat History
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        if message["type"] == "text":
            st.markdown(message["content"])
        elif message["type"] == "image":
            st.markdown(f"**Промпт для изображения:** {message['prompt']}")
            st.image(message["content"])
        elif message["type"] == "music":
            st.markdown(f"**Промпт для музыки:** {message['prompt']}")
            st.audio(message["content"])
        elif message["type"] == "video":
            st.markdown(f"**Промпт для видео:** {message['prompt']}")
            st.video(message["content"])

# Chat Input
prompt = st.chat_input("Спросите меня о чем угодно или попросите сгенерировать медиа...")

if prompt:
    # 1. Add user message to UI and history
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.chat_history.append({"role": "user", "type": "text", "content": prompt})

    # 2. Determine Route
    route = get_route(prompt)

    # 3. Handle Route
    with st.chat_message("assistant"):
        if route == "image":
            with st.spinner("Генерация изображения..."):
                url, error = generate_image(prompt)
                if url:
                    st.image(url)
                    st.session_state.chat_history.append({"role": "assistant", "type": "image", "content": url, "prompt": prompt})
                else:
                    st.error(error)
                    st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": error})

        elif route == "music":
            with st.spinner("Генерация музыки (это может занять некоторое время)..."):
                path_or_url, error = generate_music(prompt)
                if path_or_url:
                    st.audio(path_or_url)
                    st.session_state.chat_history.append({"role": "assistant", "type": "music", "content": path_or_url, "prompt": prompt})
                else:
                    st.error(error)
                    st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": error})

        elif route == "video":
            with st.spinner("Генерация видео (это может занять некоторое время)..."):
                path_or_url, error = generate_video(prompt)
                if path_or_url:
                    st.video(path_or_url)
                    st.session_state.chat_history.append({"role": "assistant", "type": "video", "content": path_or_url, "prompt": prompt})
                else:
                    st.error(error)
                    st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": error})

        else: # "text" route
            if not st.session_state.chat_session:
                 st.error("Чат сессия не инициализирована. Проверьте API ключ.")
            else:
                try:
                    response_container = st.empty()
                    full_response = ""
                    # Stream response
                    for chunk in st.session_state.chat_session.send_message_stream(prompt):
                        if chunk.text:
                            full_response += chunk.text
                            response_container.markdown(full_response + "▌")
                    response_container.markdown(full_response)
                    st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": full_response})
                except Exception as e:
                    error_msg = f"Ошибка генерации текста: {str(e)}"
                    st.error(error_msg)
                    st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": error_msg})
