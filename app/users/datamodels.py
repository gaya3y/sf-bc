from typing import List
from pydantic import BaseModel


class UserBase(BaseModel):
    username:str
    name:str

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    password:str


class User(UserCreate):
    id: int
    following: List[UserBase]
    followers: List[UserBase]

    class Config:
        orm_mode = True