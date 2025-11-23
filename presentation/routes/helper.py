from fastapi import APIRouter, UploadFile, File
from business.controllers.dataController import DataController
from utils import Settings, get_settings, render_cv_to_html


from weasyprint import HTML
from fastapi.responses import StreamingResponse
from io import BytesIO
import state


helper_router = APIRouter()
data_controller = DataController()



@helper_router.post("/extract-text")
async def extract_text(file: UploadFile):
    valid = await data_controller.validate_uploaded_file(file)  # await here
    if not valid:
        return {"status": "invalid file"}
    
    result = await data_controller.extractFileText(file)  # await the async function
    cv_text = result['extracted_text']  # now safe to access
    
    return {"extracted_text": cv_text}




@helper_router.post("/validate-file")
async def validate_file(file: UploadFile):
    flag = await data_controller.validate_uploaded_file(file)
    return {"valid": flag}  # wrap in dict for JSON




@helper_router.get("/download-cv")
def download_cv(temp_id:int):
    latest_resume = state.latest_resume
    html_content= render_cv_to_html(latest_resume,temp_id)
    
    final_pdf_name='x'
    pdf_file = BytesIO()
    HTML(string=html_content).write_pdf(pdf_file)
    pdf_file.seek(0)  

    
    return StreamingResponse(
        pdf_file,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{final_pdf_name}.pdf"'}
    )
    
    
@helper_router.get("get_final_resume_html")
def get_final_html():
    return state.final_resume_html