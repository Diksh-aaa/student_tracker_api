from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from student_tracker_api.database.database import SessionLocal
from student_tracker_api.schemas.student import StudentCreate, StudentResponse
from student_tracker_api.services import student_service

router = APIRouter(prefix="/students", tags=["Students"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=StudentResponse)
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    return student_service.create_student(db, student)


@router.get("/", response_model=list[StudentResponse])
def list_students(db: Session = Depends(get_db)):
    return student_service.list_students(db)


@router.get("/{student_id}", response_model=StudentResponse)
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = student_service.get_student(db, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@router.delete("/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    success = student_service.remove_student(db, student_id)
    if not success:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"message": "Student deleted successfully"}


@router.get("/search/", response_model=list[StudentResponse])
def search_students(name: str, db: Session = Depends(get_db)):
    return student_service.search_students(db, name)


@router.get("/top-scorer/{subject}")
def top_scorer(subject: str, db: Session = Depends(get_db)):
    result = student_service.get_top_scorer(db, subject)
    if not result:
        raise HTTPException(
            status_code=404, detail="No scores found for subject")
    student, score = result
    return {"student_id": student.id, "name": student.name, "marks": score.marks}


@router.get("/department/{department}/average-score")
def department_average(department: str, db: Session = Depends(get_db)):
    avg = student_service.get_department_average(db, department)
    if avg is None:
        raise HTTPException(
            status_code=404, detail="No students found in department")
    return {"department": department, "average_score": avg}
