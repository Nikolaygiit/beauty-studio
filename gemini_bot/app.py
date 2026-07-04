import streamlit as st
import os
from modules.routing import get_route
from modules.text import get_gemini_client, get_chat_session, generate_text_stream
from modules.image import generate_image
from modules.music import generate_music
from modules.video import generate_video

# Streamlit UI Configuration
st.set_page_config(page_title="Gemini Ultimate Bot", page_icon="✨", layout="wide")
st.title("✨ Gemini Ultimate Bot (Текст, Изображения, Музыка, Видео)")

# Sidebar for configuration
with st.sidebar:
    st.header("Настройки")
    api_key_input = st.text_input("Введите ваш Google API Key", type="password")

    if st.button("Очистить историю чата"):
        st.session_state.chat_history = []
        st.session_state.chat_session = None
        st.session_state.gemini_client = None
        st.rerun()

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "current_api_key" not in st.session_state:
    st.session_state.current_api_key = ""
if "gemini_client" not in st.session_state:
    st.session_state.gemini_client = None
if "chat_session" not in st.session_state:
    st.session_state.chat_session = None

# Update Gemini client if API key changes
if api_key_input and api_key_input != st.session_state.current_api_key:
    st.session_state.current_api_key = api_key_input
    client, error = get_gemini_client(api_key_input)
    if error:
        st.sidebar.error(error)
        st.session_state.gemini_client = None
        st.session_state.chat_session = None
    else:
        st.session_state.gemini_client = client
        chat, chat_error = get_chat_session(client)
        if chat_error:
            st.sidebar.error(chat_error)
            st.session_state.chat_session = None
        else:
             st.session_state.chat_session = chat

# Render chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        if message["type"] == "text":
            st.markdown(message["content"])
        elif message["type"] == "image":
             st.markdown(message["content"])
             if "media_path" in message and message["media_path"]:
                 st.image(message["media_path"])
        elif message["type"] == "music":
             st.markdown(message["content"])
             if "media_path" in message and message["media_path"]:
                 st.audio(message["media_path"])
        elif message["type"] == "video":
             st.markdown(message["content"])
             if "media_path" in message and message["media_path"]:
                 st.video(message["media_path"])

# Chat input
if prompt := st.chat_input("Введите сообщение (например: 'нарисуй кота', 'сочини музыку', 'сделай видео леса')..."):
    if not st.session_state.current_api_key:
        st.error("Пожалуйста, введите API ключ в боковой панели.")
        st.stop()

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.chat_history.append({"role": "user", "type": "text", "content": prompt})

    # Route request
    route = get_route(prompt)

    with st.chat_message("assistant"):
        if route == "image":
            with st.spinner("Создаю изображение..."):
                 image_url, error = generate_image(prompt)
                 if error:
                      st.error(error)
                      st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": error})
                 else:
                      st.image(image_url)
                      content = "Вот ваше изображение:"
                      st.markdown(content)
                      st.session_state.chat_history.append({
                           "role": "assistant",
                           "type": "image",
                           "content": content,
                           "media_path": image_url
                      })

        elif route == "music":
             with st.spinner("Создаю музыку... (это может занять время)"):
                  audio_path, error = generate_music(prompt)
                  if error:
                       st.error(error)
                       st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": error})
                  else:
                       st.audio(audio_path)
                       content = "Вот ваша музыка:"
                       st.markdown(content)
                       st.session_state.chat_history.append({
                            "role": "assistant",
                            "type": "music",
                            "content": content,
                            "media_path": audio_path
                       })

        elif route == "video":
             with st.spinner("Создаю видео... (это может занять время)"):
                  video_path, error = generate_video(prompt)
                  if error:
                       st.error(error)
                       st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": error})
                  else:
                       st.video(video_path)
                       content = "Вот ваше видео:"
                       st.markdown(content)
                       st.session_state.chat_history.append({
                            "role": "assistant",
                            "type": "video",
                            "content": content,
                            "media_path": video_path
                       })

        else: # route == "text"
             if not st.session_state.chat_session:
                  st.error("Сессия чата не инициализирована. Проверьте API ключ.")
             else:
                  full_response = ""
                  message_placeholder = st.empty()
                  try:
                      # Generate streaming text
                      for chunk in generate_text_stream(st.session_state.chat_session, prompt):
                           if isinstance(chunk, dict) and "error" in chunk:
                                st.error(chunk["error"])
                                full_response += "\n" + chunk["error"]
                           elif chunk.text:
                                full_response += chunk.text
                                message_placeholder.markdown(full_response + "▌")
                      message_placeholder.markdown(full_response)
                      st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": full_response})
                  except Exception as e:
                      st.error(f"Непредвиденная ошибка: {e}")
