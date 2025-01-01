from PyPDF2 import PdfReader

def check_pdf_metadata(pdf_path):
    try:
        reader = PdfReader(pdf_path)
        metadata = reader.metadata

        if not metadata:
            return "No metadata found in the PDF."

        print("Loaded Metadata:")
        response = ""
        for key, value in metadata.items():
            response += f"{key}: {value}\n"
        return response
    except Exception as e:
        return f"Error reading metadata: {e}"




# pdf_path = "./books/processed_pdfs/The 7 Habits Of Highly Effective People: Powerful Lessons In Personal Change.pdf"
# check_pdf_metadata(pdf_path=pdf_path)
# # Example usage
# pdf_path = "./books/processed_pdfs/Fundamentals Of Data Engineering.pdf"
# check_pdf_metadata(pdf_path)
