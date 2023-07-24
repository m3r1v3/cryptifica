import os
import random

from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine(os.environ.get('DATABASE_URL'))
Base = declarative_base()

Session = sessionmaker(bind=engine)
session = Session()


class Favorites(Base):
    __tablename__ = "favorites"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, unique=True, nullable=False)
    favorites = Column(String, unique=False, nullable=True)

    @staticmethod
    def add(user_id: str, favorites: str):
        session.add(Favorites(id=random.randint(1, 2147483647), user_id=user_id, favorites=favorites))
        session.commit()

    def __repr__(self):
        return "<Favorites(id='%s', user_id='%s', favorites='%s')>" % (self.id, self.role, self.server)