from fastapi import APIRouter, UploadFile, File
from business.controllers.dataController import DataController
from business.llm.CVChatbot import CVChatbot

resume_router = APIRouter()
chatbot = CVChatbot()
data_controller = DataController()

@resume_router.post("/generate-cv")
async def generate_cv(cv_file: UploadFile, jd: str, notes: str,company_info:str, template_id: str = "default"):
    cv_text=""
    if data_controller.validate_uploaded_file(cv_file)[0]:
        cv_text = data_controller.extractFileText(cv_file)['extracted_text']

    parsed_cv = await chatbot.parse_cv(cv_text)
    analysis = await chatbot.analyze_cv(parsed_cv, jd_text, notes_text)
    final_cv = await chatbot.generate_cv(parsed_cv, analysis, template_id)

    return {"final_cv": final_cv}
