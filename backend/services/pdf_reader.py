import requests
from io import BytesIO
from PyPDF2 import PdfReader

class PDFReader:
    def extract_text(self, pdf_url: str):
        try:
            headers = {
                "User-Agent": "Mozilla/5.0"
            }

            response = requests.get(pdf_url, headers=headers)

            if response.status_code != 200:
                print("Failed to download PDF:", response.status_code)
                return None

            pdf_file = BytesIO(response.content)
            reader = PdfReader(pdf_file)

            text = ""

            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text

            return text.strip()

        except Exception as e:
            print("PDF extraction error:", e)
            return None
