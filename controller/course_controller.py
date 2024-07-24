from loguru import logger
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from exception.exception import CustomException
from service import course_service
from schemas import CourseBase, CourseCreate

router = APIRouter()


@router.post("/course", response_model=CourseBase, status_code=status.HTTP_201_CREATED, tags=["Course"])
async def add_course(course: CourseCreate, db: Session = Depends(get_db)):
    try:
        logger.info("Process starting to creating course.")
        return course_service.add_course(db, course)
    except HTTPException as e:
        logger.error("Exception while adding course.")
        raise CustomException(status_code=e.status_code, detail=e.detail)


@router.get("/course", response_model=List[CourseBase], status_code=status.HTTP_200_OK, tags=["Course"])
async def get_all_courses(db: Session = Depends(get_db)):
    logger.info("Getting all courses")
    try:
        students = course_service.get_all_course(db)
        if not students:
            logger.info("No course found.")
            raise HTTPException(status_code=404, detail='No course found.')
        logger.success(f"Fetched all courses = {students}")
        return students
    except HTTPException as e:
        logger.error("Exception while fetching courses.")
        raise CustomException(status_code=e.status_code, detail=e.detail)
