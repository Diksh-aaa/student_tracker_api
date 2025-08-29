from pydantic import BaseModel
from typing import List
from student_tracker_api.schemas.score import ScoreResponse


class StudentBase(BaseModel):
    name: str
    department: str


class StudentCreate(StudentBase):
    pass


class StudentResponse(StudentBase):
    id: int
    scores: List[ScoreResponse] = []

    class Config:
        orm_mode = True
