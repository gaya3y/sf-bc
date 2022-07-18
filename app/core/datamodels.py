from typing import List
from pydantic import BaseModel, validator


class SongCreate(BaseModel):
    name: str
    artists: List[str]
    genres: List[str]
    duration: int
    url: str


class Song(SongCreate):
    id: int
    artists: List[str]
    genres: List[str]

    @validator("artists", "genres", pre=True)
    def convert_to_string(cls, v):
        return [x.name for x in v]

    class Config:
        orm_mode = True
    