from fastapi import FastAPI
from student_tracker_api.database.database_manager import Base, engine
from student_tracker_api.controllers import student_controller, score_controller
from student_tracker_api.exceptions import app_exceptions, error_handlers

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Student Performance Tracker API")

# Register routers
app.include_router(student_controller.router)
app.include_router(score_controller.router)

# Register exception handlers
app.add_exception_handler(
    app_exceptions.StudentNotFoundException, error_handlers.student_not_found_handler)
app.add_exception_handler(
    app_exceptions.ScoreNotFoundException, error_handlers.score_not_found_handler)
