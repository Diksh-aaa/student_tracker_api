from sqlalchemy.orm import Session
from student_tracker_api.repositories import student_repository
from student_tracker_api.schemas.student import StudentCreate


def create_student(db: Session, student: StudentCreate):
    return student_repository.insert_student(db, student)


def list_students(db: Session):
    return student_repository.get_all_students(db)


def get_student(db: Session, student_id: int):
    return student_repository.get_student_by_id(db, student_id)


def search_students(db: Session, name: str):
    return student_repository.get_student_by_name(db, name)


def remove_student(db: Session, student_id: int):
    return student_repository.delete_student(db, student_id)


def get_department_average(db: Session, department: str):
    return student_repository.get_department_average(db, department)


def get_top_scorer(db: Session, subject: str):
    return student_repository.get_top_scorer(db, subject)
