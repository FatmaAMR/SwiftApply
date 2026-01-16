from fastapi import APIRouter, UploadFile, File, Form, Depends, status
from fastapi.responses import JSONResponse
from utils import get_settings, Settings
from business import DataController, resume_llm
import state

llm = resume_llm()
data_router = APIRouter(prefix="/comprehensive-resume")

@data_router.post("/upload")
async def upload_cv(
    file: UploadFile | None = File(None),
    text: str | None = Form(None),
    settings: Settings = Depends(get_settings),
    data_controller: DataController = Depends(DataController)
):
    if not file and not text:
        return JSONResponse(
            status_code=400,
            content={"success": False, "message": "No CV provided"}
        )

    cv_text = ""

    if file:
        is_valid = await data_controller.validate_uploaded_file(file)
        if not is_valid:
            return JSONResponse(
                status_code=400,
                content={"success": False, "message": "Invalid CV file format"}
            )
        result = await data_controller.extractFileText(file)
        cv_text += result["extracted_text"]

    if text:
        cv_text += "\n" + text

    parsed_cv = await llm.parse_cv(cv_text)
    

    return JSONResponse(
        status_code=200,
        content={
            "success": True,
            "cv": parsed_cv,
            "message": "CV processed successfully"
        }
    )
