from fastapi import APIRouter, UploadFile, Depends, status
from fastapi.responses import JSONResponse
from utils import get_settings, Settings
from business import DataController

data_router = APIRouter(prefix="/comprehensive-resume")

@data_router.post("/upload")
async def uploadCV(file: UploadFile, settings: Settings = Depends(get_settings), controller: DataController = Depends(DataController)):
    
    is_valid, signal = await controller.validate_uploaded_file(file)
    
    
    if is_valid==True:
        #extracting data from cv
        #cashing this data to user
        pass
    
    
    reponse_content = {
            "success": is_valid,
            "message": signal
            }
    
    return JSONResponse(
        status_code=status.HTTP_200_OK if is_valid
        else status.HTTP_400_BAD_REQUEST,
        content=reponse_content
    )

