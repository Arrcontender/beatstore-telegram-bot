from sqlalchemy.exc import IntegrityError

from .db_engine import session
from .db_map import User, Beats


def register_user(message):
    username = message.from_user.username if message.from_user.username else None
    user = User(id=int(message.from_user.id), username=username, name=message.from_user.full_name)
    session.add(user)
    try:
        session.commit()
        return True
    except IntegrityError:
        session.rollback()
        return False


def filter_by_genre_from_db(value):
    genre = session.query(Beats.name, Beats.url,
                          Beats.leasing, Beats.genre,
                          Beats.exclusive).filter(Beats.genre == value).all()
    return genre


def show_all_beats():
    all_beats = session.query(Beats.name, Beats.url,
                              Beats.leasing, Beats.genre, Beats.exclusive).all()
    return all_beats
