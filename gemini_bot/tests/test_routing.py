from modules.routing import route_prompt

def test_route_prompt_image():
    assert route_prompt("нарисуй красивый пейзаж") == "image"
    assert route_prompt("Сделай мне ФОТО кота") == "image"
    assert route_prompt("покажи изображение солнца") == "image"
    assert route_prompt("сгенерируй картинку") == "image"

def test_route_prompt_music():
    assert route_prompt("создай музыку для релакса") == "music"
    assert route_prompt("напиши веселую песню") == "music"
    assert route_prompt("включи крутой трек") == "music"
    assert route_prompt("нужна мелодия") == "music"

def test_route_prompt_video():
    assert route_prompt("сделай видео про космос") == "video"
    assert route_prompt("сними ролик") == "video"
    assert route_prompt("крутой клип") == "video"

def test_route_prompt_text():
    assert route_prompt("Привет, как дела?") == "text"
    assert route_prompt("Что такое искусственный интеллект?") == "text"
    assert route_prompt("расскажи сказку") == "text"
