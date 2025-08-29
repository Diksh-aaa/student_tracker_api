from sqlalchemy.orm import Session
from student_tracker_api.models.score import Score
from student_tracker_api.schemas.score import ScoreCreate


def add_or_update_score(db: Session, student_id: int, score: ScoreCreate):
    db_score = db.query(Score).filter(
        Score.student_id == student_id,
        Score.subject == score.subject
    ).first()
    if db_score:
        db_score.marks = score.marks
    else:
        db_score = Score(student_id=student_id,
                         subject=score.subject, marks=score.marks)
        db.add(db_score)
    db.commit()
    db.refresh(db_score)
    return db_score


def get_scores_by_student(db: Session, student_id: int):
    return db.query(Score).filter(Score.student_id == student_id).all()


def get_average_score(db: Session, student_id: int):
    scores = get_scores_by_student(db, student_id)
    if not scores:
        return 0
    return sum(s.marks for s in scores) / len(scores)
