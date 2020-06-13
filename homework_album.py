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


class EmptyData(Exception):
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
    try:
        session = connect_db()
        new_data["year"] = int(new_data["year"])
        if (not new_data["artist"] or not new_data["genre"] or not new_data["album"]):
            raise EmptyData("Ввод пустых данных")
    except (ValueError, TypeError):
        result = HTTPError(400, "Формат данных для значения year некорректен.")
    except EmptyData as err:
        result = HTTPError(400, "Ввод пустых данных")

    else:
        check = session.query(Album).filter(
            Album.artist == new_data["artist"]).filter(Album.album == new_data["album"]).first()
        # print(check.album, new_data["album"])
        if not check:
            session.add(Album(year=new_data["year"], artist=new_data["artist"], genre=new_data["genre"],
                              album=new_data["album"]))
            session.commit()
            result = "Данные сохранены"
        else:
            result = HTTPError(409, "Альбом уже существует в базе")
    return result
