from fastapi import APIRouter, UploadFile, File
from business.controllers.dataController import DataController
from langchain_core.messages import HumanMessage

from utils import Settings, get_settings, render_cv_to_html
from business.llm.resume_llm import resume_llm
import state
import json

resume_router = APIRouter()
llm = resume_llm()
data_controller = DataController()
@resume_router.post("/generate-cv")
async def generate_cv(job_description_text: str, notes_text: str,company_info:str):
    parsed_cv=state.user_parsed_cv
    analysis = await llm.analyze_cv(parsed_cv, job_description_text, notes_text, company_info)
    final_results = await llm.generate_cv(parsed_cv, analysis,job_description_text, company_info)
    state.latest_resume=final_results
    return final_results



    