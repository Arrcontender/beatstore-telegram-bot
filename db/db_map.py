from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Beats(Base):
    __tablename__ = 'beats'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    url = Column(String, nullable=False)
    genre = Column(String)
    leasing = Column(Integer)
    exclusive = Column(Integer)

    def __repr__(self):
        return f"Beats(name={self.name!r}, url={self.url!r}, genre={self.genre!r}, " \
               f"leasing={self.leasing!r}, exclusive={self.exclusive!r})"


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String)
    name = Column(String)
    admin = Column(Boolean, default=False)
