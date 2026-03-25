import streamlit as st
from google import genai
from modules.text import generate_text
from modules.image import generate_image
from modules.music import generate_music
from modules.video import generate_video

# Streamlit App Configuration
st.set_page_config(
    page_title="Gemini Ultimate Bot",
    page_icon="🤖",
    layout="wide"
)

st.title("Gemini Ultimate Bot 🤖")

# Sidebar
with st.sidebar:
    st.header("Настройки")
    api_key = st.text_input("Введите GOOGLE_API_KEY", type="password")

    st.markdown("---")
    if st.button("Очистить историю чата", use_container_width=True):
        if 'chat_session' in st.session_state:
            del st.session_state['chat_session']
        if 'messages' in st.session_state:
            del st.session_state['messages']
        st.success("История очищена!")
        st.rerun()

    st.markdown("---")
    st.markdown("""
    ### Поддерживаемые команды:
    - **Текст**: Обычный диалог
    - **Изображение**: Начни с *нарисуй*, *фото*, *изображение*
    - **Музыка**: Начни с *музыка*, *песня*, *трек*
    - **Видео**: Начни с *видео*, *ролик*
    """)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["type"] == "text":
            st.markdown(message["content"])
        elif message["type"] == "image":
            st.image(message["content"], caption=message["prompt"])
        elif message["type"] == "audio":
            st.audio(message["content"])
        elif message["type"] == "video":
            if isinstance(message["content"], str) and message["content"].startswith("**Ошибка"):
                st.markdown(message["content"])
            else:
                st.video(message["content"])
        elif message["type"] == "error":
            st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Введите ваш запрос..."):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "type": "text", "content": prompt})

    if not api_key:
        error_msg = "**Пожалуйста, введите GOOGLE_API_KEY в боковой панели.**"
        st.chat_message("assistant").markdown(error_msg)
        st.session_state.messages.append({"role": "assistant", "type": "error", "content": error_msg})
        st.stop()

    client = genai.Client(api_key=api_key)

    prompt_lower = prompt.lower().strip()

    with st.chat_message("assistant"):
        # Image Generation
        if prompt_lower.startswith(("нарисуй", "фото", "изображение")):
            with st.spinner("Создаю изображение..."):
                result = generate_image(prompt)
                if isinstance(result, str) and result.startswith("**Ошибка"):
                    st.markdown(result)
                    st.session_state.messages.append({"role": "assistant", "type": "error", "content": result})
                else:
                    st.image(result, caption=prompt)
                    st.session_state.messages.append({"role": "assistant", "type": "image", "content": result, "prompt": prompt})

        # Music Generation
        elif prompt_lower.startswith(("музыка", "песня", "трек")):
            with st.spinner("Создаю музыку..."):
                result = generate_music(prompt)
                if isinstance(result, str) and result.startswith("**Ошибка"):
                    st.markdown(result)
                    st.session_state.messages.append({"role": "assistant", "type": "error", "content": result})
                else:
                    st.audio(result)
                    st.session_state.messages.append({"role": "assistant", "type": "audio", "content": result})

        # Video Generation
        elif prompt_lower.startswith(("видео", "ролик")):
            with st.spinner("Создаю видео..."):
                result = generate_video(prompt)
                if isinstance(result, str) and result.startswith("**Ошибка"):
                    st.markdown(result)
                    st.session_state.messages.append({"role": "assistant", "type": "error", "content": result})
                else:
                    st.video(result)
                    st.session_state.messages.append({"role": "assistant", "type": "video", "content": result})

        # Text Generation
        else:
            with st.spinner("Думаю..."):
                response_placeholder = st.empty()
                full_response = ""

                try:
                    for chunk in generate_text(prompt, client):
                        full_response += chunk
                        response_placeholder.markdown(full_response + "▌")
                    response_placeholder.markdown(full_response)
                    st.session_state.messages.append({"role": "assistant", "type": "text", "content": full_response})
                except Exception as e:
                    error_msg = f"**Непредвиденная ошибка при генерации текста:** {e}"
                    response_placeholder.markdown(error_msg)
                    st.session_state.messages.append({"role": "assistant", "type": "error", "content": error_msg})
