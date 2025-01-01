from PyPDF2 import PdfReader

def check_pdf_metadata(pdf_path):
    try:
        reader = PdfReader(pdf_path)
        metadata = reader.metadata
        print("Loaded Metadata:")
        for key, value in metadata.items():
            print(f"{key}: {value}")
    except Exception as e:
        print(f"Error reading metadata: {e}")



# pdf_path = "./books/processed_pdfs/The 7 Habits Of Highly Effective People: Powerful Lessons In Personal Change.pdf"
# check_pdf_metadata(pdf_path=pdf_path)
# # Example usage
# pdf_path = "./books/processed_pdfs/Fundamentals Of Data Engineering.pdf"
# check_pdf_metadata(pdf_path)
