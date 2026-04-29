import urllib.parse
import random

def generate_image(prompt):
    """
    Генерирует ссылку на изображение с помощью Pollinations.ai.
    Возвращает (image_url, None). В случае ошибки возвращает (None, error_message).
    """
    try:
        # Убираем ключевые слова для лучшего результата (опционально, но полезно)
        # prompt_clean = prompt.replace('нарисуй', '').replace('фото', '').replace('изображение', '').strip()

        # URL encode
        encoded_prompt = urllib.parse.quote(prompt)

        # Генерируем случайный сид, чтобы изображения не кешировались
        seed = random.randint(1, 1000000)

        image_url = f"https://pollinations.ai/p/{encoded_prompt}?seed={seed}"

        return image_url, None
    except Exception as e:
        return None, f"Ошибка при генерации изображения: {e}"
