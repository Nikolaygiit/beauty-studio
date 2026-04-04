import streamlit as st
from modules import text, image, music, video

st.set_page_config(page_title="Gemini Ultimate Bot", page_icon="🤖", layout="wide")

st.title("🤖 Gemini Ultimate Bot")
st.markdown("Универсальный бот: генерирует текст, изображения, музыку и видео!")

# Sidebar for API Key and options
with st.sidebar:
    st.header("Настройки")
    api_key = st.text_input("Введите GOOGLE_API_KEY", type="password")

    if st.button("Очистить историю чата"):
        if "chat_session" in st.session_state:
            del st.session_state.chat_session
        if "messages" in st.session_state:
            st.session_state.messages = []
        st.success("История очищена!")

# Initialize session state for UI messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Verify API key
if not api_key:
    st.warning("Пожалуйста, введите GOOGLE_API_KEY в боковой панели для начала работы.")
    st.stop()

# Initialize Gemini Chat Session
if "chat_session" not in st.session_state:
    try:
        client = text.get_client(api_key)
        st.session_state.chat_session = text.start_chat(client)
    except Exception as e:
        st.error(f"Ошибка инициализации Gemini: {e}")
        st.stop()

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg["type"] == "text":
            st.markdown(msg["content"])
        elif msg["type"] == "image":
            st.image(msg["content"])
        elif msg["type"] == "audio":
            if str(msg["content"]).startswith("Ошибка"):
                st.error(msg["content"])
            else:
                st.audio(msg["content"])
        elif msg["type"] == "video":
            if str(msg["content"]).startswith("Ошибка"):
                st.error(msg["content"])
            else:
                st.video(msg["content"])

# Chat input
if prompt := st.chat_input("Напишите сообщение..."):
    # Display user message
    st.session_state.messages.append({"role": "user", "type": "text", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Determine generation type based on keywords
    prompt_lower = prompt.lower()

    with st.chat_message("assistant"):
        if any(keyword in prompt_lower for keyword in ['нарисуй', 'фото', 'изображение']):
            with st.spinner("Генерирую изображение..."):
                img_url = image.generate_image_url(prompt)
                st.image(img_url)
                st.session_state.messages.append({"role": "assistant", "type": "image", "content": img_url})

        elif any(keyword in prompt_lower for keyword in ['музыка', 'песня', 'трек']):
            with st.spinner("Генерирую музыку..."):
                audio_result = music.generate_music(prompt)
                if isinstance(audio_result, str) and audio_result.startswith("Ошибка"):
                     st.error(audio_result)
                else:
                     st.audio(audio_result)
                st.session_state.messages.append({"role": "assistant", "type": "audio", "content": audio_result})

        elif any(keyword in prompt_lower for keyword in ['видео', 'ролик']):
            with st.spinner("Генерирую видео..."):
                video_result = video.generate_video(prompt)
                if isinstance(video_result, str) and video_result.startswith("Ошибка"):
                     st.error(video_result)
                else:
                     st.video(video_result)
                st.session_state.messages.append({"role": "assistant", "type": "video", "content": video_result})

        else:
            # Default to text generation via Gemini
            with st.spinner("Генерирую ответ..."):
                response_container = st.empty()
                full_response = ""
                for chunk in text.generate_text_stream(st.session_state.chat_session, prompt):
                    full_response += chunk
                    response_container.markdown(full_response + "▌")
                response_container.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "type": "text", "content": full_response})
