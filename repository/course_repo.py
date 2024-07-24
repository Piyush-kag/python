from sqlalchemy import text
from sqlalchemy.orm import Session
from schemas import CourseCreate, CourseBase
from models import Course
from loguru import logger


def add_course(db: Session, course: CourseCreate) -> Course:
    db_course = Course(course_name=course.course_name)
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    logger.success("Course created successfully.")
    return db_course


def get_all_course(db):
    query = text("""
            SELECT
                c.id AS course_id,
                c.course_name,
                COUNT(s.id) AS student_count
            FROM
                courses c
            LEFT JOIN
                student_course sc ON c.id = sc.course_id
            LEFT JOIN
                students s ON sc.student_id = s.id
            GROUP BY
                c.id, c.course_name;
        """)

    result = db.execute(query).fetchall()
    logger.info(f"Fetched result = {result}")
    courses = [
        CourseBase(id=row.course_id, course_name=row.course_name, student_count=row.student_count)
        for row in result
    ]
    logger.success(f"Fetched course with student count successfully.")
    return courses
