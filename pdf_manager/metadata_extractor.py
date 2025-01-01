import openai
import os
from PyPDF2 import PdfReader, PdfWriter
from dotenv import load_dotenv
import json

load_dotenv()

class PDFMetadataExtractor:
    def __init__(self, file_path, n_pages: int):
        self.file_path = file_path
        self.n_pages = n_pages

    def extract_metadata(self):
        reader = PdfReader(self.file_path)
        total_pages = len(reader.pages)

        # Determine unique pages to extract
        unique_pages = set(range(0, min(self.n_pages, total_pages))) | set(range(max(total_pages - self.n_pages, 0), total_pages))

        # Extract text from the pages
        extracted_text = []
        for page_num in sorted(unique_pages):
            page = reader.pages[page_num]
            extracted_text.append(page.extract_text())

        return "\n".join(extracted_text)


    @staticmethod
    def query_openai_for_metadata(text):
        try:
            prompt = f"""
            Extract metadata from the following text and return it in JSON format with the fields: title, authors, language, publisher, edition, publication_date, and ISBN. 
            If a field cannot be extracted, return it as \"Unknown\".
            {text}
            """

            response = openai.ChatCompletion.create(
                model=os.getenv("OPENAI_MODEL", "gpt-3.5-turbo"),
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that extracts metadata from text."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                temperature=0
            )

            if "choices" not in response or not response["choices"]:
                raise ValueError("Empty response from OpenAI API")

            content = response["choices"][0]["message"]["content"]
            if isinstance(content, str):
                # Clean up the response to ensure it can be parsed as JSON
                if content.startswith("```json"):
                    content = content.replace("```json", "").replace("```", "").strip()
                return json.loads(content)
            elif isinstance(content, dict):
                return content
            else:
                raise ValueError("Unexpected format in OpenAI response")

        except json.JSONDecodeError:
            print(f"Error decoding JSON: {content}")
            raise ValueError("Failed to decode JSON from OpenAI API response")

        except Exception as e:
            print(f"Error querying OpenAI API: {e}")
            raise




    @staticmethod
    def infer_language(text):
            if "the" in text.lower():
                return "English"
            elif "le" in text.lower():
                return "French"
            elif "el" in text.lower():
                return "Spanish"
            elif "và" in text.lower() or "của" in text.lower():
                return "Vietnamese"
            return "Unknown"

    def ensure_metadata_fields(self, metadata, text):
        required_fields = ["title", "authors", "language", "publisher", "edition", "publication_date", "ISBN"]

        for field in required_fields:
            # Check if field is missing or empty
            if field not in metadata or not metadata[field] or metadata[field] == "Unknown":
                metadata[field] = "Unknown"

        # Special handling for authors (list)
        if isinstance(metadata["authors"], list) and not metadata["authors"]:
            metadata["authors"] = "Unknown"
        elif isinstance(metadata["authors"], list):
            metadata["authors"] = ", ".join(metadata["authors"])  # Convert list to comma-separated string

        # Infer language if not provided
        if metadata["language"] == "Unknown":
            metadata["language"] = self.infer_language(text)

        # Infer title if not provided
        if metadata["title"] == "Unknown":
            metadata["title"] = os.path.splitext(os.path.basename(self.file_path))[0]

        return metadata



class CoverPageExtractor(PDFMetadataExtractor):
    def __init__(self, file_path, n_pages: int):
        super().__init__(file_path, n_pages)

    def extract_cover_page(self, output_dir):
        try:
            reader = PdfReader(self.file_path)

            if len(reader.pages) == 0:
                print("Error: The PDF file has no pages.")
                return None

            first_page = reader.pages[0]
            writer = PdfWriter()
            writer.add_page(first_page)

            os.makedirs(output_dir, exist_ok=True)
            output_file = os.path.join(output_dir, f"{os.path.splitext(os.path.basename(self.file_path))[0]}_cover.pdf")
            with open(output_file, "wb") as out_pdf:
                writer.write(out_pdf)
            print(f"Cover page saved to: {output_file}")
            return output_file

        except Exception as e:
            print(f"Error: Failed to extract cover page. {str(e)}")
            return None
if __name__ == "__main__":
    file_path = "./books/7 thoi quen de thanh dat.pdf"
    openai.api_key = os.getenv("OPENAI_API_KEY")

    if not openai.api_key:
        print("Error: OpenAI API key not found. Ensure it is set in the environment.")
        exit(1)

    print(f"Using OpenAI model: {os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo')}")


