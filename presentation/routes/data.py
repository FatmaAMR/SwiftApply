from fastapi import APIRouter, UploadFile, Depends, status, Request
from fastapi.responses import JSONResponse
from utils import get_settings, Settings
from business import DataController, resume_llm
import state


llm = resume_llm()
data_router = APIRouter(prefix="/comprehensive-resume")

@data_router.post("/upload")
async def uploadCV(file: UploadFile, settings: Settings = Depends(get_settings), data_controller: DataController = Depends(DataController)):
    parsed_cv = {}
    is_valid = await data_controller.validate_uploaded_file(file)
    
    msg="Invalid CV format!❌"
    if is_valid==True:
        result = await data_controller.extractFileText(file)
        cv_text = result['extracted_text'] 
        parsed_cv = await llm.parse_cv(cv_text)
        msg="Your Comprehansive CV is uploaded succesfully!🎉 \n It's time to swift your applys!🧑🏻‍🎓"
        
        state.user_parsed_cv = parsed_cv
        #cashing parsed_cv
        pass
    
    
    reponse_content = {
            "success": is_valid,
            "cv":parsed_cv,
            "message":msg
            }
    
    return JSONResponse(
        status_code=status.HTTP_200_OK if is_valid
        else status.HTTP_400_BAD_REQUEST,
        content=reponse_content
    )

