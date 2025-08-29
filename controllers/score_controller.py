from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from student_tracker_api.database.database import SessionLocal
from student_tracker_api.schemas.score import ScoreCreate, ScoreResponse
from student_tracker_api.services import score_service, student_service
from student_tracker_api.exceptions.app_exceptions import StudentNotFoundException

router = APIRouter(prefix="/students/{student_id}/scores", tags=["Scores"])

# Dependency to get DB session


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=ScoreResponse)
def add_score(student_id: int, score: ScoreCreate, db: Session = Depends(get_db)):
    """
    Add or update a score for a student.
    """
    student = student_service.get_student(db, student_id)
    if not student:
        raise StudentNotFoundException(student_id)
    return score_service.add_or_update_score(db, student_id, score)


@router.get("/", response_model=list[ScoreResponse])
def get_scores(student_id: int, db: Session = Depends(get_db)):
    """
    Get all scores for a student.
    """
    student = student_service.get_student(db, student_id)
    if not student:
        raise StudentNotFoundException(student_id)
    return score_service.get_student_scores(db, student_id)


@router.get("/average-score", summary="Get average score of a student")
def average_score(student_id: int, db: Session = Depends(get_db)):
    """
    Calculate and return the average score for a student.
    """
    student = student_service.get_student(db, student_id)
    if not student:
        raise StudentNotFoundException(student_id)
    avg = score_service.get_average_score(db, student_id)
    return {"student_id": student_id, "average_score": avg}
