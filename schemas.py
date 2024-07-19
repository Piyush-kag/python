from pydantic import BaseModel

class PostBase(BaseModel):
    title: str
    content: str
    user_id: int

class UserBase(BaseModel):
    id: int
    username: str
    email: str
