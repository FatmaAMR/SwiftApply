from docx import Document
import fitz
from weasyprint import HTML
from fastapi.responses import StreamingResponse
from io import BytesIO
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
from presentation.enums.templates_dect import TemplateID
env = Environment(loader=FileSystemLoader("templates"))



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

templates = {
        1:TemplateID.CLASSIC,
        2:TemplateID.MINIMAL,
        3:TemplateID.TWO_COL,
        4:TemplateID.FUUL_PAGE
}

def render_cv_to_html(json_data:dict, temp_num:int):
        path = templates[temp_num].value
        
        template = env.get_template(path)
        html_content = template.render(cv=json_data['cv'])  
        return html_content