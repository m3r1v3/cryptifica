import os

from sqlalchemy import create_engine

from sqlalchemy.orm import DeclarativeBase, Mapped, Session
from sqlalchemy.orm import mapped_column

engine = create_engine(os.environ.get('DATABASE_URL'))


def create_db():
    Base.metadata.create_engine(engine)


class Base(DeclarativeBase):
    pass


class Favorites(Base):
    __tablename__ = "favorites"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(unique=True, nullable=False)
    favorites: Mapped[str]

    @staticmethod
    def get(user_id: int):
        with Session(engine) as session:
            session.begin()
            try:
                if not session.query(Favorites.id).filter(Favorites.user_id == user_id).count():
                    session.add(Favorites(user_id=user_id, favorites=""))
                    session.commit()
                return session.query(Favorites).filter(Favorites.user_id == user_id).first().favorites
            except Exception:
                session.rollback()

    @staticmethod
    def add(user_id: int, favorite: str):
        with Session(engine) as session:
            session.begin()
            try:
                if session.query(Favorites.id).filter(Favorites.user_id == user_id).count():
                    session.query(Favorites).filter(Favorites.user_id == user_id).update({
                        'favorites': f'{session.query(Favorites).filter(Favorites.user_id == user_id).first().favorites}{favorite},'})
                else:
                    session.add(Favorites(user_id=user_id, favorites=f"{favorite},"))
            except Exception:
                session.rollback()
            else:
                session.commit()

    @staticmethod
    def remove(user_id: int, favorite: str):
        with Session(engine) as session:
            session.begin()
            try:
                if session.query(Favorites.id).filter(Favorites.user_id == user_id).count():
                    session.query(Favorites).filter(Favorites.user_id == user_id).update({
                        'favorites': f'{session.query(Favorites).filter(Favorites.user_id == user_id).first().favorites.replace(f"{favorite},", "")}'})
            except Exception:
                session.rollback()
            else:
                session.commit()

    def __repr__(self):
        return f"Favorites(id={self.id!r}, user_id={self.user_id!r}, favorites={self.favorites!r})"
