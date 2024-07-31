from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
from loguru import logger

URL_DATABASE = "mysql+pymysql://root:root@localhost:3306/BlogApplication"

engine = create_engine(
    URL_DATABASE
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def createDb():
    Base.metadata.create_all(bind=engine)
    logger.success("Creating tables")
