from fastapi import APIRouter, HTTPException
from app.database import get_db_connection
from app.schemas import (
    ScoreCreate, StudentAverageResponse, TopScorerResponse, 
    DepartmentAverageResponse, SuccessResponse
)

router = APIRouter(tags=["scores"])

@router.post("/students/{student_id}/scores/",
            summary="Add or update student score",
            description="Add a new score or update existing score for a student in a specific subject")
async def add_or_update_score(student_id: int, score_data: ScoreCreate):
    """Add or update a score for a student in a specific subject"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # Check if student exists
        cursor.execute("SELECT * FROM students WHERE id = ?", (student_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Student not found")
        
        # Insert or update score
        cursor.execute(
            "INSERT OR REPLACE INTO scores (student_id, subject, score) VALUES (?, ?, ?)",
            (student_id, score_data.subject, score_data.score)
        )
        conn.commit()
        
        return {
            "message": f"Score for {score_data.subject} updated successfully",
            "student_id": student_id,
            "subject": score_data.subject,
            "score": score_data.score
        }

@router.get("/students/{student_id}/average-score/", 
           response_model=StudentAverageResponse,
           summary="Get student's average score",
           description="Calculate and return the average score for a specific student")
async def get_student_average(student_id: int):
    """Get average score for a student across all subjects"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # Check if student exists
        cursor.execute("SELECT name FROM students WHERE id = ?", (student_id,))
        student = cursor.fetchone()
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")
        
        # Calculate average
        cursor.execute(
            "SELECT AVG(score) as average FROM scores WHERE student_id = ?",
            (student_id,)
        )
        result = cursor.fetchone()
        average = result['average']
        
        if average is None:
            return StudentAverageResponse(
                student_id=student_id,
                student_name=student['name'],
                average_score=0,
                message="No scores found for this student"
            )
        
        return StudentAverageResponse(
            student_id=student_id,
            student_name=student['name'],
            average_score=round(average, 2)
        )

@router.get("/students/top-scorer/{subject}", 
           response_model=TopScorerResponse,
           summary="Get top scorer in subject",
           description="Find the student with the highest score in a specific subject")
async def get_top_scorer(subject: str):
    """Get the top scorer in a given subject"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT s.id, s.name, s.department, sc.score 
            FROM students s 
            JOIN scores sc ON s.id = sc.student_id 
            WHERE sc.subject = ? 
            ORDER BY sc.score DESC 
            LIMIT 1
        ''', (subject,))
        
        result = cursor.fetchone()
        if not result:
            raise HTTPException(
                status_code=404, 
                detail=f"No scores found for subject: {subject}"
            )
        
        return TopScorerResponse(
            subject=subject,
            top_scorer={
                "id": result['id'],
                "name": result['name'],
                "department": result['department'],
                "score": result['score']
            }
        )

@router.get("/departments/{department}/average-score/", 
           response_model=DepartmentAverageResponse,
           summary="Get department average score",
           description="Calculate average score for all students in a department")
async def get_department_average(department: str):
    """Get average score for all students in a department"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT AVG(sc.score) as average, COUNT(DISTINCT s.id) as student_count
            FROM students s 
            JOIN scores sc ON s.id = sc.student_id 
            WHERE s.department = ?
        ''', (department,))
        
        result = cursor.fetchone()
        average = result['average']
        student_count = result['student_count']
        
        if average is None or student_count == 0:
            raise HTTPException(
                status_code=404, 
                detail=f"No students with scores found in department: {department}"
            )
        
        return DepartmentAverageResponse(
            department=department,
            average_score=round(average, 2),
            student_count=student_count
        )