from sqlalchemy.orm import Session
from student_tracker_api.models.student import Student
from student_tracker_api.models.score import Score
from student_tracker_api.schemas.student import StudentCreate


def insert_student(db: Session, student: StudentCreate):
    db_student = Student(name=student.name, department=student.department)
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student


def get_all_students(db: Session):
    return db.query(Student).all()


def get_student_by_id(db: Session, student_id: int):
    return db.query(Student).filter(Student.id == student_id).first()


def get_student_by_name(db: Session, name: str):
    return db.query(Student).filter(Student.name.ilike(f"%{name}%")).all()


def delete_student(db: Session, student_id: int):
    student = get_student_by_id(db, student_id)
    if student:
        db.delete(student)
        db.commit()
        return True
    return False


def get_department_average(db: Session, department: str):
    students = db.query(Student).filter(Student.department == department).all()
    if not students:
        return None
    total, count = 0, 0
    for student in students:
        for score in student.scores:
            total += score.marks
            count += 1
    return total / count if count > 0 else 0


def get_top_scorer(db: Session, subject: str):
    return (
        db.query(Student, Score)
        .join(Score)
        .filter(Score.subject == subject)
        .order_by(Score.marks.desc())
        .first()
    )
