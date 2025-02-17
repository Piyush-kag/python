from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from service import post_service
from schemas import PostBase

router = APIRouter()


@router.post("/posts", status_code=status.HTTP_201_CREATED, tags=["Posts"])
async def create_post(post: PostBase, db: Session = Depends(get_db)):
    try:
        return post_service.create_post(db, post)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/posts/{post_id}", status_code=status.HTTP_200_OK, tags=["Posts"])
async def read_post_by_id(post_id: int, db: Session = Depends(get_db)):
    try:
        db_post = post_service.get_post(db, post_id)
        if db_post is None:
            raise HTTPException(status_code=404, detail='Post was not found.')
        return db_post
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/posts/{post_id}", status_code=status.HTTP_200_OK, tags=["Posts"])
async def delete_post_by_id(post_id: int, db: Session = Depends(get_db)):
    try:
        db_post = post_service.delete_post(db, post_id)
        if db_post is None:
            raise HTTPException(status_code=404, detail='Post not found.')
        return {"detail": "Post deleted"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/posts", status_code=status.HTTP_200_OK, tags=["Posts"])
async def read_all_posts(db: Session = Depends(get_db)):
    try:
        db_posts = post_service.get_posts(db)
        if not db_posts:
            raise HTTPException(status_code=404, detail='No posts found.')
        return db_posts
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/posts/byWord/{post_word}", status_code=status.HTTP_200_OK, tags=["Posts"])
async def get_post_title_by_fuzzy_search(post_word: str, db: Session = Depends(get_db)):
    try:
        db_post = post_service.get_post_by_word(db, post_word)
        if not db_post:
            raise HTTPException(status_code=404, detail='Post not found.')
        return db_post
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
