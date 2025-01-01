import os
import shutil
import logging
from fastapi import APIRouter, File, UploadFile, HTTPException, Query, Body
from fastapi.responses import FileResponse, JSONResponse
from pdf_manager.manager import PDFManager
from pdf_manager.check_metadata import check_pdf_metadata

UPLOAD_DIR = "./uploaded_files"
PROCESSED_DIR = "./processed_files"
router = APIRouter()

# Ensure the upload and processed directories exist
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)

@router.get("/pdf-list")
def list_uploaded_files():
    """
    Endpoint to list all uploaded PDF files as a list and string.
    """
    try:
        files = os.listdir(UPLOAD_DIR)
        pdf_files = [file for file in files if file.endswith(".pdf")]
        pdf_files_string = ", ".join(pdf_files)
        return {
            "uploaded_files": pdf_files,
            "uploaded_files_string": pdf_files_string
        }
    except Exception as e:
        logging.error(f"Error listing uploaded files: {e}")
        raise HTTPException(status_code=500, detail="Error listing uploaded files.")

@router.get("/processed-pdf-list")
def list_processed_files():
    """
    Endpoint to list all processed PDF files.
    """
    try:
        files = os.listdir(PROCESSED_DIR)
        pdf_files = [file for file in files if file.endswith(".pdf")]
        return {"processed_files": pdf_files}
    except Exception as e:
        logging.error(f"Error listing processed files: {e}")
        raise HTTPException(status_code=500, detail="Error listing processed files.")

@router.post("/pdf-upload-and-process")
def upload_and_process_file(file: UploadFile = File(...), n_pages: int = 5):
    """
    Endpoint to upload and immediately process a PDF file.
    """
    try:
        # Save the uploaded file
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        logging.info(f"File uploaded: {file_path}")

        # Process the uploaded file
        pdf_manager = PDFManager(file_path, n_pages=n_pages)
        metadata_file, cover_file, renamed_pdf_path = pdf_manager.process_pdf()

        # Move processed files to the processed directory
        shutil.move(renamed_pdf_path, os.path.join(PROCESSED_DIR, os.path.basename(renamed_pdf_path)))
        if metadata_file:
            shutil.move(metadata_file, os.path.join(PROCESSED_DIR, os.path.basename(metadata_file)))
        if cover_file:
            shutil.move(cover_file, os.path.join(PROCESSED_DIR, os.path.basename(cover_file)))

        return {
            "message": "PDF uploaded and processed successfully.",
            "metadata_file": os.path.join(PROCESSED_DIR, os.path.basename(metadata_file)) if metadata_file else None,
            "cover_file": os.path.join(PROCESSED_DIR, os.path.basename(cover_file)) if cover_file else None,
            "renamed_pdf": os.path.join(PROCESSED_DIR, os.path.basename(renamed_pdf_path))
        }

    except Exception as e:
        logging.error(f"Error uploading and processing PDF: {e}")
        raise HTTPException(status_code=500, detail=f"Error uploading and processing PDF: {e}")

@router.post("/pdf-check")
def check_metadata(file_info: dict = Body(..., example={"file_name": "example file.pdf"})):
    """
    Endpoint to check and return metadata of a processed PDF file.
    Accepts JSON input for file name to handle spaces in key-value pairs.
    """
    try:
        # Extract file name from JSON body
        file_name = file_info.get("file_name")
        if not file_name:
            raise HTTPException(status_code=400, detail="File name is required in the JSON body.")

        file_path = os.path.join(PROCESSED_DIR, file_name)
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="File not found. Please process the file first.")

        logging.info(f"Checking metadata for PDF: {file_path}")

        # Call the check_pdf_metadata function
        metadata = check_pdf_metadata(file_path)

        return JSONResponse({
            "message": "Metadata checked successfully.",
            "metadata": metadata
        })

    except ValueError as e:
        logging.error(f"Error when checking PDF metadata: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logging.error(f"Unexpected error when checking PDF metadata: {e}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred while checking PDF metadata.")
@router.get("/pdf-download")
def download_pdf(file_name: str = Query(..., description="Name of the processed PDF file")):
    """
    Endpoint to download the processed PDF file.
    """
    try:
        file_path = os.path.join(PROCESSED_DIR, file_name)
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="File not found. Please process the file first.")

        logging.info(f"Serving PDF file for download: {file_path}")
        return FileResponse(
            file_path,
            media_type="application/pdf",
            filename=os.path.basename(file_path),
        )

    except Exception as e:
        logging.error(f"Error serving PDF file for download: {e}")
        raise HTTPException(status_code=500, detail=f"Error serving PDF file: {e}")
@router.delete("/pdf-delete")
def delete_pdf(file_name: str = Query(..., description="Name of the PDF file to delete")):
    """
    Endpoint to delete a specified PDF file from the processed directory.
    """
    try:
        file_path = os.path.join(PROCESSED_DIR, file_name)
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="File not found.")

        os.remove(file_path)
        logging.info(f"Deleted PDF file: {file_path}")

        return JSONResponse({"message": f"File '{file_name}' deleted successfully."})

    except Exception as e:
        logging.error(f"Error deleting PDF file: {e}")
        raise HTTPException(status_code=500, detail=f"Error deleting PDF file: {e}")