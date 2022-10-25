import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from .db_map import Base

host = os.getenv('db_host')
password = os.getenv('db_pass')
database = os.getenv('db_name')

engine = create_engine(f'postgresql+psycopg2://postgres:{password}@{host}/{database}')

session = scoped_session(sessionmaker(bind=engine))
Base.query = session.query_property()

Base.metadata.create_all(bind=engine)

