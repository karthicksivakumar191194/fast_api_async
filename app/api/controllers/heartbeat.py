from fastapi import APIRouter, status
from fastapi.responses import JSONResponse


router = APIRouter()


@router.get("/application")
async def check_application_heartbeat():
    """
    Heartbeat endpoint to check if the application is alive and healthy.
    """
    return JSONResponse(content={"message": "Running"}, status_code=status.HTTP_200_OK)


@router.get("/database")
async def check_database_heartbeat():
    """
    Heartbeat endpoint to check if the database is alive and healthy.
    """
    return JSONResponse(content={"message": "Running"}, status_code=status.HTTP_200_OK)
