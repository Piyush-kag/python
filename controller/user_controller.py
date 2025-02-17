from logging_config import logging_config
from loguru import logger
from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from database import get_db
from exception.exception import CustomException
from service import user_service
from schemas import UserBase, UserCreate

router = APIRouter()


@router.post("/users", response_model=UserBase, status_code=status.HTTP_201_CREATED, tags=["One-to-Many/Users"])
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        return user_service.create_user(db, user)
    except CustomException as e:
        raise e
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise CustomException(status_code=500, detail="Internal Server Error")


@router.post("/fetch-users-from-tp-api", status_code=status.HTTP_200_OK, tags=["One-to-Many/Users"])
async def fetch_users_from_third_party_api(db: Session = Depends(get_db)):
    try:
        message = user_service.fetch_and_store_users(db)
        return {"message": message}
    except CustomException as e:
        logger.error(f"CustomException: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise CustomException(status_code=500, detail="Internal Server Error")


@router.get("/users/{user_id}", status_code=status.HTTP_200_OK, tags=["One-to-Many/Users"])
async def read_user_by_id(user_id: int, db: Session = Depends(get_db)):
    try:
        db_user = user_service.get_user(db, user_id)
        if db_user is None:
            raise CustomException(status_code=404, detail='User not found.')
        return db_user
    except CustomException as e:
        raise e
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise CustomException(status_code=500, detail="Internal Server Error")


@router.get("/users/", response_model=List[UserBase], status_code=status.HTTP_200_OK, tags=["One-to-Many/Users"])
async def read_all_users(db: Session = Depends(get_db)):
    logger.info("Getting all users")
    try:
        db_users = user_service.get_users(db)
        if not db_users:
            raise CustomException(status_code=404, detail='No users found.')
        return db_users
    except CustomException as e:
        raise e
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise CustomException(status_code=500, detail="Internal Server Error")


@router.delete("/users/{user_id}", status_code=status.HTTP_200_OK, tags=["One-to-Many/Users"])
async def delete_user_by_id(user_id: int, db: Session = Depends(get_db)):
    try:
        db_user = user_service.delete_user(db, user_id)
        if db_user is None:
            raise CustomException(status_code=404, detail='User not found.')
        return {"detail": "User deleted"}
    except CustomException as e:
        raise e
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise CustomException(status_code=500, detail="Internal Server Error")


@router.get("/byword/{user_word}", status_code=status.HTTP_200_OK, tags=["One-to-Many/Users"])
async def get_username_by_fuzzy_search(user_word: str, db: Session = Depends(get_db)):
    try:
        db_user = user_service.get_user_by_word(db, user_word)
        if db_user is None:
            raise CustomException(status_code=404, detail='User not found.')
        return db_user
    except CustomException as e:
        raise e
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise CustomException(status_code=500, detail="Internal Server Error")


@router.get("/paginated-users/", status_code=status.HTTP_200_OK, tags=["One-to-Many/Users"])
def read_users(limit: int = 5, db: Session = Depends(get_db)):
    try:
        users = user_service.get_users_with_limit(db, limit)
        if not users:
            raise CustomException(status_code=404, detail="No users found")
        return users
    except CustomException as e:
        raise e
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise CustomException(status_code=500, detail="Internal Server Error")
