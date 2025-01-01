# routes/health_routes.py
from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get("/")
def health_check():
    """
    Endpoint to check the health of the server.
    """
    return JSONResponse(content={"status": "healthy"}, status_code=200)
