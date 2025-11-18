from fastapi import FastAPI, APIRouter, Depends
from utils import get_settings, Settings

import os
base_router = APIRouter()

@base_router.get("/")
async def root(settings: Settings = Depends(get_settings)):
    settings = get_settings()
    app_name = settings.APP_NAME
    return {
        "message": f"Wlecome to {app_name}!"
    }