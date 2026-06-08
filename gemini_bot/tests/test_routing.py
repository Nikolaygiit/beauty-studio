from modules.routing import route_prompt

def test_route_image():
    assert route_prompt("нарисуй кота") == "image"
    assert route_prompt("сгенерируй картинку леса") == "image"
    assert route_prompt("сделай фото") == "image"

def test_route_music():
    assert route_prompt("создай музыку") == "music"
    assert route_prompt("спой песню") == "music"
    assert route_prompt("крутой трек") == "music"

def test_route_video():
    assert route_prompt("сделай видео") == "video"
    assert route_prompt("смешной ролик") == "video"

def test_route_text():
    assert route_prompt("привет как дела") == "text"
    assert route_prompt("напиши код на питоне") == "text"
    assert route_prompt("расскажи сказку") == "text"

def test_route_case_insensitivity():
    assert route_prompt("НАРИСУЙ") == "image"
    assert route_prompt("МуЗыК") == "music"
