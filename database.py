from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
from loguru import logger

URL_DATABASE = "mysql+pymysql://root:root@localhost:3306/BlogApplication"

engine = create_engine(
    URL_DATABASE,
    pool_size=5,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=1800
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def createDb():
    Base.metadata.create_all(bind=engine)
    logger.success("Creating tables")
