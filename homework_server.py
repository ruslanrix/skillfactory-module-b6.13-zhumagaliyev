from bottle import route
from bottle import run
from bottle import HTTPError
from bottle import request

import homework_album


@route("/albums/<artist>")
def albums(artist):
    albums_list = homework_album.find(artist)
    if not albums_list:
        message = "Альбомов {} не найдено".format(artist)
        result = HTTPError(404, message)
    else:
        album_names = [album.album for album in albums_list]
        length = len(album_names)
        result = "Исполнитель: {}.<br>Количество альбомов: {}.<br>Список альбомов:<br>".format(artist, length)
        result += "<br>".join(album_names)
    return result


@route("/albums", method="POST")
def new_album():
    new_data = {
        "artist": request.forms.get("artist"),
        "genre": request.forms.get("genre"),
        "album": request.forms.get("album"),
        "year": request.forms.get("year")
    }
    try:
        new_data["year"] = int(new_data["year"])
    except (ValueError, TypeError):
        return HTTPError(400, "Формат данных для значения year некорректен.")
    try:
        result = homework_album.save_album(new_data)
    except homework_album.IncorrectData as err:
        result = HTTPError(400, str(err))
    except homework_album.EmptyData as err:
        result = HTTPError(400, str(err))
    except homework_album.AlreadyExists as err:
        result = HTTPError(409, str(err))
    return result

if __name__ == "__main__":
    run(host="localhost", port=8080, debug=True)
