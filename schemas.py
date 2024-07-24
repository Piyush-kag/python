from typing import List
from pydantic import BaseModel


class PostBase(BaseModel):
    id: int
    title: str
    content: str
    user_id: int

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    id: int
    username: str
    email: str
    posts: List[PostBase] = []

    class Config:
        from_attributes = True


class UserName(BaseModel):
    id: int
    username: str
    email: str
    posts: List[PostBase] = []

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    username: str
    email: str

    class Config:
        from_attributes = True


class StudentCreate(BaseModel):
    student_name: str

    class Config:
        from_attributes = True


class CourseReference(BaseModel):
    id: int
    course_name: str

    class Config:
        from_attributes = True


class CourseBase(BaseModel):
    id: int
    course_name: str
    student_count: int

    class Config:
        from_attributes = True


class StudentBase(BaseModel):
    id: int
    student_name: str
    courses: List[CourseReference] = []

    class Config:
        from_attributes = True


class CourseCreate(BaseModel):
    course_name: str

    class Config:
        from_attributes = True
