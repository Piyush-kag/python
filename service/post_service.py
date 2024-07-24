from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session
from models import Post
from repository import post_repo
from schemas import PostBase


def create_post(db: Session, post: PostBase):
    db_post = Post(
        id=post.id,
        title=post.title,
        content=post.content,
        user_id=post.user_id
    )
    return post_repo.create_post(db, db_post)


def get_post(db: Session, post_id: int):
    return post_repo.get_post(db, post_id)


def get_posts(db: Session):
    return post_repo.get_posts(db)


def delete_post(db: Session, post_id: int):
    return post_repo.delete_post(db, post_id)


def get_post_by_word(db: Session, post_word: str):
    posts = db.query(Post.title).filter(func.lower(Post.title).like(f'%{post_word.lower()}%')).all()
    if not posts:
        raise HTTPException(status_code=404, detail=f'Post not found with word {post_word}')
    posts = [posts[0] for posts in posts]
    return posts
