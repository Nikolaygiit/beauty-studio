from modules.routing import get_route

def test_get_route_image():
    assert get_route("Нарисуй мне красивый пейзаж") == "image"
    assert get_route("Покажи фото кота") == "image"
    assert get_route("Сгенерируй фотографию города") == "image"
    assert get_route("Создай изображение собаки") == "image"

def test_get_route_music():
    assert get_route("Напиши мне музыку для расслабления") == "music"
    assert get_route("Сочини веселую песню") == "music"
    assert get_route("Сделай крутой трек") == "music"

def test_get_route_video():
    assert get_route("Сделай видео с котиками") == "video"
    assert get_route("Создай рекламный ролик") == "video"

def test_get_route_text():
    assert get_route("Привет, как дела?") == "text"
    assert get_route("Напиши код на питоне") == "text"
    assert get_route("Расскажи сказку") == "text"
