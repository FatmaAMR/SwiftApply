from business import BaseController
from fastapi import UploadFile
from presentation.enums.responseEnum import ResponseSignal
from utils import gb_to_bytes, extract_docs_text, extract_pdf_text
import os 
class DataController(BaseController):
    
    def __init__(self):
        super().__init__()
        
    async def validate_uploaded_file(self, file:UploadFile):
        
        filename = file.filename 
        
        ext = os.path.splitext(filename)[1].lower().replace(".", "")
        
        if ext not in self.app_settings.FILE_ALLOWED_TYPES:
            return False

        contents = await file.read()
        max_bytes = gb_to_bytes(self.app_settings.FILE_MAX_SIZE)

        if len(contents) > max_bytes:
            return False

        await file.seek(0)
        return True
    
    
    async def extractFileText(self, file: UploadFile):
        
        file_bytes = await file.read()

        if file.filename.endswith(".pdf"):
            text = extract_pdf_text(file_bytes)
        elif file.filename.endswith(".docx"):
            text = extract_docs_text(file_bytes)
        else:
            text = file_bytes.decode("utf-8")

        cleaned = text.replace("\n\n", "\n").strip()

        return {"extracted_text": cleaned}