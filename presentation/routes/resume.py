from fastapi import APIRouter, UploadFile, File
from business.controllers.dataController import DataController
from langchain_core.messages import HumanMessage

from utils import Settings, get_settings
from business.llm.resume_llm import resume_llm

resume_router = APIRouter()
llm = resume_llm()
data_controller = DataController()

@resume_router.post("/generate-cv")
async def generate_cv(cv_file: UploadFile, job_description_text: str, notes_text: str,company_info:str, template_id: str = "default"):
    cv_text=""
    if await data_controller.validate_uploaded_file(cv_file):
        extracted = (await data_controller.extractFileText(cv_file))
        cv_text=extracted["extracted_text"]
    parsed_cv = await llm.parse_cv(cv_text)
    analysis = await llm.analyze_cv(parsed_cv, job_description_text, notes_text, company_info)
    final_cv = await llm.generate_cv(parsed_cv, analysis, template_id)

    return {"final_cv": final_cv}
