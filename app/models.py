class Student:
    """Student domain model"""
    
    def __init__(self, student_id: int, name: str, age: int, department: str):
        self.id = student_id
        self.name = name
        self.age = age
        self.department = department

    @classmethod
    def from_db_row(cls, row):
        """Create Student instance from database row"""
        return cls(row['id'], row['name'], row['age'], row['department'])

    def to_dict(self):
        """Convert Student instance to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'department': self.department
        }

    def __repr__(self):
        return f"Student(id={self.id}, name='{self.name}', age={self.age}, department='{self.department}')"

class Score:
    """Score domain model"""
    
    def __init__(self, student_id: int, subject: str, score: float, score_id: int = None):
        self.id = score_id
        self.student_id = student_id
        self.subject = subject
        self.score = score

    @classmethod
    def from_db_row(cls, row):
        """Create Score instance from database row"""
        return cls(row['student_id'], row['subject'], row['score'], row.get('id'))

    def to_dict(self):
        """Convert Score instance to dictionary"""
        return {
            'id': self.id,
            'student_id': self.student_id,
            'subject': self.subject,
            'score': self.score
        }

    def __repr__(self):
        return f"Score(id={self.id}, student_id={self.student_id}, subject='{self.subject}', score={self.score})"