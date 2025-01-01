# EBook Metadata Automation Server

## Project Overview
This project is a Python-based server that automates the process of retrieving metadata for eBooks in PDF format using the OpenAI API. The server also facilitates sending the processed eBooks to a Kindle device via email using the Google Scripts App for email automation.

---

## Features
- **Metadata Retrieval**: Automatically fetches detailed metadata for eBooks in PDF format using OpenAI API.
- **Kindle Integration**: Sends processed eBooks to Kindle devices using email.
- **Google Scripts Integration**: Utilizes Google Scripts App for automated email services.
- **User-Friendly API**: Exposes endpoints for processing PDFs and sending them to Kindle.

---

## Technologies Used
- **Python**: Backend server implementation.
- **OpenAI API**: For metadata extraction.
- **Google Scripts App**: For automated email services.
- **FastAPI**: For creating RESTful API endpoints.
- **Docker**: For containerization.
- **Postman** (optional): For testing API endpoints.

---

## Prerequisites
1. Python 3.11 or higher installed on your system.
2. OpenAI API key for metadata extraction.
3. Access to a Gmail account for Google Scripts integration.
4. Docker (optional, for containerized deployment).

---

## Installation and Setup

### Step 1: Clone the Repository
```bash
git clone https://github.com/your-username/ebook-metadata-server.git
cd ebook-metadata-server
```

### Step 2: Set Up Environment Variables
Create a `.env` file in the project root with the following contents:
```env
OPENAI_API_KEY=your_openai_api_key
GMAIL_USER=your_gmail_account
KINDLE_EMAIL=your_kindle_email_address
```

### Step 3: Install Dependencies
Create a virtual environment and install required packages:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Step 4: Run the Server
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

---

## API Endpoints

### 1. **List Uploaded PDFs**
   - **URL**: `/pdf/pdf-list`
   - **Method**: `GET`
   - **Description**: Lists all uploaded PDF files.
   - **Response**:
     ```json
     {
         "uploaded_files": ["example1.pdf", "example2.pdf"],
         "uploaded_files_string": "example1.pdf, example2.pdf"
     }
     ```

### 2. **List Processed PDFs**
   - **URL**: `/pdf/processed-pdf-list`
   - **Method**: `GET`
   - **Description**: Lists all processed PDF files.
   - **Response**:
     ```json
     {
         "processed_files": ["processed1.pdf", "processed2.pdf"]
     }
     ```

### 3. **Upload and Process PDF**
   - **URL**: `/pdf/pdf-upload-and-process`
   - **Method**: `POST`
   - **Description**: Uploads and processes a PDF file to extract metadata.
   - **Request Parameters**:
     - **file**: The PDF file to upload (multipart).
     - **n_pages**: Number of pages to process (default is 5).
   - **Response**:
     ```json
     {
         "message": "PDF uploaded and processed successfully.",
         "metadata_file": "processed_files/metadata_example.json",
         "cover_file": "processed_files/cover_example.png",
         "renamed_pdf": "processed_files/example_processed.pdf"
     }
     ```

### 4. **Check Metadata of a Processed PDF**
   - **URL**: `/pdf/pdf-check`
   - **Method**: `GET`
   - **Description**: Retrieves metadata of a processed PDF file.
   - **Query Parameters**:
     - **file_name**: Name of the processed PDF file.
   - **Response**:
     ```json
     {
         "message": "Metadata checked successfully.",
         "metadata": {
             "title": "Example Title",
             "author": "Example Author",
             "publisher": "Example Publisher"
         }
     }
     ```

### 5. **Download Processed PDF**
   - **URL**: `/pdf/pdf-download`
   - **Method**: `GET`
   - **Description**: Downloads a processed PDF file.
   - **Query Parameters**:
     - **file_name**: Name of the processed PDF file.
   - **Response**: Returns the PDF file as a downloadable attachment.

---

## Google Scripts Email Setup
1. Open [Google Scripts](https://script.google.com/) and create a new project.
2. Add the email sending logic to the script.
3. Deploy the script as a web app and ensure it has appropriate permissions.
4. Note the Web App URL and configure it in the server.

---

## Docker Deployment

### Step 1: Build the Docker Image
```bash
docker build -t ebook-metadata-server .
```

### Step 2: Run the Docker Container
```bash
docker run -d -p 8000:8000 --env-file .env ebook-metadata-server
```

---

## Future Enhancements
1. Add support for other eBook formats (e.g., EPUB, MOBI).
2. Implement a web-based UI for easier interaction.
3. Enhance metadata extraction with additional APIs.
4. Include automated scheduling for sending eBooks to Kindle.

---

## Contribution Guidelines
1. Fork the repository.
2. Create a new branch for your feature/fix.
3. Commit your changes and push to your fork.
4. Submit a pull request for review.

---

## License
This project is licensed under the MIT License. See the LICENSE file for details.

---

## Contact
For questions or support, please reach out to:
- **Email**: luannn010@gmail.com
- **GitHub**: [luannn010](https://github.com/luannn010)

