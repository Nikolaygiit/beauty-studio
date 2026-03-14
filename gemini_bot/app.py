import streamlit as st
from modules.text import get_text_response, init_chat_session
from modules.image import generate_image_url
from modules.music import init_music_client, generate_music
from modules.video import init_video_client, generate_video

# Streamlit Page Config
st.set_page_config(
    page_title="Gemini Ultimate Bot",
    page_icon="✨",
    layout="wide"
)

# Initialize Session State
if "chat_session" not in st.session_state:
    st.session_state.chat_session = None

if "messages" not in st.session_state:
    st.session_state.messages = []

# Caching Resource-Heavy Clients
@st.cache_resource
def get_music_client():
    return init_music_client()

@st.cache_resource
def get_video_client():
    return init_video_client()

# Sidebar Configuration
with st.sidebar:
    st.title("Настройки бота ⚙️")

    # API Key Input
    google_api_key = st.text_input(
        "Введите GOOGLE_API_KEY",
        type="password",
        help="Ключ необходим для работы текстовой модели Gemini"
    )

    if st.button("Очистить историю чата", use_container_width=True):
        st.session_state.messages = []
        if google_api_key:
            st.session_state.chat_session = init_chat_session(google_api_key)
        else:
            st.session_state.chat_session = None
        st.success("История очищена!")
        st.rerun()

    st.markdown("---")
    st.markdown("### Инструкция")
    st.markdown("""
    - **Текст**: Просто напишите ваш вопрос (работает через Gemini).
    - **Изображение**: Начните запрос со слов `нарисуй`, `фото` или `изображение`.
    - **Музыка**: Начните запрос со слова `музыка`.
    - **Видео**: Начните запрос со слова `видео`.
    """)

# Main Content Title
st.title("Gemini Ultimate Bot ✨")
st.markdown("Генерация текста, изображений, музыки и видео в одном месте!")

# Initialize chat session if key is provided and session doesn't exist
if google_api_key and st.session_state.chat_session is None:
    st.session_state.chat_session = init_chat_session(google_api_key)

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["type"] == "text":
            st.markdown(message["content"])
        elif message["type"] == "image":
            st.image(message["content"], caption=message.get("caption", ""))
        elif message["type"] == "music":
            st.audio(message["content"])
            if "caption" in message:
                st.caption(message["caption"])
        elif message["type"] == "video":
            st.video(message["content"])
            if "caption" in message:
                st.caption(message["caption"])

# Chat Input & Routing
prompt = st.chat_input("Введите ваш запрос...")

if prompt:
    # Append user message to history
    st.session_state.messages.append({"role": "user", "type": "text", "content": prompt})

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    prompt_lower = prompt.lower()

    # Route Image Generation
    if prompt_lower.startswith(("нарисуй", "фото", "изображение")):
        # Strip keyword
        clean_prompt = prompt
        for kw in ["нарисуй", "фото", "изображение"]:
             if prompt_lower.startswith(kw):
                 clean_prompt = prompt[len(kw):].strip()
                 break

        if not clean_prompt:
             clean_prompt = "beautiful landscape" # Fallback

        with st.chat_message("assistant"):
            st.markdown(f"Генерирую изображение: *{clean_prompt}*...")
            image_url = generate_image_url(clean_prompt)
            st.image(image_url)
            st.session_state.messages.append({
                "role": "assistant",
                "type": "image",
                "content": image_url,
                "caption": clean_prompt
            })

    # Route Music Generation
    elif prompt_lower.startswith("музыка"):
        clean_prompt = prompt[len("музыка"):].strip()
        if not clean_prompt:
            clean_prompt = "80s pop track with synth and instrumentals"

        with st.chat_message("assistant"):
            st.markdown(f"Создаю музыку: *{clean_prompt}*... (Это может занять некоторое время)")
            client = get_music_client()
            error_msg, audio_path = generate_music(client, clean_prompt)

            if error_msg:
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "type": "text", "content": error_msg})
            elif audio_path:
                st.audio(audio_path)
                st.session_state.messages.append({
                    "role": "assistant",
                    "type": "music",
                    "content": audio_path,
                    "caption": clean_prompt
                })

    # Route Video Generation
    elif prompt_lower.startswith("видео"):
        clean_prompt = prompt[len("видео"):].strip()
        if not clean_prompt:
             clean_prompt = "a dog playing in the park"

        with st.chat_message("assistant"):
            st.markdown(f"Генерирую видео: *{clean_prompt}*... (Это может занять некоторое время)")
            client = get_video_client()
            error_msg, video_path = generate_video(client, clean_prompt)

            if error_msg:
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "type": "text", "content": error_msg})
            elif video_path:
                 st.video(video_path)
                 st.session_state.messages.append({
                     "role": "assistant",
                     "type": "video",
                     "content": video_path,
                     "caption": clean_prompt
                 })

    # Route Text Generation (Default)
    else:
        with st.chat_message("assistant"):
            if not google_api_key:
                 error_msg = "Ошибка: Пожалуйста, введите ваш Google API Key в боковой панели."
                 st.error(error_msg)
                 st.session_state.messages.append({"role": "assistant", "type": "text", "content": error_msg})
            else:
                 response_placeholder = st.empty()
                 full_response = ""

                 # Initialize session if we don't have it
                 if st.session_state.chat_session is None:
                     st.session_state.chat_session = init_chat_session(google_api_key)

                 # Stream response
                 for chunk in get_text_response(google_api_key, prompt, st.session_state.chat_session):
                      full_response += chunk
                      response_placeholder.markdown(full_response + "▌")

                 response_placeholder.markdown(full_response)
                 st.session_state.messages.append({"role": "assistant", "type": "text", "content": full_response})
