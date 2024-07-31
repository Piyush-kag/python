from fastapi import APIRouter
import logging
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from exception.exception import CustomException
from service import student_service
from schemas import StudentBase, StudentCreate
from loguru import logger

router = APIRouter()


@router.post("/student", response_model=StudentBase, status_code=status.HTTP_201_CREATED,
             tags=["Many-to-Many/Students"])
async def add_student(student: StudentCreate, db: Session = Depends(get_db)):
    try:
        logger.info(f"Adding {student.student_name}")
        return student_service.add_student(db, student)
    except HTTPException as e:
        logger.error(f"Exception while adding student {student.student_name} !! {e.detail}")
        raise CustomException(status_code=e.status_code, detail=e.detail)


@router.post("/enroll/student", status_code=status.HTTP_200_OK, tags=["Many-to-Many/Students"])
async def enroll_student(student_id: int, course_id: int, db: Session = Depends(get_db)):
    try:
        logger.info(f"Enrolling student with id = {student_id} with course id = {course_id}")
        student_service.enroll_student_in_course(db, student_id, course_id)
        return {"message": "Student enrolled in course successfully"}
    except HTTPException as e:
        logger.error(f"Exception while enrolling students in course. !! {e.detail}")
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@router.get("/students", response_model=List[StudentBase], status_code=status.HTTP_200_OK,
            tags=["Many-to-Many/Students"])
async def get_all_students(db: Session = Depends(get_db)):
    logging.info("Getting all students")
    try:
        students = student_service.get_all_students(db)
        if not students:
            raise HTTPException(status_code=404, detail='No students found.')
        return students
    except HTTPException as e:
        logger.error(f"Exception while fetching students = {e.detail}")
        raise CustomException(status_code=e.status_code, detail=e.detail)
