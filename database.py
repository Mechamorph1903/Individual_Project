# database.py
from sqlalchemy import create_engine, event
from sqlalchemy.orm import DeclarativeBase, sessionmaker

engine = create_engine(
    "sqlite:///./images.db", connect_args={"check_same_thread": False}
)


@event.listens_for(engine, "connect")
def enableForeignKeys(dbapiConnection, connectionRecord):
    cursor = dbapiConnection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass
