from typing import List
from pydantic import BaseModel


class UserBase(BaseModel):
    username:str
    name:str

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    password:str


class UserEmbedded(UserBase):
    id: int

    class Config:
        orm_mode = True

class User(UserBase):
    id: int
    following: List[UserEmbedded]
    followers: List[UserEmbedded]

    class Config:
        orm_mode = True