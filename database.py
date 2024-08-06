import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from models import Base
from loguru import logger

load_dotenv(dotenv_path='.env.dev')

URL_DATABASE = os.getenv("URL_DATABASE")

if not URL_DATABASE:
    logger.error("Database URL not found in environment variables.")
    raise ValueError("Database URL not set in environment variables")

engine = create_engine(URL_DATABASE)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def createDb():
    Base.metadata.create_all(bind=engine)
    logger.success("Updated DB.")
