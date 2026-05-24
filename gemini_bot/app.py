import streamlit as st
from modules.text import init_gemini_client_and_session, generate_text_stream
from modules.image import generate_image
from modules.music import generate_music
from modules.video import generate_video

# --- UI Sidebar ---
st.sidebar.title("Настройки")
api_key_input = st.sidebar.text_input("Введите GOOGLE_API_KEY", type="password")

if st.sidebar.button("Очистить историю чата"):
    st.session_state.chat_history = []
    st.session_state.chat_session = None
    st.session_state.gemini_client = None
    st.session_state.current_api_key = None
    st.sidebar.success("История очищена.")

# --- Session State Management ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "chat_session" not in st.session_state:
    st.session_state.chat_session = None
if "gemini_client" not in st.session_state:
    st.session_state.gemini_client = None
if "current_api_key" not in st.session_state:
    st.session_state.current_api_key = None

# Re-initialize Gemini client if API key changes
if api_key_input and api_key_input != st.session_state.current_api_key:
    client, session = init_gemini_client_and_session(api_key_input)
    if client and session:
        st.session_state.gemini_client = client
        st.session_state.chat_session = session
        st.session_state.current_api_key = api_key_input
        st.sidebar.success("Успешное подключение к Gemini!")
    else:
        st.sidebar.error("Ошибка при подключении. Проверьте API ключ.")

st.title("Gemini Ultimate Bot 🤖")
st.markdown("Бот умеет генерировать текст, изображения, музыку и видео. Попросите его!")

# --- Display Chat History ---
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        if msg["type"] == "text":
            st.markdown(msg["content"])
        elif msg["type"] == "image":
            st.image(msg["content"])
        elif msg["type"] == "audio":
            st.audio(msg["content"])
        elif msg["type"] == "video":
            st.video(msg["content"])

# --- App Routing ---
user_input = st.chat_input("Введите ваш запрос...")

def determine_routing(prompt: str) -> str:
    prompt_lower = prompt.lower()

    # Image routing
    if any(keyword in prompt_lower for keyword in ['нарисуй', 'фото', 'изображение']):
        return "image"

    # Music routing
    if any(keyword in prompt_lower for keyword in ['музык', 'песн', 'трек']):
        return "music"

    # Video routing
    if any(keyword in prompt_lower for keyword in ['видео', 'ролик']):
        return "video"

    return "text"

if user_input:
    # Handle API Key check for text mode
    route = determine_routing(user_input)
    if route == "text" and not st.session_state.chat_session:
        st.error("Для генерации текста сначала введите GOOGLE_API_KEY в боковой панели.")
        st.stop()

    # Append user message
    st.session_state.chat_history.append({"role": "user", "type": "text", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Rendering Assistant response
    with st.chat_message("assistant"):
        if route == "image":
            with st.spinner("Генерация изображения..."):
                url, error = generate_image(user_input)
                if error:
                    st.error(error)
                    st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": error})
                elif url:
                    st.image(url)
                    st.session_state.chat_history.append({"role": "assistant", "type": "image", "content": url})

        elif route == "music":
            with st.spinner("Генерация музыки..."):
                file_path, error = generate_music(user_input)
                if error:
                    st.error(error)
                    st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": error})
                elif file_path:
                    st.audio(file_path)
                    st.session_state.chat_history.append({"role": "assistant", "type": "audio", "content": file_path})

        elif route == "video":
            with st.spinner("Генерация видео..."):
                file_path, error = generate_video(user_input)
                if error:
                    st.error(error)
                    st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": error})
                elif file_path:
                    st.video(file_path)
                    st.session_state.chat_history.append({"role": "assistant", "type": "video", "content": file_path})

        elif route == "text":
            stream = generate_text_stream(st.session_state.chat_session, user_input)
            response_placeholder = st.empty()
            full_response = ""
            for chunk_text in stream:
                 full_response += chunk_text
                 response_placeholder.markdown(full_response + "▌")
            response_placeholder.markdown(full_response)
            st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": full_response})
