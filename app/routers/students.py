from fastapi import APIRouter, HTTPException, Query
from typing import List
from app.database import get_db_connection
from app.schemas import (
    StudentCreate, StudentResponse, StudentWithScores, 
    ScoreResponse, SuccessResponse
)
from app.models import Student

router = APIRouter(prefix="/students", tags=["students"])

@router.post("/", 
            response_model=StudentResponse,
            summary="Add a new student",
            description="Create a new student with name, age, and department")
async def add_student(student: StudentCreate):
    """Add a new student to the database"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO students (name, age, department) VALUES (?, ?, ?)",
            (student.name, student.age, student.department)
        )
        conn.commit()
        student_id = cursor.lastrowid
        
        cursor.execute("SELECT * FROM students WHERE id = ?", (student_id,))
        row = cursor.fetchone()
        return StudentResponse(**dict(row))

@router.get("/", 
           response_model=List[StudentResponse],
           summary="List all students",
           description="Retrieve a list of all students in the database")
async def list_students():
    """Get all students ordered by ID"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students ORDER BY id")
        rows = cursor.fetchall()
        return [StudentResponse(**dict(row)) for row in rows]

@router.get("/{student_id}", 
           response_model=StudentWithScores,
           summary="Get student by ID",
           description="Get detailed information about a student including their scores")
async def get_student(student_id: int):
    """Get student details by ID with all their scores"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # Get student
        cursor.execute("SELECT * FROM students WHERE id = ?", (student_id,))
        student_row = cursor.fetchone()
        if not student_row:
            raise HTTPException(status_code=404, detail="Student not found")
        
        # Get scores
        cursor.execute("SELECT subject, score FROM scores WHERE student_id = ?", (student_id,))
        score_rows = cursor.fetchall()
        
        student_data = dict(student_row)
        student_data['scores'] = [ScoreResponse(**dict(row)) for row in score_rows]
        
        return StudentWithScores(**student_data)

@router.delete("/{student_id}", 
              response_model=SuccessResponse,
              summary="Delete student",
              description="Remove a student and all their scores from the database")
async def delete_student(student_id: int):
    """Remove student by ID along with all associated scores"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # Check if student exists
        cursor.execute("SELECT * FROM students WHERE id = ?", (student_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Student not found")
        
        # Delete scores first (foreign key constraint)
        cursor.execute("DELETE FROM scores WHERE student_id = ?", (student_id,))
        
        # Delete student
        cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
        conn.commit()
        
        return SuccessResponse(message=f"Student {student_id} deleted successfully")

@router.get("/search/", 
           response_model=List[StudentResponse],
           summary="Search students by name",
           description="Search for students by partial name match (case-insensitive)")
async def search_students(name: str = Query(..., min_length=1, description="Name to search for")):
    """Search students by name using partial matching"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM students WHERE name LIKE ? ORDER BY id",
            (f"%{name}%",)
        )
        rows = cursor.fetchall()
        return [StudentResponse(**dict(row)) for row in rows]