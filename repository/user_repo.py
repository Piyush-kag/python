from sqlalchemy.orm import Session
from models import User
from sqlalchemy.orm import joinedload
from schemas import UserCreate


def create_user(db: Session, user: UserCreate) -> User:
    db_user = User(username=user.username, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_users(db: Session):
    return db.query(User).options(joinedload(User.posts)).all()


def delete_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
        return user
    return None
