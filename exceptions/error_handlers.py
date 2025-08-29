from fastapi import Request
from fastapi.responses import JSONResponse
from student_tracker_api.exceptions.app_exceptions import StudentNotFoundException, ScoreNotFoundException


async def student_not_found_handler(request: Request, exc: StudentNotFoundException):
    return JSONResponse(
        status_code=404,
        content={"error": str(exc)},
    )


async def score_not_found_handler(request: Request, exc: ScoreNotFoundException):
    return JSONResponse(
        status_code=404,
        content={"error": str(exc)},
    )
