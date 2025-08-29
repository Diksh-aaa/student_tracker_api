from pydantic import BaseModel


class ScoreBase(BaseModel):
    subject: str
    marks: float


class ScoreCreate(ScoreBase):
    pass


class ScoreResponse(ScoreBase):
    id: int

    class Config:
        orm_mode = True
