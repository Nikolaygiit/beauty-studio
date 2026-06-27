from modules.routing import get_route

def test_get_route_image():
    assert get_route("Нарисуй мне кота") == "image"
    assert get_route("сделай фото леса") == "image"
    assert get_route("изображение города") == "image"

def test_get_route_music():
    assert get_route("сделай музыку веселую") == "music"
    assert get_route("включи песню") == "music"
    assert get_route("новый трек") == "music"

def test_get_route_video():
    assert get_route("сними видео") == "video"
    assert get_route("сделай ролик") == "video"

def test_get_route_text():
    assert get_route("как дела?") == "text"
    assert get_route("расскажи сказку") == "text"
    assert get_route("напиши код на python") == "text"
