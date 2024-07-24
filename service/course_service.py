from sqlalchemy.orm import Session

from models import Course

from repository import course_repo


def add_course(db: Session, course: Course):
    return course_repo.add_course(db, course)


def get_all_course(db):
    return course_repo.get_all_course(db)
