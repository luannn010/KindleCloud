# routes/log_routes.py
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
import os

LOG_FILE = "./server.log"

router = APIRouter()

@router.get("/")
def get_log():
    """
    Endpoint to retrieve the server log.
    """
    if not os.path.exists(LOG_FILE):
        raise HTTPException(status_code=404, detail="Log file not found.")
    return FileResponse(LOG_FILE, media_type="text/plain")
