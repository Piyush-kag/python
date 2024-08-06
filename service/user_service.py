from logging_config import logging_config
from loguru import logger
from sqlite3 import IntegrityError
import requests
from sqlalchemy.orm import Session
from exception.exception import CustomException
from models import User
from repository import user_repo
from schemas import UserCreate


def create_user(db: Session, user: UserCreate):
    try:
        return user_repo.create_user(db, user)
    except IntegrityError as e:
        logger.error(f"IntegrityError: {e}")
        raise CustomException(status_code=400, detail="User already exists.")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise CustomException(status_code=500, detail="Internal Server Error")


def get_user(db: Session, user_id: int):
    try:
        user = user_repo.get_user(db, user_id)
        if not user:
            raise CustomException(status_code=404, detail="User not found.")
        return user
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise CustomException(status_code=500, detail=f"No user found with id : {user_id}")


def get_users(db: Session):
    try:
        users = user_repo.get_users(db)
        if not users:
            raise CustomException(status_code=404, detail="No users found.")
        return users
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise CustomException(status_code=500, detail="Internal Server Error")


def delete_user(db: Session, user_id: int):
    try:
        user = user_repo.delete_user(db, user_id)
        if user is None:
            raise CustomException(status_code=404, detail=f"User not found with user_id : {user_id}")
        return {"detail": "User and related posts deleted"}
    except CustomException as e:
        raise e
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise CustomException(status_code=500, detail="Internal Server Error")


def get_user_by_word(db: Session, user_word: str):
    try:
        usernames = user_repo.get_user_by_word(db, user_word)
        if not usernames:
            raise CustomException(status_code=404, detail=f'User not found with word {user_word}')
        return [username[0] for username in usernames]
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise CustomException(status_code=500, detail="Internal Server Error")


def fetch_and_store_users(db: Session):
    try:
        response = requests.get("https://jsonplaceholder.typicode.com/users")
        response.raise_for_status()
        users_data = response.json()

        for user_data in users_data:
            user = User(
                id=user_data['id'],
                username=user_data['username'],
                email=user_data['email'],
            )

            try:
                create_user(db, user)
            except CustomException as e:
                logger.warning(f"Skipping user with id {user.id} due to error: {e.detail}")
                db.rollback()
            except IntegrityError:
                logger.warning(f"User with id {user.id} already exists in the database. Skipping insertion.")
                db.rollback()

        return "Users have been successfully fetched and stored."
    except requests.RequestException as e:
        logger.error(f"HTTP error: {e}")
        raise CustomException(status_code=500, detail="Failed to fetch users from the third-party API.")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise CustomException(status_code=500, detail="Internal Server Error")


def get_users_with_limit(db: Session, limit: int):
    try:
        logger.info(f"Finding Users...")
        users = db.query(User).limit(limit).all()
        if not users:
            raise CustomException(status_code=404, detail="No users found")
        return users
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise CustomException(status_code=500, detail="Internal Server Error")
