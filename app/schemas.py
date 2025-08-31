from typing import List, Optional
from pydantic import BaseModel, Field, constr, confloat


# Student Schemas
class StudentBase(BaseModel):
    name: constr(strip_whitespace=True, min_length=1, max_length=100)
    department: constr(strip_whitespace=True, min_length=1, max_length=100)


class StudentCreate(StudentBase):
    pass


class StudentOut(StudentBase):
    id: int

    class Config:
        from_attributes = True


# Score Schemas
class ScoreBase(BaseModel):
    subject: constr(strip_whitespace=True, min_length=1, max_length=100)
    score: confloat(ge=0, le=100)


class ScoreCreate(ScoreBase):
    pass


class ScoreOut(ScoreBase):
    id: int
    student_id: int

    class Config:
        from_attributes = True


class AverageOut(BaseModel):
    average: float = Field(..., description="Average score")


class DepartmentAverageOut(BaseModel):
    department: str
    average: float
    student_count: int
    score_count: int
