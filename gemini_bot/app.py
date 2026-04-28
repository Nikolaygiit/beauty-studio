import streamlit as st
import modules.text as text_module
import modules.image as image_module
import modules.music as music_module
import modules.video as video_module

st.set_page_config(page_title="Gemini Ultimate Bot", page_icon="✨")

st.title("✨ Gemini Ultimate Bot")
st.markdown("Универсальный бот: текст, изображения, музыка и видео!")

# Sidebar config
st.sidebar.header("Настройки")
api_key = st.sidebar.text_input("Введите GOOGLE_API_KEY", type="password")

if st.sidebar.button("Очистить историю чата"):
    st.session_state.chat_history = []
    if 'chat_session' in st.session_state:
        del st.session_state.chat_session
    if 'gemini_client' in st.session_state:
        del st.session_state.gemini_client
    st.session_state.current_api_key = None
    st.rerun()

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "current_api_key" not in st.session_state:
    st.session_state.current_api_key = None

# Re-initialize Gemini client if the API key changes or is missing
if api_key and (st.session_state.current_api_key != api_key or "chat_session" not in st.session_state):
    try:
        client, chat = text_module.initialize_chat(api_key)
        st.session_state.gemini_client = client
        st.session_state.chat_session = chat
        st.session_state.current_api_key = api_key
    except Exception as e:
        st.sidebar.error(f"Ошибка инициализации Gemini: {e}")

# Cache resource heavy generators to prevent re-init
@st.cache_resource(show_spinner=False)
def get_music_generator():
    return music_module.generate_music

@st.cache_resource(show_spinner=False)
def get_video_generator():
    return video_module.generate_video

# Render Chat History
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        if message["type"] == "text":
            st.markdown(message["content"])
        elif message["type"] == "image":
            st.image(message["content"], caption=message.get("prompt", ""))
        elif message["type"] == "music":
            st.audio(message["content"])
            st.caption(f"Prompt: {message.get('prompt', '')}")
        elif message["type"] == "video":
            st.video(message["content"])
            st.caption(f"Prompt: {message.get('prompt', '')}")
        elif message["type"] == "error":
            st.error(message["content"])

# User Input
if prompt := st.chat_input("Напишите сообщение (напр. 'нарисуй кота', 'музыка для сна', 'видео океана')..."):
    if not api_key:
        st.error("Пожалуйста, введите GOOGLE_API_KEY в боковом меню.")
        st.stop()

    st.session_state.chat_history.append({"role": "user", "type": "text", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    prompt_lower = prompt.lower()

    # Keyword Router
    if any(word in prompt_lower for word in ["нарисуй", "фото", "изображение"]):
        # Image Generation
        with st.chat_message("assistant"):
            with st.spinner("Генерирую изображение..."):
                img_url = image_module.generate_image_url(prompt)
                st.image(img_url)
        st.session_state.chat_history.append({"role": "assistant", "type": "image", "content": img_url, "prompt": prompt})

    elif any(word in prompt_lower for word in ["музыка", "песня", "трек"]):
        # Music Generation
        with st.chat_message("assistant"):
            with st.spinner("Создаю музыку..."):
                gen_func = get_music_generator()
                audio_path, error = gen_func(prompt)

                if error:
                    st.error(error)
                    st.session_state.chat_history.append({"role": "assistant", "type": "error", "content": error})
                elif audio_path:
                    st.audio(audio_path)
                    st.session_state.chat_history.append({"role": "assistant", "type": "music", "content": audio_path, "prompt": prompt})

    elif any(word in prompt_lower for word in ["видео", "ролик"]):
        # Video Generation
        with st.chat_message("assistant"):
            with st.spinner("Синтезирую видео..."):
                gen_func = get_video_generator()
                video_path, error = gen_func(prompt)

                if error:
                    st.error(error)
                    st.session_state.chat_history.append({"role": "assistant", "type": "error", "content": error})
                elif video_path:
                    st.video(video_path)
                    st.session_state.chat_history.append({"role": "assistant", "type": "video", "content": video_path, "prompt": prompt})

    else:
        # Standard Text Generation (Gemini)
        with st.chat_message("assistant"):
            if "chat_session" in st.session_state:
                with st.spinner("Печатаю..."):
                    chat = st.session_state.chat_session
                    placeholder = st.empty()
                    full_response = ""
                    for chunk_text in text_module.stream_text_response(chat, prompt):
                        full_response += chunk_text
                        placeholder.markdown(full_response + "▌")
                    placeholder.markdown(full_response)

                # Check if it was an error message from text module
                if full_response.startswith("⚠️"):
                     st.session_state.chat_history.append({"role": "assistant", "type": "error", "content": full_response})
                else:
                     st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": full_response})
            else:
                st.error("Сессия чата не инициализирована. Проверьте API ключ.")
