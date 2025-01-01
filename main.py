from fastapi import FastAPI
from routes.health import router as health_router
from routes.logs import router as log_router
from routes.process_pdf import router as pdf_router  # Assuming you named the combined PDF routes "pdf_routes.py"
import logging

# Initialize the FastAPI app
app = FastAPI(title="PDF Processing API",
              description="API for uploading, processing, and managing PDF files",
              version="1.0.0")

# Configure logging
logging.basicConfig(
    filename="server.log",
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# Include the routers
app.include_router(health_router, prefix="/health", tags=["Health"])
app.include_router(log_router, prefix="/logs", tags=["Logs"])
app.include_router(pdf_router, prefix="/pdf", tags=["PDF Operations"])

# Run the server (if running directly)
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
