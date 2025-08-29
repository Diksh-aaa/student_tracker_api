from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from student_tracker_api.database.database import Base


class Score(Base):
    __tablename__ = "scores"

    id = Column(Integer, primary_key=True, index=True)
    subject = Column(String, nullable=False)
    marks = Column(Float, nullable=False)
    student_id = Column(Integer, ForeignKey("students.id"))

    student = relationship("Student", back_populates="scores")
