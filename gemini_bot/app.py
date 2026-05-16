import streamlit as st
from modules.text import init_gemini_client, init_chat_session
from modules.image import generate_image
from modules.music import generate_music
from modules.video import generate_video

@st.cache_resource
def cached_generate_music(prompt):
    return generate_music(prompt)

@st.cache_resource
def cached_generate_video(prompt):
    return generate_video(prompt)

# --- App Configuration ---
st.set_page_config(page_title="Gemini Ultimate Bot", page_icon="🤖", layout="wide")

st.title("Gemini Ultimate Bot")
st.write("Привет! Я могу общаться с тобой, а также генерировать изображения, музыку и видео по твоим запросам.")

# --- Sidebar: Configuration & Tools ---
with st.sidebar:
    st.header("Настройки")
    api_key = st.text_input("Введите GOOGLE_API_KEY", type="password")

    if st.button("Очистить историю чата"):
        for key in ["chat_history", "chat_session", "gemini_client", "current_api_key"]:
            if key in st.session_state:
                del st.session_state[key]
        st.success("История чата очищена!")
        st.rerun()

# --- Session State Initialization ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "current_api_key" not in st.session_state or st.session_state.current_api_key != api_key:
    if api_key:
        client, err = init_gemini_client(api_key)
        if err:
            st.sidebar.error(err)
        else:
            chat, chat_err = init_chat_session(client)
            if chat_err:
                st.sidebar.error(chat_err)
            else:
                st.session_state.gemini_client = client
                st.session_state.chat_session = chat
                st.session_state.current_api_key = api_key
                st.sidebar.success("Успешно подключено к Gemini!")
    elif "current_api_key" in st.session_state:
        # Key was removed
        del st.session_state.current_api_key
        if "gemini_client" in st.session_state: del st.session_state.gemini_client
        if "chat_session" in st.session_state: del st.session_state.chat_session

# --- Main Chat Interface ---
# Display existing chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "media_type" in message:
            if message["media_type"] == "image":
                st.image(message["media_url"])
            elif message["media_type"] == "music":
                st.audio(message["media_url"])
            elif message["media_type"] == "video":
                st.video(message["media_url"])

# Chat input
if prompt := st.chat_input("Напишите сообщение..."):
    if not api_key or "chat_session" not in st.session_state:
        st.error("Пожалуйста, введите GOOGLE_API_KEY в боковой панели.")
    else:
        # Display user message
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Routing Logic based on Russian keywords
        lower_prompt = prompt.lower()

        with st.chat_message("assistant"):
            if any(keyword in lower_prompt for keyword in ["нарисуй", "фото", "изображение"]):
                st.write("Генерирую изображение...")
                with st.spinner("Создание изображения..."):
                    img_url, err = generate_image(prompt)
                    if err:
                        st.error(err)
                        st.session_state.chat_history.append({"role": "assistant", "content": f"Ошибка генерации изображения: {err}"})
                    else:
                        st.image(img_url)
                        st.session_state.chat_history.append({
                            "role": "assistant",
                            "content": "Вот ваше изображение:",
                            "media_type": "image",
                            "media_url": img_url
                        })

            elif any(keyword in lower_prompt for keyword in ["музыка", "песня", "трек"]):
                st.write("Генерирую музыку...")
                with st.spinner("Создание музыки..."):
                    music_path, err = cached_generate_music(prompt)
                    if err:
                        st.error(err)
                        st.session_state.chat_history.append({"role": "assistant", "content": f"Ошибка генерации музыки: {err}"})
                    else:
                        # Gradio client returns a file path or tuple for audio
                        if isinstance(music_path, tuple):
                             music_file = music_path[0]
                        else:
                             music_file = music_path

                        st.audio(music_file)
                        st.session_state.chat_history.append({
                            "role": "assistant",
                            "content": "Вот ваша музыка:",
                            "media_type": "music",
                            "media_url": music_file
                        })

            elif any(keyword in lower_prompt for keyword in ["видео", "ролик"]):
                st.write("Генерирую видео...")
                with st.spinner("Создание видео..."):
                    video_path, err = cached_generate_video(prompt)
                    if err:
                        st.error(err)
                        st.session_state.chat_history.append({"role": "assistant", "content": f"Ошибка генерации видео: {err}"})
                    else:
                        st.video(video_path)
                        st.session_state.chat_history.append({
                            "role": "assistant",
                            "content": "Вот ваше видео:",
                            "media_type": "video",
                            "media_url": video_path
                        })

            else:
                # Default text generation
                st.write("Думаю...")
                try:
                    response = st.session_state.chat_session.send_message(prompt, stream=True)
                    response_text = ""
                    placeholder = st.empty()
                    for chunk in response:
                        if chunk.text:
                            response_text += chunk.text
                            placeholder.markdown(response_text + "▌")
                    placeholder.markdown(response_text)
                    st.session_state.chat_history.append({"role": "assistant", "content": response_text})
                except Exception as e:
                    st.error(f"Ошибка при общении с Gemini: {e}")
                    st.session_state.chat_history.append({"role": "assistant", "content": f"Ошибка: {e}"})
