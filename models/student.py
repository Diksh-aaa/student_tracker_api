from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from student_tracker_api.database.database import Base


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    department = Column(String, nullable=False)

    scores = relationship("Score", back_populates="student",
                          cascade="all, delete-orphan")
