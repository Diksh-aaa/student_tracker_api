from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import init_database
from app.routers import students, scores
import uvicorn

# Create FastAPI app with metadata
app = FastAPI(
    title="Student Performance Tracker",
    description="A comprehensive REST API for tracking student performance and scores across different subjects and departments",
    version="1.0.0",
    contact={
        "name": "Student Tracker API",
        "email": "admin@studenttracker.com",
    },
    license_info={
        "name": "MIT",
    },
)

# Add CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(students.router)
app.include_router(scores.router)

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    """Initialize database and perform startup tasks"""
    init_database()
    print("✅ Database initialized successfully")
    print("🚀 Student Performance Tracker API is starting up...")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup tasks on shutdown"""
    print("🛑 Student Performance Tracker API is shutting down...")

# Root endpoint
@app.get("/", 
         summary="API Health Check",
         description="Check if the API is running and get basic information")
async def root():
    """Health check endpoint with API information"""
    return {
        "message": "Student Performance Tracker API is running!",
        "version": "1.0.0",
        "status": "healthy",
        "endpoints": {
            "documentation": "/docs",
            "openapi_schema": "/openapi.json",
            "students": "/students/",
            "scores": "Various score endpoints"
        }
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    """Detailed health check for monitoring"""
    return {
        "status": "healthy",
        "service": "Student Performance Tracker API",
        "version": "1.0.0"
    }

# Run the application
if __name__ == "__main__":
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=True,
        log_level="info"
    )