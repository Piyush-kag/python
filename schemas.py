from typing import List, Optional
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
    password: str
    posts: List[PostBase] = []

    class Config:
        from_attributes = True


class UserName(BaseModel):
    id: int
    username: str
    email: str
    password: str
    posts: List[PostBase] = []

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    username: str
    email: str
    password: str

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str

    class Config:
        from_attributes = True


class TokenData(BaseModel):
    username: str or None = None
    id: int or None = None

    class Config:
        from_attributes = True


class UserInDB(BaseModel):
    hashed_password: str

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


class EmployeeDetailsBase(BaseModel):
    address: Optional[str] = None
    phone_number: Optional[str] = None


class EmployeeDetailsCreate(EmployeeDetailsBase):
    employee_id: int


class EmployeeDetails(EmployeeDetailsBase):
    id: int
    employee_id: int

    class Config:
        from_attributes = True


class EmployeeBase(BaseModel):
    name: str


class EmployeeCreate(EmployeeBase):
    pass


class Employee(EmployeeBase):
    id: int
    details: Optional[EmployeeDetails] = None

    class Config:
        from_attributes = True
