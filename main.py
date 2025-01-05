from fastapi import FastAPI, Depends, HTTPException, Header
from dotenv import load_dotenv
import os
import logging
from routes.health import router as health_router
from routes.logs import router as log_router
from routes.process_pdf import router as pdf_router  # Assuming you have a "process_pdf" module

# Load environment variables from .env
load_dotenv()

# Retrieve the API key from the .env file
GCP_API_KEY = os.getenv("GCP_API_KEY")
if not GCP_API_KEY:
    raise ValueError("GCP_API_KEY must be set.")

# Initialize the FastAPI app
app = FastAPI(
    title="PDF Processing API",
    description="API for uploading, processing, and managing PDF files",
    version="1.0.0"
)

# Configure logging
logging.basicConfig(
    filename="server.log",
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Dependency to validate API Key
async def validate_api_key(api_key: str = Header(...)):
    """
    Validate the API key passed in the headers.
    """
    if api_key != GCP_API_KEY:
        logger.warning("Unauthorized access attempt with invalid API key.")
        raise HTTPException(status_code=401, detail="Unauthorized: Invalid API Key")

# Include the routers with the API key dependency
app.include_router(health_router, prefix="/health", tags=["Health"], dependencies=[Depends(validate_api_key)])
app.include_router(log_router, prefix="/logs", tags=["Logs"], dependencies=[Depends(validate_api_key)])
app.include_router(pdf_router, prefix="/pdf", tags=["PDF Operations"], dependencies=[Depends(validate_api_key)])

# Root endpoint (optional, for basic status checks)
@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint to verify the server is running.
    """
    logger.info("Root endpoint accessed.")
    return {"message": "PDF Processing API is up and running!"}

# Run the server (if running directly)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
