import streamlit as st
from modules.text import init_chat_session, generate_text_stream
from modules.image import generate_image
from modules.music import generate_music
from modules.video import generate_video

# Function to clear chat history and reset session state
def clear_chat_history():
    st.session_state.chat_history = []
    st.session_state.chat_session = None
    st.session_state.gemini_client = None
    # Depending on requirements, we might want to keep the current_api_key or reset it.
    # In this case, memory states clearing chat history resets session state including api_key:
    st.session_state.current_api_key = ""

# Initialization of Streamlit layout and session state
st.set_page_config(page_title="Gemini Ultimate Bot", page_icon="🤖", layout="wide")
st.title("🤖 Gemini Ultimate Bot")
st.markdown("Ваш интеллектуальный помощник с функциями генерации текста, изображений, музыки и видео!")

# Initialize session state variables if they don't exist
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "chat_session" not in st.session_state:
    st.session_state.chat_session = None
if "gemini_client" not in st.session_state:
    st.session_state.gemini_client = None
if "current_api_key" not in st.session_state:
    st.session_state.current_api_key = ""

# Sidebar for API Key and Chat Controls
with st.sidebar:
    st.header("Настройки")
    api_key_input = st.text_input("Введите GOOGLE_API_KEY", type="password", value=st.session_state.current_api_key)

    if st.button("Очистить историю чата", on_click=clear_chat_history):
        pass # The callback handles the logic

    st.markdown("---")
    st.markdown("""
    **Команды для генерации медиа:**
    - **Изображение:** *нарисуй, фото, изображение*
    - **Музыка:** *музыка, песня, трек*
    - **Видео:** *видео, ролик*
    """)

# Re-initialize Gemini client if API key has changed and is valid
if api_key_input and api_key_input != st.session_state.current_api_key:
    st.session_state.current_api_key = api_key_input
    client, chat, error_msg = init_chat_session(st.session_state.current_api_key)
    if error_msg:
        st.sidebar.error(error_msg)
        st.session_state.chat_session = None
        st.session_state.gemini_client = None
    else:
        st.session_state.gemini_client = client
        st.session_state.chat_session = chat
        st.sidebar.success("Gemini API успешно подключен!")

# Render existing chat history
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
        elif message["type"] == "error":
            st.error(message["content"])

# --- Keyword Routing and Request Handling ---

def detect_media_intent(prompt):
    """
    Returns media intent ('image', 'music', 'video', or None) based on keywords in the prompt.
    """
    p_lower = prompt.lower()
    if any(keyword in p_lower for keyword in ['нарисуй', 'фото', 'изображение']):
        return 'image'
    elif any(keyword in p_lower for keyword in ['музык', 'песн', 'трек']):
        # 'музык' accounts for morphology (музыка, музыку, музыки)
        # 'песн' accounts for morphology (песня, песню, песни)
        return 'music'
    elif any(keyword in p_lower for keyword in ['видео', 'ролик']):
        return 'video'
    return None

prompt = st.chat_input("Введите ваше сообщение...")

if prompt:
    # 1. Add user message to history and render it
    st.session_state.chat_history.append({"role": "user", "type": "text", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Check if API Key is set
    if not st.session_state.current_api_key or not st.session_state.chat_session:
        error_text = "Пожалуйста, введите валидный GOOGLE_API_KEY в боковой панели."
        st.session_state.chat_history.append({"role": "assistant", "type": "error", "content": error_text})
        with st.chat_message("assistant"):
            st.error(error_text)
        st.stop()

    intent = detect_media_intent(prompt)

    # 2. Handle based on intent
    with st.chat_message("assistant"):
        if intent == 'image':
            with st.spinner("Генерация изображения..."):
                image_url, err = generate_image(prompt)
                if err:
                    st.error(err)
                    st.session_state.chat_history.append({"role": "assistant", "type": "error", "content": err})
                else:
                    st.image(image_url)
                    st.session_state.chat_history.append({"role": "assistant", "type": "image", "content": image_url})

        elif intent == 'music':
            with st.spinner("Генерация музыки (это может занять время)..."):
                music_path, err = generate_music(prompt)
                if err:
                    st.error(err)
                    st.session_state.chat_history.append({"role": "assistant", "type": "error", "content": err})
                else:
                    st.audio(music_path)
                    st.session_state.chat_history.append({"role": "assistant", "type": "audio", "content": music_path})

        elif intent == 'video':
            with st.spinner("Генерация видео (это может занять значительное время)..."):
                video_path, err = generate_video(prompt)
                if err:
                    st.error(err)
                    st.session_state.chat_history.append({"role": "assistant", "type": "error", "content": err})
                else:
                    st.video(video_path)
                    st.session_state.chat_history.append({"role": "assistant", "type": "video", "content": video_path})

        else:
            # Regular text generation
            with st.spinner("Думаю..."):
                stream, err = generate_text_stream(st.session_state.chat_session, prompt)
                if err:
                    st.error(err)
                    st.session_state.chat_history.append({"role": "assistant", "type": "error", "content": err})
                else:
                    message_placeholder = st.empty()
                    full_response = ""
                    try:
                        for chunk in stream:
                            if chunk.text:
                                full_response += chunk.text
                                message_placeholder.markdown(full_response + "▌")
                        message_placeholder.markdown(full_response)
                        st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": full_response})
                    except Exception as e:
                        err_msg = f"Ошибка во время потоковой передачи: {e}"
                        st.error(err_msg)
                        st.session_state.chat_history.append({"role": "assistant", "type": "error", "content": err_msg})
