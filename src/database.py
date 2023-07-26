import os
import random

from sqlalchemy import create_engine

from sqlalchemy.orm import DeclarativeBase, Mapped, Session
from sqlalchemy.orm import mapped_column

engine = create_engine(os.environ.get('DATABASE_URL'))
session = Session(engine)


class Base(DeclarativeBase):
    pass


class Favorites(Base):
    __tablename__ = "favorites"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[str] = mapped_column(nullable=False)
    favorites: Mapped[str]

    @staticmethod
    def add_favorite(self, user_id, favorites):
        pass

    @staticmethod
    def remove_favorite(self):
        pass

    def __repr__(self):
        return "<Favorites(id='%s', user_id='%s', favorites='%s')>" % (self.id, self.user_id, self.favorites)
