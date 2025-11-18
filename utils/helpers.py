from docx import Document
import fitz


def gb_to_bytes(gb: float) -> int:
        """Convert GB to bytes."""
        BYTES_IN_GB = 1024 * 1024 * 1024
        return int(gb * BYTES_IN_GB)


def extract_pdf_text(file_bytes:bytes)->str:
        text=""
        pdf=fitz.open(stream=file_bytes, filetype="pdf")
        for page in pdf:
                text+=page.get_text()
        return text

def extract_docs_text(self, file_bytes:bytes)->str:
        doc = Document(file_bytes)
        text = "\n".join([p.text for p in doc.paragraphs])
        return text
