from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, root_validator, validator


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
        return [x if isinstance(x, str) else x.name for x in v]

    class Config:
        orm_mode = True


class ListeningHistory(BaseModel):
    song_id: int
    user_id: int
    duration: Optional[int]
    song: Song
    timestamp: Optional[datetime]
    
    @classmethod
    def from_orm(cls, orm):
        instance = super().from_orm(orm)
        if orm.end_time:
            instance.duration = (orm.end_time - orm.start_time).total_seconds()
        else:
            instance.duration = min((datetime.utcnow() - orm.start_time).total_seconds(), orm.song.duration)
        instance.timestamp = orm.start_time
        return instance

    class Config:
        orm_mode = True
