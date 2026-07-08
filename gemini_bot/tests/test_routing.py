from modules.routing import route_prompt

def test_route_prompt_image():
    assert route_prompt("Нарисуй красивый пейзаж") == "image"
    assert route_prompt("Сделай фото кота") == "image"
    assert route_prompt("Покажи фотографию машины") == "image"
    assert route_prompt("Сгенерируй изображение города") == "image"

def test_route_prompt_music():
    assert route_prompt("Сочини музыку для отдыха") == "music"
    assert route_prompt("Сделай веселую песню") == "music"
    assert route_prompt("Напиши классный трек") == "music"

def test_route_prompt_video():
    assert route_prompt("Сделай видео с собакой") == "video"
    assert route_prompt("Покажи короткий ролик") == "video"

def test_route_prompt_text():
    assert route_prompt("Привет, как дела?") == "text"
    assert route_prompt("Расскажи сказку") == "text"
    assert route_prompt("Что такое фотосинтез?") == "text" # "фото" is part of the word, but word boundary should prevent 'image' match
