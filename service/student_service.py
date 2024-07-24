from fastapi import HTTPException
from sqlalchemy.orm import Session

from models import Student
from repository import student_repo
from repository.student_repo import add_student_to_course


def add_student(db: Session, student: Student):
    return student_repo.add_student(db, student)


def enroll_student_in_course(db: Session, student_id: int, course_id: int):
    try:
        add_student_to_course(db, student_id, course_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Error enrolling student in course")


def get_all_students(db: Session):
    return student_repo.get_all_students(db)