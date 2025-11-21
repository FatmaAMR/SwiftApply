from fastapi import APIRouter, UploadFile, File
from business.controllers.dataController import DataController
from utils import Settings, get_settings

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
