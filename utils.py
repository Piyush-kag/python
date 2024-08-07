from fastapi import Depends
from fastapi_users import db
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt, JWTError
from starlette import status
from schemas import TokenData, UserInDB
from service import user_service
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "d0bff72efbb95ef8a557e7f88055912c3fdd4c212c31d3f922bcd64712464c46"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expired_delta: timedelta or None = None):
    to_encode = data.copy()
    if expired_delta:
        expire = datetime.utcnow() + expired_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt


class HttpException(Exception):
    pass


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credential_exception = HttpException(status_code=status.Http_401_UNAUTHORIZED,
                                         detail="Could not validate credentials",
                                         headers={"WWW-Authenticate": "Bearer"})
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms={ALGORITHM})
        username: str = payload.get("sub")
        if username is None:
            raise credential_exception

        token_data = TokenData(username=username)
    except JWTError:
        raise credential_exception

    user = user_service.get_user(db, username=token_data.id)
    if user is None:
        raise credential_exception

    return user


def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    return token_data


async def get_current_active_user(current_user: UserInDB = Depends(get_current_user)):
    if current_user.disabled:
        raise HttpException(status_code=400, detail="Inactive user")

    return current_user
