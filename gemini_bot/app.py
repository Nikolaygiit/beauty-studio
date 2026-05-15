import streamlit as st
from modules.text import init_chat_session, generate_text_stream
from modules.image import generate_image
from modules.music import generate_music
from modules.video import generate_video

# --- Caching Resource-Heavy Generators ---
@st.cache_resource
def get_music_generator():
    return generate_music

@st.cache_resource
def get_video_generator():
    return generate_video

# --- State Management ---
def clear_chat_history():
    st.session_state.chat_history = []
    st.session_state.chat_session = None
    st.session_state.gemini_client = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "chat_session" not in st.session_state:
    st.session_state.chat_session = None
if "gemini_client" not in st.session_state:
    st.session_state.gemini_client = None
if "current_api_key" not in st.session_state:
    st.session_state.current_api_key = ""

# --- UI Setup ---
st.set_page_config(page_title="Gemini Ultimate Bot", page_icon="🤖", layout="wide")
st.title("🤖 Gemini Ultimate Bot")

# --- Sidebar ---
with st.sidebar:
    st.header("Настройки")
    api_key = st.text_input("Введите GOOGLE_API_KEY", type="password")

    # Re-initialize if API key changes
    if api_key != st.session_state.current_api_key:
        st.session_state.current_api_key = api_key
        st.session_state.chat_session = None
        st.session_state.gemini_client = None

    st.button("Очистить историю чата", on_click=clear_chat_history)

    st.markdown("---")
    st.markdown("### Доступные функции:")
    st.markdown("- **Чат с Gemini 2.0 Flash** (обычный текст)")
    st.markdown("- **Генерация изображений** (напишите *нарисуй*, *фото* или *изображение*)")
    st.markdown("- **Генерация музыки** (напишите *музыка*, *песня* или *трек*)")
    st.markdown("- **Генерация видео** (напишите *видео* или *ролик*)")

# --- Initialize Gemini Session ---
if api_key and not st.session_state.chat_session:
    client, session, error = init_chat_session(api_key)
    if error:
        st.sidebar.error(error)
    else:
        st.session_state.gemini_client = client
        st.session_state.chat_session = session

# --- Display Chat History ---
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        if message["type"] == "text":
            st.markdown(message["content"])
        elif message["type"] == "image":
            st.image(message["content"])
            st.markdown(message["caption"])
        elif message["type"] == "audio":
            st.audio(message["content"])
            st.markdown(message["caption"])
        elif message["type"] == "video":
            st.video(message["content"])
            st.markdown(message["caption"])

# --- Chat Input ---
if prompt := st.chat_input("Введите сообщение или запрос..."):
    # Require API key
    if not api_key:
        st.error("Пожалуйста, введите GOOGLE_API_KEY в боковой панели.")
        st.stop()

    # Append user message
    st.session_state.chat_history.append({"role": "user", "type": "text", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        prompt_lower = prompt.lower()

        # --- Routing Logic ---
        if any(kw in prompt_lower for kw in ["нарисуй", "фото", "изображение"]):
            with st.spinner("Рисую..."):
                img_url, error = generate_image(prompt)
                if error:
                    st.error(error)
                    st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": error})
                elif img_url:
                    st.image(img_url)
                    msg = "Вот ваше изображение!"
                    st.markdown(msg)
                    st.session_state.chat_history.append({"role": "assistant", "type": "image", "content": img_url, "caption": msg})

        elif any(kw in prompt_lower for kw in ["музыка", "песня", "трек"]):
            with st.spinner("Создаю музыку (это может занять некоторое время)..."):
                music_gen_func = get_music_generator()
                audio_path, error = music_gen_func(prompt)
                if error:
                    st.error(error)
                    st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": error})
                elif audio_path:
                    st.audio(audio_path)
                    msg = "Вот ваша музыка!"
                    st.markdown(msg)
                    st.session_state.chat_history.append({"role": "assistant", "type": "audio", "content": audio_path, "caption": msg})

        elif any(kw in prompt_lower for kw in ["видео", "ролик"]):
            with st.spinner("Монтирую видео (это может занять время)..."):
                video_gen_func = get_video_generator()
                video_path, error = video_gen_func(prompt)
                if error:
                    st.error(error)
                    st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": error})
                elif video_path:
                    st.video(video_path)
                    msg = "Вот ваше видео!"
                    st.markdown(msg)
                    st.session_state.chat_history.append({"role": "assistant", "type": "video", "content": video_path, "caption": msg})

        else:
            # Fallback to Text Generation with Streaming
            if st.session_state.chat_session:
                response_placeholder = st.empty()
                full_response = ""

                stream = generate_text_stream(st.session_state.chat_session, prompt)
                error_occurred = False

                for text_chunk, error in stream:
                    if error:
                        st.error(error)
                        full_response += f"\n\n[Ошибка: {error}]"
                        error_occurred = True
                        break
                    elif text_chunk:
                        full_response += text_chunk
                        response_placeholder.markdown(full_response + "▌")

                if not error_occurred:
                    response_placeholder.markdown(full_response)

                if full_response:
                    st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": full_response})
            else:
                st.error("Сессия чата не инициализирована. Проверьте API ключ.")
