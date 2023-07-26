from sqlalchemy import create_engine
from sqlalchemy.sql.expression import exists

from sqlalchemy.orm import DeclarativeBase, Mapped, Session
from sqlalchemy.orm import mapped_column

engine = create_engine(
    "postgresql://postgres:MDCW5YRm76OIMdtk9kEC@containers-us-west-195.railway.app:5767/railway")  # create_engine(os.environ.get('DATABASE_URL'))


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
            except:
                session.rollback()
                raise

    @staticmethod
    def add(user_id: int, favorite: str):
        with Session(engine) as session:
            session.begin()
            try:
                if session.query(exists().where(Favorites.user_id == user_id)).scalar():
                    session.query(Favorites).filter(Favorites.user_id == user_id).update({
                        'favorites': f'{session.query(Favorites).filter(Favorites.user_id == user_id).first().favorites}{favorite},'})
                else:
                    session.add(Favorites(user_id=user_id, favorites=f"{favorite},"))
            except:
                session.rollback()
            else:
                session.commit()

    @staticmethod
    def remove(user_id: int, favorite: str):
        with Session(engine) as session:
            session.begin()
            try:
                if session.query(exists().where(Favorites.user_id == user_id)).scalar():
                    session.query(Favorites).filter(Favorites.user_id == user_id).update({
                        'favorites': f'{session.query(Favorites).filter(Favorites.user_id == user_id).first().favorites.replace(f"{favorite},", "")}'})
            except:
                session.rollback()
            else:
                session.commit()

    def __repr__(self):
        return f"Favorites(id={self.id!r}, user_id={self.user_id!r}, favorites={self.favorites!r})"
