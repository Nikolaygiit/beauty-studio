from modules.routing import get_route

def test_get_route_image():
    assert get_route("Нарисуй мне кота") == "image"
    assert get_route("Сделай фото леса") == "image"
    assert get_route("Сгенерируй изображение города") == "image"
    assert get_route("сгенерируй картинку собаки") == "image"

def test_get_route_music():
    assert get_route("Включи музыку") == "music"
    assert get_route("Спой песню") == "music"
    assert get_route("Сделай крутой трек") == "music"
    assert get_route("Хочу много песен") == "music"

def test_get_route_video():
    assert get_route("Сделай видео про космос") == "video"
    assert get_route("Сгенерируй ролик") == "video"

def test_get_route_text():
    assert get_route("Привет, как дела?") == "text"
    assert get_route("Что такое фотосинтез?") == "text"
    assert get_route("Напиши код на питоне") == "text"

def test_get_route_mixed():
    # It should match the first condition that returns true in the routing logic
    # Right now logic goes: image -> music -> video -> text
    assert get_route("Нарисуй видео") == "image"
    assert get_route("Сделай музыку для видео") == "music"
