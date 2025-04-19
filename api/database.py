from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
import config.config as cg

DATABASE_URL = cg.DB_CONNECTION_URL

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autoflush=False)
Base = declarative_base()

# Dependency
def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()