from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Score, Student
from ..schemas import AverageOut, DepartmentAverageOut, ScoreCreate, ScoreOut


router = APIRouter(prefix="/students", tags=["Scores"])


def _get_student_or_404(student_id: int, db: Session) -> Student:
    student = db.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    return student


@router.post("/{student_id}/scores/", response_model=ScoreOut, status_code=status.HTTP_201_CREATED, summary="Add/update subject score for a student")
def upsert_score(
    student_id: int = Path(..., ge=1),
    payload: ScoreCreate = ...,
    db: Session = Depends(get_db),
):
    _get_student_or_404(student_id, db)

    # Try to find existing score for subject
    stmt = select(Score).where(Score.student_id == student_id, func.lower(Score.subject) == payload.subject.lower())
    existing = db.execute(stmt).scalars().first()
    if existing:
        existing.score = float(payload.score)
        db.add(existing)
        db.commit()
        db.refresh(existing)
        return existing

    new_score = Score(student_id=student_id, subject=payload.subject.strip(), score=float(payload.score))
    db.add(new_score)
    db.commit()
    db.refresh(new_score)
    return new_score


@router.get("/{student_id}/average-score/", response_model=AverageOut, summary="Get average score for a student")
def student_average(student_id: int, db: Session = Depends(get_db)):
    _get_student_or_404(student_id, db)
    stmt = select(func.avg(Score.score)).where(Score.student_id == student_id)
    avg_val = db.execute(stmt).scalar()
    if avg_val is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No scores found for student")
    return {"average": round(float(avg_val), 2)}


@router.get("/top-scorer/{subject}", response_model=ScoreOut, summary="Get top scorer in a subject")
def top_scorer(subject: str, db: Session = Depends(get_db)):
    stmt = (
        select(Score)
        .where(func.lower(Score.subject) == subject.lower())
        .order_by(Score.score.desc())
        .limit(1)
    )
    top = db.execute(stmt).scalars().first()
    if not top:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No scores for subject")
    return top


@router.get("/departments/{department}/average-score/", response_model=DepartmentAverageOut, summary="Get average score for a department")
def department_average(department: str, db: Session = Depends(get_db)):
    # Average over all scores for students in the department
    avg_stmt = (
        select(func.avg(Score.score))
        .join(Student, Student.id == Score.student_id)
        .where(func.lower(Student.department) == department.lower())
    )
    avg_val = db.execute(avg_stmt).scalar()

    if avg_val is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No scores for department")

    # Count students and scores in department (for context)
    student_count = db.execute(
        select(func.count(func.distinct(Student.id))).where(func.lower(Student.department) == department.lower())
    ).scalar() or 0

    score_count = db.execute(
        select(func.count(Score.id)).join(Student, Student.id == Score.student_id).where(
            func.lower(Student.department) == department.lower()
        )
    ).scalar() or 0

    return {
        "department": department,
        "average": round(float(avg_val), 2),
        "student_count": int(student_count),
        "score_count": int(score_count),
    }

