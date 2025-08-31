from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Student
from ..schemas import StudentCreate, StudentOut


router = APIRouter(prefix="/students", tags=["Students"])


@router.post("/", response_model=StudentOut, status_code=status.HTTP_201_CREATED, summary="Add a new student")
def create_student(payload: StudentCreate, db: Session = Depends(get_db)):
    student = Student(name=payload.name.strip(), department=payload.department.strip())
    db.add(student)
    db.commit()
    db.refresh(student)
    return student


@router.get("/", response_model=List[StudentOut], summary="List all students")
def list_students(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Max records to return"),
    db: Session = Depends(get_db),
):
    stmt = select(Student).offset(skip).limit(limit)
    results = db.execute(stmt).scalars().all()
    return results


@router.get("/{student_id}", response_model=StudentOut, summary="Get student by ID")
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = db.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    return student


@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Remove student by ID")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student = db.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    db.delete(student)
    db.commit()
    return None


@router.get("/search/", response_model=List[StudentOut], summary="Search students by name")
def search_students(name: str = Query(..., min_length=1), db: Session = Depends(get_db)):
    name = name.strip()
    stmt = select(Student).where(func.lower(Student.name).like(f"%{name.lower()}%"))
    results = db.execute(stmt).scalars().all()
    return results
