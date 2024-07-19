import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from exception.exception import CustomException
from service import user_service
from schemas import UserBase

router = APIRouter()

@router.post("/users", status_code=status.HTTP_201_CREATED, tags=["Users"])
async def create_user(user: UserBase, db: Session = Depends(get_db)):
   try:
        return user_service.create_user(db, user)
   except HTTPException as e:
        raise CustomException(status_code=e.status_code, detail=e.detail)
   except Exception as e:
        raise CustomException(status_code=500, detail="Internal Server Error")

@router.post("/fetch-users", status_code=status.HTTP_200_OK, tags=["Users"])
async def fetch_users(db: Session = Depends(get_db)):
    try:
        message = user_service.fetch_and_store_users(db)
        return {"message": message}
    except HTTPException as e:
        logging.error(f"HTTPException: {e.detail}")
        raise e
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
@router.get("/users/{user_id}", status_code=status.HTTP_200_OK, tags=["Users"])
async def read_user_by_id(user_id: int, db: Session = Depends(get_db)):
    try: 
        db_user = user_service.get_user(db, user_id)
        if db_user is None:
            raise HTTPException(status_code=404, detail='User not found.')
        return db_user
    except HTTPException as e:
        raise CustomException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        raise CustomException(status_code=500, detail="Internal Server Error")

@router.get("/users/", status_code=status.HTTP_200_OK, tags=["Users"])
async def read_all_users(db: Session = Depends(get_db)):
    try:
        db_users = user_service.get_users(db)
        if not db_users:
            raise HTTPException(status_code=404, detail='No users found.')
        return db_users
    except HTTPException as e:
        raise CustomException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        raise CustomException(status_code=500, detail="Internal Server Error")

@router.delete("/{user_id}", status_code=status.HTTP_200_OK, tags=["Users"])
async def delete_user_by_id(user_id: int, db: Session = Depends(get_db)):
    try:
        db_user = user_service.delete_user(db, user_id)
        if db_user is None:
            raise HTTPException(status_code=404, detail='User not found.')
        return {"detail": "User deleted"}
    except HTTPException as e:
        raise CustomException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        raise CustomException(status_code=500, detail="Internal Server Error")

@router.get("/byword/{user_word}", status_code=status.HTTP_200_OK, tags=["Users"])
async def get_username_by_fuzzy_search(user_word: str, db: Session = Depends(get_db)):
    try:
        db_user = user_service.get_user_by_word(db, user_word)
        if db_user is None:
            raise HTTPException(status_code=404, detail='User not found.')
        return db_user
    except HTTPException as e:
        raise CustomException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        raise CustomException(status_code=500, detail="Internal Server Error")