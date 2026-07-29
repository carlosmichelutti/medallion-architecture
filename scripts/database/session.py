from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from scripts.configuration.config import settings

engine = create_engine(url=settings.database.database_url, echo=False, future=True)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def get_db_session():
    return SessionLocal()