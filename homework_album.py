import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from bottle import HTTPError

DB_PATH = "sqlite:///albums.sqlite3"
Base = declarative_base()


class Album(Base):
    """
    Описывает структуру таблицы album для хранения записей музыкальной библиотеки
    """

    __tablename__ = "album"

    id = sa.Column(sa.INTEGER, primary_key=True)
    year = sa.Column(sa.INTEGER)
    artist = sa.Column(sa.TEXT)
    genre = sa.Column(sa.TEXT)
    album = sa.Column(sa.TEXT)

class Error(Exception):
    pass

class IncorrectData(Error):
    pass

class EmptyData(Error):
    pass

class AlreadyExists(Error):
    pass

def connect_db():
    """
    Устанавливает соединение к базе данных, создает таблицу, если их еще нет и возвращает объект сессии
    """
    engine = sa.create_engine(DB_PATH)
    Base.metadata.create_all(engine)
    session = sessionmaker(engine)
    return session()


def find(artist):
    """
    Находит все альбомы в базе данных по заданному артисту
    """
    session = connect_db()
    albums = session.query(Album).filter(Album.artist == artist).all()
    return albums


def save_album(new_data):
    """
    Проверяет и сохраняет новый альбом
    """
    session = connect_db()
    if not isinstance(new_data["artist"], str) or not isinstance(new_data["genre"], str) or not isinstance(new_data["album"], str):
        raise IncorrectData("Ввод некорректных данных")
    if not new_data["artist"] or not new_data["genre"] or not new_data["album"]:
        raise EmptyData("Ввод пустых данных")
    check_album = session.query(Album).filter(
            Album.artist == new_data["artist"]).filter(Album.album == new_data["album"]).first()
    if not check_album:
        session.add(Album(year=new_data["year"], artist=new_data["artist"], genre=new_data["genre"],
                              album=new_data["album"]))
        session.commit()
        result = "Данные сохранены"
    else:
        raise AlreadyExists("Альбом уже существует в базе")
    return result
