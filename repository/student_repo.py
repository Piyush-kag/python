from sqlalchemy.orm import Session, joinedload
from schemas import StudentCreate
from loguru import logger
from models import Student, student_course_association


def add_student(db: Session, student: StudentCreate) -> Student:
    db_student = Student(student_name=student.student_name)
    db.add(db_student)
    db.commit()
    logger.success("Added student successfully.")
    db.refresh(db_student)

    return db_student


def add_student_to_course(db: Session, student_id: int, course_id: int):
    db.execute(
        student_course_association.insert().values(student_id=student_id, course_id=course_id)
    )
    db.commit()
    logger.success("Added student to course successfully.")


def get_all_students(db: Session):
    logger.info("getting students ready.")
    students_data = db.query(Student).options(joinedload(Student.courses)).all()
    logger.success(f"Fetched students successfully = {students_data}")
    return students_data
