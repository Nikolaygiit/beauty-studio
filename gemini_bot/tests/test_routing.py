from modules.routing import get_route

def test_get_route_image():
    assert get_route("Нарисуй мне кота") == "image"
    assert get_route("Красивое ФОТО природы") == "image"
    assert get_route("сгенерируй ИЗОБРАЖЕНИЕ") == "image"

def test_get_route_music():
    assert get_route("включи музыку") == "music"
    assert get_route("напиши песню") == "music"
    assert get_route("сделай трек") == "music"

def test_get_route_video():
    assert get_route("создай видео") == "video"
    assert get_route("смешной ролик") == "video"

def test_get_route_text_default():
    assert get_route("как дела?") == "text"
    assert get_route("напиши код на python") == "text"
