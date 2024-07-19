import logging
from sqlite3 import IntegrityError
import requests
from sqlalchemy.orm import Session
from models import User
from repository import user_repo
from fastapi import HTTPException
from sqlalchemy.sql import func
    

def create_user(db: Session, user: User):
    return user_repo.create_user(db, user)

def get_user(db: Session, user_id: int):
    return user_repo.get_user(db, user_id)

def get_users(db: Session):
    return user_repo.get_users(db)

def delete_user(db: Session, user_id: int):
    return user_repo.delete_user(db, user_id)

def get_user_by_word(db: Session, user_word: str):
    usernames = db.query(User.username).filter(func.lower(User.username).like(f'%{user_word.lower()}%')).all()
    if not usernames:
        raise HTTPException(status_code=404, detail=f'User not found with word {user_word}')
    usernames = [username[0] for username in usernames]
    return usernames

def fetch_and_store_users(db: Session):
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
        except IntegrityError:
            logging.warning(f"User with id {user.id} already exists in the database. Skipping insertion.")
            db.rollback()

    return "Users have been successfully fetched and stored."