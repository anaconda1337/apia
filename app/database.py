from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.settings import get_postgres_settings


def create_database_connection():
    postgres_settings = get_postgres_settings()
    engine = create_engine(
        f"postgresql://{postgres_settings.user}:{postgres_settings.password}@{postgres_settings.host}:{postgres_settings.port}/{postgres_settings.database}"  # noqa
    )
    return engine


def create_session():
    engine = create_database_connection()
    Session = sessionmaker(bind=engine)
    return Session()


def get_db_session() -> sessionmaker:
    session = create_session()
    try:
        yield session
    finally:
        session.close()
