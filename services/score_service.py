from sqlalchemy.orm import Session
from student_tracker_api.repositories import score_repository
from student_tracker_api.schemas.score import ScoreCreate


def add_or_update_score(db: Session, student_id: int, score: ScoreCreate):
    return score_repository.add_or_update_score(db, student_id, score)


def get_student_scores(db: Session, student_id: int):
    return score_repository.get_scores_by_student(db, student_id)


def get_average_score(db: Session, student_id: int):
    return score_repository.get_average_score(db, student_id)
