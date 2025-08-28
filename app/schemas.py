from pydantic import BaseModel, Field
from typing import List, Optional

# Student Schemas
class StudentCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Student's full name")
    age: int = Field(..., ge=1, le=150, description="Student's age")
    department: str = Field(..., min_length=1, max_length=100, description="Student's department")

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "John Doe",
                "age": 20,
                "department": "Computer Science"
            }
        }
    }

class StudentResponse(BaseModel):
    id: int
    name: str
    age: int
    department: str

class StudentUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    age: Optional[int] = Field(None, ge=1, le=150)
    department: Optional[str] = Field(None, min_length=1, max_length=100)

# Score Schemas
class ScoreCreate(BaseModel):
    subject: str = Field(..., min_length=1, max_length=100, description="Subject name")
    score: float = Field(..., ge=0, le=100, description="Score value (0-100)")

    model_config = {
        "json_schema_extra": {
            "example": {
                "subject": "Mathematics",
                "score": 85.5
            }
        }
    }

class ScoreResponse(BaseModel):
    subject: str
    score: float

class ScoreUpdate(BaseModel):
    score: float = Field(..., ge=0, le=100)

# Combined Schemas
class StudentWithScores(BaseModel):
    id: int
    name: str
    age: int
    department: str
    scores: List[ScoreResponse] = []

class TopScorerResponse(BaseModel):
    subject: str
    top_scorer: dict

class DepartmentAverageResponse(BaseModel):
    department: str
    average_score: float
    student_count: int

class StudentAverageResponse(BaseModel):
    student_id: int
    student_name: str
    average_score: float
    message: Optional[str] = None

# Error Response Schema
class ErrorResponse(BaseModel):
    detail: str
    
class SuccessResponse(BaseModel):
    message: str