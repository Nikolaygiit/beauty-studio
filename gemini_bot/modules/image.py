import streamlit as st
import requests
from io import BytesIO
from PIL import Image

def render_image_module():
    st.header("🖼️ Генерация изображений (Pollinations.ai)")
    st.write("Генерация изображений не требует API ключа Gemini, так как использует сторонний сервис Pollinations.ai.")

    prompt = st.text_area("Описание изображения:", "Котенок программист за ноутбуком, киберпанк, высокое качество, 4k")

    col1, col2 = st.columns(2)
    with col1:
        width = st.number_input("Ширина", min_value=256, max_value=2048, value=1024, step=64)
    with col2:
        height = st.number_input("Высота", min_value=256, max_value=2048, value=1024, step=64)

    seed = st.number_input("Seed (для повторяемости, 0 - случайный)", min_value=0, value=0)

    if st.button("Сгенерировать изображение"):
        if prompt:
            with st.spinner("Создаю изображение..."):
                try:
                    # Construct URL for Pollinations.ai API
                    # Pollinations API usage: https://image.pollinations.ai/prompt/{prompt}?width={width}&height={height}&seed={seed}&nologo=true
                    encoded_prompt = requests.utils.quote(prompt)
                    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={width}&height={height}&nologo=true"
                    if seed != 0:
                        url += f"&seed={seed}"

                    response = requests.get(url, timeout=30)
                    response.raise_for_status()

                    image = Image.open(BytesIO(response.content))
                    st.image(image, caption=f"Промпт: {prompt}")

                    # Provide download button
                    img_bytes = BytesIO()
                    image.save(img_bytes, format='PNG')
                    st.download_button(
                        label="⬇️ Скачать изображение",
                        data=img_bytes.getvalue(),
                        file_name="generated_image.png",
                        mime="image/png"
                    )
                except Exception as e:
                    st.error(f"Ошибка при генерации изображения: {e}")
        else:
            st.warning("Пожалуйста, введите описание.")
