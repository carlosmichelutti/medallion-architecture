from configuration.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(url=settings.database.database_url, echo=False, future=True)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def get_db_session():
    with SessionLocal() as session:
        return session

engine = get_db_session().get_bind()