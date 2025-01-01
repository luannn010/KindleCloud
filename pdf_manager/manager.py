import os
import json
from PyPDF2 import PdfReader, PdfWriter
from pdf_manager.metadata_extractor import PDFMetadataExtractor, CoverPageExtractor

class PDFManager:
    def __init__(self, file_path, n_pages: int, save_metadata=False, save_cover_page=False):
        self.metadata_extractor = PDFMetadataExtractor(file_path, n_pages)
        self.cover_page_extractor = CoverPageExtractor(file_path, n_pages)
        self.save_metadata = save_metadata
        self.save_cover_page = save_cover_page

    def process_pdf(self):
        extracted_text = self.metadata_extractor.extract_metadata()

        metadata = {
            "title": "Unknown",
            "authors": "Unknown",
            "language": "Unknown",
            "publisher": "Unknown",
            "edition": "Unknown",
            "publication_date": "Unknown",
            "ISBN": "Unknown"
        }

        try:
            new_metadata = self.metadata_extractor.query_openai_for_metadata(extracted_text)
            print(f"Parsed metadata: {new_metadata}")  # Debug: parsed metadata from OpenAI

            metadata = self.metadata_extractor.ensure_metadata_fields(new_metadata, extracted_text)
            print(f"Final metadata after ensuring fields: {metadata}")  # Debug: final metadata
        except Exception as e:
            print(f"Error during metadata extraction: {e}")

        # Define output directories
        base_dir = os.path.dirname(self.metadata_extractor.file_path)
        processed_dir = os.path.join(base_dir, "processed_pdfs")
        metadata_dir = os.path.join(base_dir, "metadata")
        os.makedirs(processed_dir, exist_ok=True)
        os.makedirs(metadata_dir, exist_ok=True)

        # Save the cover page if enabled
        cover_file = None
        if self.save_cover_page:
            cover_file = self.extract_and_save_cover_page(metadata_dir)

        # Attach metadata and cover page to PDF
        updated_pdf_path = os.path.join(processed_dir, f"{os.path.splitext(os.path.basename(self.metadata_extractor.file_path))[0]}_with_metadata.pdf")
        self.attach_metadata_and_cover_to_pdf(self.metadata_extractor.file_path, updated_pdf_path, metadata, cover_file)

        # Rename the file based on the title
        renamed_pdf_path = self.rename_pdf_by_title(updated_pdf_path, metadata["title"])

        # Save metadata as a JSON file if enabled
        metadata_file = None
        if self.save_metadata:
            metadata_file = os.path.join(metadata_dir, f"{os.path.splitext(os.path.basename(self.metadata_extractor.file_path))[0]}_metadata.json")
            with open(metadata_file, "w", encoding="utf-8") as file:
                json.dump(metadata, file, indent=4, ensure_ascii=False)

        print(f"Metadata attached and saved to: {renamed_pdf_path}")
        return metadata_file, cover_file, renamed_pdf_path

    def extract_and_save_cover_page(self, metadata_dir):
        try:
            reader = PdfReader(self.metadata_extractor.file_path)
            cover_page = reader.pages[0]  # Assuming the first page is the cover page
            cover_page_path = os.path.join(metadata_dir, f"{os.path.splitext(os.path.basename(self.metadata_extractor.file_path))[0]}_cover_page.pdf")

            writer = PdfWriter()
            writer.add_page(cover_page)

            with open(cover_page_path, "wb") as cover_pdf:
                writer.write(cover_pdf)

            print(f"Cover page successfully saved to: {cover_page_path}")
            return cover_page_path
        except Exception as e:
            print(f"Error extracting cover page: {e}")
            return None

    @staticmethod
    def attach_metadata_and_cover_to_pdf(input_pdf, output_pdf, metadata, cover_file):
        try:
            # Open the existing PDF
            reader = PdfReader(input_pdf)
            writer = PdfWriter()

            # Add the cover page first, if available
            if cover_file:
                cover_reader = PdfReader(cover_file)
                writer.add_page(cover_reader.pages[0])

            # Copy pages from the original PDF
            for page in reader.pages:
                writer.add_page(page)

            # Set metadata with standard keys
            writer.add_metadata({
                "/Title": metadata.get("title", "Unknown"),
                "/Author": metadata.get("authors", "Unknown"),
                "/Subject": metadata.get("publisher", "Unknown"),
                "/Keywords": metadata.get("ISBN", "Unknown"),
                "/CreationDate": metadata.get("publication_date", "Unknown"),
                "/Producer": "PDF Metadata Manager"
            })

            # Write to the output file
            with open(output_pdf, "wb") as output:
                writer.write(output)

            print(f"Metadata and cover page successfully attached to PDF: {output_pdf}")
        except Exception as e:
            print(f"Error attaching metadata and cover page to PDF: {e}")

    @staticmethod
    def rename_pdf_by_title(pdf_path, title):
        try:
            if not title or title.strip() == "Unknown":
                print("Title is unknown. Skipping renaming.")
                return pdf_path

            dir_path = os.path.dirname(pdf_path)
            formatted_title = " ".join([word.capitalize() for word in title.strip().split()])
            new_name = f"{formatted_title}.pdf"
            renamed_path = os.path.join(dir_path, new_name)

            os.rename(pdf_path, renamed_path)
            print(f"PDF renamed to: {renamed_path}")
            return renamed_path
        except Exception as e:
            print(f"Error renaming PDF: {e}")
            return pdf_path
