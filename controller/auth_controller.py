from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm
from loguru import logger

import utils
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas import Token
from models import User

router = APIRouter()


@router.post("/token", response_model=Token)
def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not utils.verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=utils.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = utils.create_access_token(data={"sub": user.username})
    logger.success("User Login Successfully.")
    logger.success(f"Access_Token : {access_token}")
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me")
def read_users_me(current_user: User = Depends(utils.get_current_user)):
    return [{"item_id": 1, "owner": current_user}]
