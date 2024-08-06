# import os
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from dotenv import load_dotenv
# from loguru import logger
# from models import Base
#
# load_dotenv(dotenv_path='.env')
#
# active_profile = os.getenv("ACTIVE_PROFILE")
#
# database_urls = {
#     "local": os.getenv("URL_DATABASE_LOCAL"),
#     "dev": os.getenv("URL_DATABASE_DEV"),
# }
#
# URL_DATABASE = database_urls.get(active_profile)
#
# if not URL_DATABASE:
#     logger.error(f"Database URL not found for the active profile: {active_profile}")
#     raise ValueError(f"Database URL not set for the active profile: {active_profile}")
#
# # Create engine and session
# engine = create_engine(URL_DATABASE)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#
#
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
#
#
# def create_db():
#     Base.metadata.create_all(bind=engine)
#     logger.success("Database created/updated successfully.")


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from loguru import logger
from models import Base
from config import settings

active_profile = settings.active_profile
database_url = settings.database_urls.get(active_profile)

if not database_url:
    logger.error(f"Database URL not found for the active profile: {active_profile}")
    raise ValueError(f"Database URL not set for the active profile: {active_profile}")

# Create engine and session
engine = create_engine(database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_db():
    Base.metadata.create_all(bind=engine)
    logger.success("Database created/updated successfully.")
