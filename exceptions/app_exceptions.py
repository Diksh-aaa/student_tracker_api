class StudentNotFoundException(Exception):
    def __init__(self, student_id: int):
        self.student_id = student_id
        super().__init__(f"Student with ID {student_id} not found")


class ScoreNotFoundException(Exception):
    def __init__(self, student_id: int, subject: str = None):
        self.student_id = student_id
        self.subject = subject
        message = f"No scores found for student ID {student_id}"
        if subject:
            message += f" in subject '{subject}'"
        super().__init__(message)
