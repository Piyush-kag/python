from typing import List
from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Mapped, mapped_column

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    # Relationship to the Post class
    posts: Mapped[List["Post"]] = relationship()


class Post(Base):
    __tablename__ = 'posts'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(50))
    content: Mapped[str] = mapped_column(String(100))
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))
    # user: Mapped["User"] = relationship("User", back_populates="posts")


# Association table
student_course_association = Table(
    'student_course', Base.metadata,
    Column('student_id', Integer, ForeignKey('students.id')),
    Column('course_id', Integer, ForeignKey('courses.id'))
)


class Student(Base):
    __tablename__ = 'students'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    student_name: Mapped[str] = mapped_column(String(50), index=True)
    courses: Mapped[List["Course"]] = relationship(
        "Course",
        secondary="student_course",  # Ensure this matches the actual association table name
        back_populates="students"
    )

    def __repr__(self):
        return f"Student(id={self.id}, name={self.student_name})"


class Course(Base):
    __tablename__ = 'courses'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    course_name: Mapped[str] = mapped_column(String(100), index=True)
    students: Mapped[List["Student"]] = relationship(
        "Student",
        secondary=student_course_association,
        back_populates="courses"
    )
